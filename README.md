# 製造業ナウキャスト・ダッシュボード
### Manufacturing Nowcast Dashboard

オルタナティブデータ（衛星画像・位置情報など）を活用した製造業指数のリアルタイム可視化プロトタイプです。  
週次データのトレンド表示・地理的活動ヒートマップ・変動根拠の分析UIを備えています。

> ⚠️ このリポジトリは**研究・学習目的のプロトタイプ**です。衛星データ等のオルタナティブデータ取得可否の検証を目的としています。

---

## 📸 スクリーンショット

<!-- スクリーンショットを assets/ フォルダに配置後、下記を更新してください -->
<!-- ![Dashboard Screenshot](./assets/screenshot.png) -->

---

## 🎯 プロジェクト概要

| 項目 | 内容 |
|------|------|
| 目的 | 衛星・位置情報等のオルタナティブデータを用いた製造業指数のナウキャスティング |
| データソース | ダミーデータ（将来：夜間光衛星データ・船舶AISデータ等） |
| 対象指標 | 製造業指数 (`mfg_index`)・新規受注 (`orders`) |
| 更新頻度 | 週次 |

---

## 🏗️ アーキテクチャß

```
┌─────────────────────────────────────────┐
│            Next.js Frontend              │
│  (React + Recharts + Leaflet)            │
│  localhost:3000                          │
└────────────────┬────────────────────────┘
                 │ REST API (HTTP)
┌────────────────▼────────────────────────┐
│            FastAPI Backend               │
│  /api/timeseries  /api/geo/activity      │
│  localhost:8000                          │
└────────────────┬────────────────────────┘
                 │ (将来接続予定)
┌────────────────▼────────────────────────┐
│          External Database               │
│  PostgreSQL / SQLite (sales_data.db)     │
└─────────────────────────────────────────┘
```

---

## 📁 ディレクトリ構成

```
DETABASE/
├── app/                          # Streamlit 試作 (旧バージョン)
│   ├── .streamlit/
│   │   └── secrets.toml          # DB接続情報 (⚠️ .gitignore 必須)
│   └── main.py                   # Streamlit エントリポイント
│
├── frontend/                     # Next.js フロントエンド
│   └── app/
│       ├── globals.css           # グローバルスタイル (Tailwind + ダークテーマ)
│       ├── layout.tsx            # ルートレイアウト
│       └── page.tsx              # メインダッシュボード画面
│   └── components/
│       └── MapCard.tsx           # Leaflet 地図コンポーネント
│
├── main.py                       # FastAPI バックエンド (APIサーバー)
├── requirements.txt              # Python 依存パッケージ
├── sales_data.db                 # SQLite データベース
└── README.md
```

---

## 🖥️ 主な機能

**ダッシュボード (`page.tsx`)**

| 機能 | 説明 |
|------|------|
| 📊 トレンドチャート | Rechartsによる週次時系列グラフ（エリアチャート） |
| 🗺️ 活動ヒートマップ | Leaflet + OpenStreetMap による拠点別活動量の地図表示 |
| 🔢 サマリーカード | 最新値・前週比・データ点数 |
| 📅 期間フィルター | 日 / 週 / 月 / 年 / 最大 のプリセット切替 |
| ◀▶ ナビゲーション | 時間軸のスライド移動・最古／最新ジャンプ |
| 🖱️ ブラシ操作 | チャート下部の小窓でカスタム範囲選択 |
| 📋 変動根拠テーブル | 各時点の主要ドライバー（evidence フィールド）を一覧表示 |
| ❓ ヘルプダイアログ | 操作説明のモーダル |

---

## 🚀 セットアップ

### 前提条件

- Python 3.10+
- Node.js 18+

### 1. バックエンド（FastAPI）起動

```bash
# 依存パッケージのインストール
pip install -r requirements.txt

# サーバー起動（ポート8000）
uvicorn main:app --reload --port 8000
```

APIドキュメント: [http://localhost:8000/docs](http://localhost:8000/docs)

### 2. フロントエンド（Next.js）起動

```bash
cd frontend
npm install
npm run dev
```

ブラウザで [http://localhost:3000](http://localhost:3000) を開きます。

---

## 📡 APIエンドポイント

| メソッド | パス | 説明 |
|---------|------|------|
| `GET` | `/health` | ヘルスチェック |
| `GET` | `/api/timeseries` | 時系列データ取得 |
| `GET` | `/api/geo/activity` | 地理的活動データ取得 |

**クエリパラメータ（`/api/timeseries`）**

| パラメータ | デフォルト | 説明 |
|-----------|----------|------|
| `metric` | `mfg_index` | `mfg_index` または `orders` |
| `frequency` | `weekly` | `weekly` または `daily` |

---

## 🛣️ 今後の開発ロードマップ

- [ ] 衛星夜間光データ（VIIRS/DMSP）の実データ接続
- [ ] 船舶AISデータの取り込みと活動量指標化
- [ ] `evidence` / `drivers` フィールドの実装（変動根拠の自動生成）
- [ ] 外部DBへの接続切替（PostgreSQL）
- [ ] 認証機能の追加

---

## ⚠️ セキュリティに関する注意

`.streamlit/secrets.toml` にはDB接続情報が含まれています。  
**必ず `.gitignore` に追加し、リポジトリに含めないようにしてください。**

```gitignore
# .gitignore に追加
.streamlit/secrets.toml
*.db
.env
venv/
__pycache__/
.next/
```

---

## 🔧 技術スタック

**フロントエンド**
- [Next.js 14](https://nextjs.org/) (App Router)
- TypeScript
- [Tailwind CSS](https://tailwindcss.com/)
- [Recharts](https://recharts.org/) — グラフ描画
- [React Leaflet](https://react-leaflet.js.org/) — 地図表示
- [SWR](https://swr.vercel.app/) — データフェッチ

**バックエンド**
- [FastAPI](https://fastapi.tiangolo.com/)
- Python / Pydantic

---

## 📝 ライセンス

研究・学習目的のプロトタイプです。