// \frontend\Alternative_data_frontend\frontend\app\page.tsx

"use client";
"use client";
import { useEffect, useMemo, useState, type ReactNode } from "react";
import useSWR from "swr";
import {
    ResponsiveContainer,
    AreaChart,
    Area,
    CartesianGrid,
    XAxis,
    YAxis,
    Tooltip,
    Brush,
} from "recharts";
import dynamic from "next/dynamic";

// --- API 設定 ---
const fetcher = async (url: string) => {
    const res = await fetch(url);
    try { return await res.json(); } catch { return null; }
};
const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
const MapCard = dynamic(() => import("../components/MapCard"), { ssr: false });

// ---------------- UI/表示コンポーネント (変更なし) ----------------
function StatCard({ label, value, delta }: { label: string; value: string; delta?: string }) {
    return (
        <div className="rounded-2xl shadow-soft p-5 bg-surface-200 border border-brand-900/40">
            <div className="text-sm text-brand-200/80">{label}</div>
            <div className="mt-2 text-3xl font-semibold text-white">{value}</div>
            {delta && <div className="mt-1 text-xs text-brand-200/70">前週比 {delta}</div>}
        </div>
    );
}
function Badge({ children }: { children: ReactNode }) {
    return (
        <span className="inline-flex items-center rounded-lg border border-brand-800/60 bg-surface-100 px-2 py-0.5 text-[11px] text-brand-100/90">
            {children}
        </span>
    );
}
function HelpDialog({ open, onClose }: { open: boolean; onClose: () => void }) {
    if (!open) return null;
    return (
        <div role="dialog" aria-modal="true" aria-label="使い方ヘルプ" className="fixed inset-0 z-50 flex items-center justify-center">
            <div className="absolute inset-0 bg-black/60" onClick={onClose} />
            <div className="relative w-[min(720px,90vw)] rounded-2xl border border-brand-900/50 bg-surface-200 p-6 shadow-soft">
                <div className="flex items-center justify-between">
                    <h3 className="text-white text-lg font-semibold">使い方ヘルプ</h3>
                    <button className="text-brand-200/80 hover:text-white" onClick={onClose} aria-label="閉じる">×</button>
                </div>
                <div className="mt-4 space-y-4 text-sm text-brand-100/90">
                    <div>
                        <div className="font-medium text-brand-50">① 範囲プリセット</div>
                        <p>
                            <Badge>日</Badge> / <Badge>週</Badge> / <Badge>月</Badge> / <Badge>年</Badge> / <Badge>最大</Badge> で
                            “表示するデータ点数”を切替えます（バックエンドが週次でも見た目が大きく変わります）。
                        </p>
                    </div>
                    <div>
                        <div className="font-medium text-brand-50">② 過去へ／先へ</div>
                        <p>◀ / ▶ は現在のウィンドウ幅ぶんだけ隣接ウィンドウにスライドします。⏮＝最古、⏭＝最新。</p>
                    </div>
                    <div>
                        <div className="font-medium text-brand-50">③ ブラシ</div>
                        <p>下の小窓で範囲をドラッグすると <Badge>カスタム</Badge> 表示になります。</p>
                    </div>
                    <div>
                        <div className="font-medium text-brand-50">④ 変動の根拠</div>
                        <p>ツールチップと表に <Badge>evidence</Badge>（寄与）を表示します。</p>
                    </div>
                </div>
                <div className="mt-6 text-xs text-brand-200/70">Esc で閉じます。</div>
            </div>
        </div>
    );
}
function CustomTooltip({ active, payload, label }: any) {
    if (!active || !payload || !payload.length) return null;
    const p = payload[0]?.payload ?? {};
    const reasons: any[] = p.evidence ?? [];
    const dateLabel = new Date(typeof label === "number" ? label : p.x).toLocaleDateString("ja-JP", { month: "2-digit", day: "2-digit" });
    return (
        <div className="rounded-xl border border-brand-900/50 bg-surface-100 p-3 shadow-soft">
            <div className="text-xs text-brand-200/80">週: {dateLabel}</div>
            <div className="mt-1 text-white text-sm font-semibold">値: {Number(p.value).toFixed(2)}</div>
            {reasons.length ? (
                <div className="mt-2 space-y-1">
                    <div className="text-xs text-brand-200/80">変動の根拠</div>
                    <ul className="space-y-1">
                        {reasons.slice(0, 5).map((r, i) => (
                            <li key={i} className="text-[12px] text-brand-100/90">
                                <Badge>{r.source ?? r.name ?? "要因"}</Badge>
                                {typeof r.weight === "number" && <span className="ml-2 opacity-80">寄与: {(r.weight * 100).toFixed(0)}%</span>}
                                {r.note && <span className="ml-2 opacity-80">{r.note}</span>}
                            </li>
                        ))}
                    </ul>
                </div>
            ) : <div className="mt-2 text-[12px] text-brand-200/70">根拠データなし</div>}
        </div>
    );
}

// ---------------- 範囲ロジック（点数ベース） ----------------
type RangeMode = "DAY" | "WEEK" | "MONTH" | "YEAR" | "ALL";

// 週次データでも確実に見た目が変わる点数
const WINDOW_POINTS: Record<Exclude<RangeMode, "CUSTOM">, number> = {
    DAY: 12,     // 直近12点（約3ヶ月の週次でもギュッと）
    WEEK: 26,    // 約半年
    MONTH: 52,   // 約1年
    YEAR: 156,   // 約3年
    ALL: Infinity,
};

// ---------------- メインページコンポーネント ----------------
export default function Page() {
    const [metric, setMetric] = useState("mfg_index");
    const [helpOpen, setHelpOpen] = useState(false);
    const [mode, setMode] = useState<RangeMode>("MONTH"); // 既定は「月」
    const [attrLoaded, setAttrLoaded] = useState(false); // 属性データが読み込まれたか追跡

    // データ取得 (教授のAPIエンドポイントを使用)
    const { data: ts } = useSWR(`${API_BASE}/api/timeseries?metric=${metric}&frequency=weekly`, fetcher);
    // 属性データはダミーなので、ここでは単一のSWRフックに統合（attrは不要）
    const { data: geo } = useSWR(`${API_BASE}/api/geo/activity`, fetcher);

    // date→evidence マッピング (教授のバックエンドはattributionエンドポイントを持たないため、tsデータにevidenceが直接含まれることを前提とする)
    const evidenceMap = useMemo(() => {
        const m = new Map<string, any[]>();
        if (ts?.series) {
            for (const p of ts.series) {
                const k = new Date(p.date).toISOString().slice(0, 10);
                const r = p.evidence ?? p.drivers ?? p.attribution;
                if (r) m.set(k, r);
            }
        }
        // NOTE: 教授のバックエンドにはevidenceフィールドがないため、実際にはこのマップは空になります。
        // ここでは、データポイントの 'activity' 値を evidence として表示する仮ロジックは省略します。
        return m;
    }, [ts]);


    // グラフ用データ
    const chartData = useMemo(() => {
        if (!ts?.series) return [];
        return ts.series.map((p: any) => {
            const iso = new Date(p.date).toISOString().slice(0, 10);
            const x = new Date(iso).getTime();
            // evidenceMapからデータを取得
            return { iso, x, value: p.value, evidence: evidenceMap.get(iso) ?? [] };
        });
    }, [ts, evidenceMap]);

    const len = chartData.length;

    // 表示しているデータ点（インデックス範囲: 両端含む）
    const [idxRange, setIdxRange] = useState<[number, number] | null>(null);

    // モード切替時：最新側にウィンドウを合わせる
    useEffect(() => {
        if (len === 0) return;
        const pointMode = mode as Exclude<RangeMode, "CUSTOM">;
        if (mode === 'CUSTOM') {
            return;
        }
        const width = WINDOW_POINTS[pointMode] === Infinity ? len : Math.min(WINDOW_POINTS[pointMode], len);
        const start = WINDOW_POINTS[pointMode] === Infinity ? 0 : Math.max(0, len - width);
        const end = len - 1;

        setIdxRange([start, end]);
    }, [mode, len]);

    // X軸 domain をインデックスから計算
    const domain: [number, number] | undefined = useMemo(() => {
        if (!idxRange || len === 0) return undefined;
        const [s, e] = idxRange;
        return [chartData[s].x, chartData[e].x];
    }, [idxRange, chartData, len]);

    // ---- ナビゲーション（隣接ウィンドウにピタッと送る）----
    const step = (dir: -1 | 1) => {
        if (!idxRange || len === 0) return;
        const [s, e] = idxRange;
        const width = e - s + 1;

        let ns: number, ne: number;
        if (dir === -1) {
            ne = s - 1;
            ns = ne - (width - 1);
        } else {
            ns = e + 1;
            ne = ns + (width - 1);
        }

        // クランプ（幅は維持）
        if (ns < 0) {
            ns = 0;
            ne = Math.min(len - 1, ns + width - 1);
        }
        if (ne > len - 1) {
            ne = len - 1;
            ns = Math.max(0, ne - (width - 1));
        }

        setIdxRange([ns, ne]);
    };

    const jumpOldest = () => {
        if (len === 0 || !idxRange) return;
        const width = idxRange[1] - idxRange[0] + 1;
        const ns = 0;
        const ne = Math.min(len - 1, ns + width - 1);
        setIdxRange([ns, ne]);
    };

    const jumpNewest = () => {
        if (len === 0 || !idxRange) return;
        const width = idxRange[1] - idxRange[0] + 1;
        const ne = len - 1;
        const ns = Math.max(0, ne - (width - 1));
        setIdxRange([ns, ne]);
    };

    // Brush → カスタム範囲
    const onBrushChange = (range: { startIndex?: number; endIndex?: number }) => {
        const { startIndex, endIndex } = range;
        if (startIndex == null || endIndex == null) return;
        const s = Math.max(0, Math.min(startIndex, endIndex));
        const e = Math.min(len - 1, Math.max(startIndex, endIndex));
        setIdxRange([s, e]);
        // setMode("CUSTOM"); // カスタムモード切り替えが必要なら有効化
    };

    // サマリー
    const latest = chartData.at(-1)?.value;
    const prev = chartData.at(-2)?.value ?? latest ?? 0;
    const deltaVal = (Number(latest ?? 0) - Number(prev ?? 0));
    const delta = (deltaVal >= 0 ? "+" : "") + deltaVal.toFixed(2);

    type ChartPoint = {
        iso: string;
        x: number;
        value: number;
        evidence: any[]; // evidenceの具体的な型が不明なためany[]とする
    };

    return (
        <main className="min-h-screen px-6 py-6 md:px-10">
            {/* ヘッダー */}
            <header className="mb-6 flex items-center justify-between">
                <h1 className="text-white text-2xl md:text-3xl font-semibold tracking-tight">
                    製造業ナウキャスト・ダッシュボード
                </h1>
                <div className="flex items-center gap-2">
                    <select
                        className="bg-surface-100 border border-brand-800 text-white text-sm rounded-xl px-3 py-2"
                        value={metric}
                        onChange={e => setMetric(e.target.value)}
                        aria-label="メトリクスを選択"
                    >
                        <option value="mfg_index">製造業指数</option>
                        <option value="orders">新規受注</option>
                    </select>
                    <button
                        className="rounded-xl border border-brand-800 bg-surface-100 px-3 py-2 text-sm text-brand-100/90 hover:text-white"
                        onClick={() => setHelpOpen(true)}
                        aria-haspopup="dialog"
                    >
                        ？ ヘルプ
                    </button>
                </div>
            </header>

            {/* サマリー */}
            <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <StatCard label="最新値" value={Number.isFinite(Number(latest)) ? Number(latest).toFixed(2) : "—"} delta={delta} />
                <StatCard label="サンプル: 直近観測数" value={(len ?? 0).toString()} />
                <StatCard label="メトリクス" value={metric === "mfg_index" ? "製造業指数" : "新規受注"} />
            </section>

            {/* グラフ＆レンジ操作 */}
            <section className="mt-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 rounded-2xl shadow-soft p-5 bg-surface-200 border border-brand-900/40">
                    {/* コントロールバー */}
                    <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
                        <div className="flex items-center gap-1">
                            {(["DAY", "WEEK", "MONTH", "YEAR", "ALL"] as RangeMode[]).map((m) => (
                                <button
                                    key={m}
                                    onClick={() => setMode(m)}
                                    className={`px-3 py-1.5 text-xs rounded-lg border ${mode === m
                                            ? "border-cyan-400 text-white bg-cyan-400/10"
                                            : "border-brand-800 text-brand-100/90 bg-surface-100 hover:text-white"
                                        }`}
                                >
                                    {m === "DAY" && "日"}
                                    {m === "WEEK" && "週"}
                                    {m === "MONTH" && "月"}
                                    {m === "YEAR" && "年"}
                                    {m === "ALL" && "最大"}
                                </button>
                            ))}
                            {mode === "CUSTOM" && <Badge>カスタム</Badge>}
                        </div>
                        <div className="flex items-center gap-1">
                            <button className="px-2 py-1 text-xs rounded-lg border border-brand-800 bg-surface-100 text-brand-100/90 hover:text-white" onClick={jumpOldest} title="最古へ">⏮</button>
                            <button className="px-2 py-1 text-xs rounded-lg border border-brand-800 bg-surface-100 text-brand-100/90 hover:text-white" onClick={() => step(-1)} title="左へ（過去へ）">◀</button>
                            <button className="px-2 py-1 text-xs rounded-lg border border-brand-800 bg-surface-100 text-brand-100/90 hover:text-white" onClick={() => step(1)} title="右へ（先へ）">▶</button>
                            <button className="px-2 py-1 text-xs rounded-lg border border-brand-800 bg-surface-100 text-brand-100/90 hover:text-white" onClick={jumpNewest} title="最新へ">⏭</button>
                        </div>
                    </div>

                    {/* チャート */}
                    <div className="h-80">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart
                                key={`${idxRange?.[0]}-${idxRange?.[1]}`}
                                data={chartData}
                                margin={{ top: 8, right: 12, left: 12, bottom: 8 }}
                            >
                                <defs>
                                    <linearGradient id="grad" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#10a8dc" stopOpacity={0.6} />
                                        <stop offset="95%" stopColor="#10a8dc" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="#074e66" opacity={0.3} />
                                <XAxis
                                    dataKey="x"
                                    type="number"
                                    scale="time"
                                    domain={domain ?? ["dataMin", "dataMax"]}
                                    allowDataOverflow
                                    stroke="#92e4ff"
                                    tick={{ fontSize: 12 }}
                                    tickFormatter={(v: number) =>
                                        new Date(v).toLocaleDateString("ja-JP", { month: "2-digit", day: "2-digit" })
                                    }
                                />
                                <YAxis stroke="#92e4ff" tick={{ fontSize: 12 }} />
                                <Tooltip content={<CustomTooltip />} />
                                <Area type="monotone" dataKey="value" stroke="#10a8dc" fillOpacity={1} fill="url(#grad)" />
                                <Brush
                                    dataKey="x"
                                    height={28}
                                    travellerWidth={8}
                                    stroke="#0b6e8b"
                                    fill="#052733"
                                    startIndex={idxRange?.[0]}
                                    endIndex={idxRange?.[1]}
                                    tickFormatter={(v: number) =>
                                        new Date(v).toLocaleDateString("ja-JP", { month: "2-digit", day: "2-digit" })
                                    }
                                    onChange={onBrushChange}
                                />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>

                    {/* 変動の根拠 */}
                    <div className="mt-4">
                        <div className="mb-2 flex items-center justify-between">
                            <h3 className="text-white/90 text-sm font-medium">各時点の「変動の根拠」</h3>
                            <span className="text-[11px] text-brand-200/70">最新12件を表示</span>
                        </div>
                        <div className="max-h-56 overflow-auto rounded-xl border border-brand-900/40 bg-surface-100">
                            <table className="w-full text-[12px]">
                                <thead className="sticky top-0 bg-surface-100/95 backdrop-blur">
                                    <tr className="text-brand-200/70">
                                        <th className="px-3 py-2 text-left font-normal">週</th>
                                        <th className="px-3 py-2 text-right font-normal">値</th>
                                        <th className="px-3 py-2 text-right font-normal">前週差</th>
                                        <th className="px-3 py-2 text-left font-normal">主要ドライバー</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {chartData.slice(-12).map((d: ChartPoint, i: number, arr: ChartPoint[]) => {
                                        // d, i, arr の型が ChartPoint, number, ChartPoint[] として確定しました
                                        const prevVal = arr[i - 1]?.value ?? d.value;
                                        const dd = Number(d.value) - Number(prevVal);
                                        const main = (d.evidence ?? []).slice(0, 3);
                                        return (
                                            <tr key={d.iso} className="border-t border-brand-900/30">
                                                <td className="px-3 py-2 text-brand-100/90">
                                                    {new Date(d.x).toLocaleDateString("ja-JP", { month: "2-digit", day: "2-digit" })}
                                                </td>
                                                <td className="px-3 py-2 text-right text-white">{Number(d.value).toFixed(2)}</td>
                                                <td className={`px-3 py-2 text-right ${dd >= 0 ? "text-emerald-300" : "text-rose-300"}`}>
                                                    {(dd >= 0 ? "+" : "") + dd.toFixed(2)}
                                                </td>
                                                <td className="px-3 py-2">
                                                    {main.length ? (
                                                        <div className="flex flex-wrap gap-1">
                                                            {main.map((r: any, j: number) => (
                                                                <Badge key={j}>
                                                                    {(r.source ?? r.name ?? "要因") +
                                                                        (typeof r.weight === "number" ? ` ${(r.weight * 100).toFixed(0)}%` : "")}
                                                                </Badge>
                                                            ))}
                                                        </div>
                                                    ) : <span className="text-brand-200/60">根拠データなし</span>}
                                                </td>
                                            </tr>
                                        );
                                    })}
                                </tbody>
                            </table>
                        </div>
                        <p className="mt-2 text-[11px] text-brand-200/60">
                            注: ドライバーは API 応答に含まれる <code>evidence / drivers / attribution</code> を自動表示します。
                        </p>
                    </div>
                </div>

                {/* 地図 */}
                <div className="rounded-2xl shadow-soft p-5 bg-surface-200 border border-brand-900/40">
                    <h2 className="text-white/90 font-medium mb-3">活動ヒート（サンプル）</h2>
                    <div className="h-72">
                        <MapCard geo={geo} />
                    </div>
                    <p className="mt-2 text-xs text-brand-200/60">※ デモデータ（OpenStreetMap タイル使用）</p>
                </div>
            </section>

            <HelpDialog open={helpOpen} onClose={() => setHelpOpen(false)} />
        </main>
    );
}