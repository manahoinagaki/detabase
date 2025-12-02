// \frontend\Alternative_data_frontend\frontend\app\page copy.tsx

"use client";
import { useMemo, useState } from "react";
import useSWR from "swr";
import { ResponsiveContainer, AreaChart, Area, CartesianGrid, XAxis, YAxis, Tooltip } from "recharts";
import dynamic from "next/dynamic";

const fetcher = (url: string) => fetch(url).then(res => res.json());
const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
const MapCard = dynamic(() => import("../components/MapCard"), { ssr: false });

function StatCard({ label, value, delta }: { label: string; value: string; delta?: string }) {
  return (
    <div className="rounded-2xl shadow-soft p-5 bg-surface-200 border border-brand-900/40">
      <div className="text-sm text-brand-200/80">{label}</div>
      <div className="mt-2 text-3xl font-semibold text-white">{value}</div>
      {delta && <div className="mt-1 text-xs text-brand-200/70">前週比 {delta}</div>}
    </div>
  );
}

export default function Page() {
  const [metric, setMetric] = useState("mfg_index");
  const { data: ts } = useSWR(`${API_BASE}/api/timeseries?metric=${metric}&frequency=weekly`, fetcher);
  const { data: geo } = useSWR(`${API_BASE}/api/geo/activity`, fetcher);

  const chartData = useMemo(() => {
    if (!ts?.series) return [];
    return ts.series.map((p: any) => ({
      date: new Date(p.date).toISOString().slice(5, 10),
      value: p.value
    }));
  }, [ts]);

  const latest = chartData.at(-1)?.value ?? 0;
  const prev = chartData.at(-2)?.value ?? latest;
  const delta = (latest - prev).toFixed(2);

  return (
    <main className="min-h-screen px-6 py-6 md:px-10">
      <header className="mb-6 flex items-center justify-between">
        <h1 className="text-white text-2xl md:text-3xl font-semibold tracking-tight">
          製造業ナウキャスト・ダッシュボード
        </h1>
        <div className="flex gap-2">
          <select
            className="bg-surface-100 border border-brand-800 text-white text-sm rounded-xl px-3 py-2"
            value={metric}
            onChange={e => setMetric(e.target.value)}
          >
            <option value="mfg_index">製造業指数</option>
            <option value="orders">新規受注</option>
          </select>
        </div>
      </header>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard label="最新値" value={latest ? latest.toFixed(2) : '—'} delta={(parseFloat(delta) >= 0 ? "+" : "") + delta} />
        <StatCard label="サンプル: 直近観測数" value={(chartData?.length ?? 0).toString()} />
        <StatCard label="メトリクス" value={metric === "mfg_index" ? "製造業指数" : "新規受注"} />
      </section>

      <section className="mt-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 rounded-2xl shadow-soft p-5 bg-surface-200 border border-brand-900/40">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-white/90 font-medium">トレンド</h2>
            <span className="text-xs text-brand-200/70">週次</span>
          </div>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="grad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10a8dc" stopOpacity={0.6}/>
                    <stop offset="95%" stopColor="#10a8dc" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#074e66" opacity={0.3} />
                <XAxis dataKey="date" stroke="#92e4ff" tick={{ fontSize: 12 }} />
                <YAxis stroke="#92e4ff" tick={{ fontSize: 12 }} />
                <Tooltip />
                <Area type="monotone" dataKey="value" stroke="#10a8dc" fillOpacity={1} fill="url(#grad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-2xl shadow-soft p-5 bg-surface-200 border border-brand-900/40">
          <h2 className="text-white/90 font-medium mb-3">活動ヒート（サンプル）</h2>
          <div className="h-72">
            <MapCard geo={geo} />
          </div>
          <p className="mt-2 text-xs text-brand-200/60">※ デモデータ（OpenStreetMap タイル使用）</p>
        </div>
      </section>
    </main>
  );
}
