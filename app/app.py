import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3 
import numpy as np 
import os 
# import psycopg2 # PostgreSQLは使用しないため削除済み

# --- 1. データベース設定関数 (SQLiteテストデータ作成) ---
def setup_database():
    """SQLiteデータベースを作成し、夜間光データのダミーデータを挿入する。"""
    db_name = 'sales_data.db' 
    
    if os.path.exists(db_name):
        os.remove(db_name)
        
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # テーブル作成
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS monthly_sales ( 
            month TEXT,
            revenue INTEGER,
            products_sold INTEGER
        )
    ''')
    
   # 緯度, 経度, 地域名, 月, 売上, 製品数
data = [
    (35.6895, 139.6917, '東京', '1月', 15000, 150),
    (34.6937, 135.5023, '大阪', '2月', 22000, 180),
    (33.5904, 130.4017, '福岡', '3月', 18000, 160),
    (34.3963, 132.4594, '広島', '4月', 25000, 210),
    (35.1815, 136.9066, '名古屋', '5月', 30000, 250)
]
cursor.executemany('INSERT INTO monthly_sales VALUES (?, ?, ?, ?, ?, ?)', data)
    conn.close()
    
    return db_name

# --- 2. データ取得関数 (SQLite専用) ---
@st.cache_data 
def get_data():
    """SQLiteデータベースからデータを取得し、Pandas DataFrameとして返す"""
    
    conn = None 
    df = pd.DataFrame() # 戻り値のDataFrameを初期化
    
    # 1. SQLiteテストDBの作成と接続
    DB_FILE = setup_database()
    
    try:
        conn = sqlite3.connect(DB_FILE)
        sql_query = "SELECT month, revenue, products_sold FROM monthly_sales"
        df = pd.read_sql_query(sql_query, conn)
    except Exception as e:
        st.error(f"SQLiteデータ取得中にエラーが発生しました: {e}")
        # エラー時は空のDataFrameが返される
    finally:
        if conn:
            conn.close()
            
    return df

# --- 3. アプリのメインロジック ---
def main():
    st.title("💡 衛星データ可視化ダッシュボード (SQLite版)")
    
    # データベースのセットアップとデータ取得
    df = get_data() 
    
    # エラーハンドリング: データ取得に失敗した場合 (空のDataFrameが返された場合)
    if df.empty:
        st.error("データソースへの接続に失敗しました。アプリを再起動してください。")
        return
    
    # --- フィルタリング機能のために、すべての月のリストを取得 ---
    all_months = df['month'].unique().tolist() 
    
    st.subheader("取得データ（発展度分析用）") 
    st.dataframe(df)

    st.sidebar.header("設定とフィルタ")
    
    # --- 0. フィルタリング機能の追加 ---
    selected_months = st.sidebar.multiselect( 
        "0. 表示する期間（月）を選択",
        all_months,
        default=all_months # デフォルトでは全ての月を選択
    )
    
    # 選択された月でデータフレームをフィルタリングする
    if not selected_months:
        st.warning("表示する月を選択してください。")
        return
    
    df_filtered = df[df['month'].isin(selected_months)] 

    # --- 数値列の抽出（ヒストグラム/円グラフの選択肢を制限するため） ---
    numeric_cols = df_filtered.select_dtypes(include=np.number).columns.tolist()
    column_options = df_filtered.columns.tolist()

    # --- A. グラフの種類選択 (最優先事項) ---
    chart_type = st.sidebar.selectbox(
        "1. グラフの種類を選択してください",
        ["折れ線グラフ", "棒グラフ", "散布図", "複合グラフ", "ヒストグラム", "円グラフ"]
    )

    # --- B. X軸/カテゴリの選択 ---
    x_column = st.sidebar.selectbox(
        "2. X軸 (カテゴリ/時系列) のデータを選択",
        column_options,
        index=0 # デフォルトで 'month' を選択
    )
    
    # --- C. Y軸/値の選択 (グラフの種類に応じて制御) ---
    if chart_type == "複合グラフ":
        max_select = 2
        default_select = ['revenue', 'products_sold']
        y_columns = st.sidebar.multiselect(
            "3. Y軸 (値) のデータを選択 (必ず2つ選択してください)",
            column_options,
            default=default_select,
            max_selections=max_select
        )
    elif chart_type in ["ヒストグラム", "円グラフ"]:
        max_select = 1
        default_select = ['revenue'] if 'revenue' in numeric_cols else numeric_cols[:1]
        
        # 選択肢を数値列のみに制限します
        y_columns = st.sidebar.multiselect( 
            f"3. Y軸 (値) のデータを選択 (1つのみ)",
            numeric_cols, # <-- 数値列のみを使用
            default=default_select,
            max_selections=max_select
        )
    else:
        # その他 (Line, Bar, Scatter) は複数選択を許可
        y_columns = st.sidebar.multiselect(
            "3. Y軸 (値) のデータを選択 (複数選択可)",
            column_options,
            default=['revenue']
        )
    
    # --- D. グラフ描画 ---
    if not y_columns:
        st.warning("Y軸にデータを選択してください。")
        return
    
    # --- ビン数スライダーの追加 (ヒストグラムの場合のみ) ---
    bins = 10
    if chart_type == "ヒストグラム":
        max_bins = len(df_filtered[y_columns[0]].unique())
        bins = st.sidebar.slider(
            "4. ビン数 (Bins) を選択",
            min_value=1,
            max_value=max_bins if max_bins >= 1 else 1,
            value=min(10, max_bins if max_bins >= 1 else 1)
        )

    st.subheader(f"{chart_type} の結果")

    # Matplotlib Figureの初期化とサイズ調整
    if chart_type == "円グラフ":
        fig, ax1 = plt.subplots(figsize=(8, 8))
    else:
        fig, ax1 = plt.subplots(figsize=(10, 5)) 

    # --- グラフの種類ごとのロジック ---

    if chart_type == "複合グラフ" and len(y_columns) == 2:
        # 複合グラフ (棒 + 折れ線)
        ax2 = ax1.twinx() 
        
        ax1.bar(df_filtered[x_column], df_filtered[y_columns[0]], color='skyblue', label=y_columns[0], alpha=0.6)
        ax1.set_ylabel(y_columns[0], color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue')
        
        ax2.plot(df_filtered[x_column], df_filtered[y_columns[1]], marker='o', color='red', label=y_columns[1])
        ax2.set_ylabel(y_columns[1], color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        ax1.set_title(f"複合グラフ: {y_columns[0]} と {y_columns[1]} の比較 (夜間光データ分析)")
        ax1.set_xlabel(x_column)

        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines + lines2, labels + labels2, loc='upper left')
        ax1.grid(axis='y', linestyle='--')

    elif chart_type == "ヒストグラム":
        # ヒストグラム
        ax1.hist(df_filtered[y_columns[0]], bins=bins, color='orange', edgecolor='black') 
        ax1.set_title(f"{y_columns[0]} の分布 (ヒストグラム)")
        ax1.set_xlabel(y_columns[0])
        ax1.set_ylabel("度数 (Frequency)")
        ax1.grid(axis='y', linestyle='--')

    elif chart_type == "円グラフ":
        # 円グラフ
        labels = df_filtered[x_column]
        sizes = df_filtered[y_columns[0]]
        explode = tuple([0.1] + [0] * (len(sizes) - 1))

        ax1.pie(
            sizes, 
            explode=explode, 
            labels=labels, 
            autopct='%1.1f%%',
            shadow=True, 
            startangle=90
        )
        ax1.axis('equal') 
        ax1.set_title(f"{y_columns[0]} の内訳 ({x_column}別)")

    else:
        # 単純な単軸グラフ (Line, Scatter, Bar)
        for col in y_columns:
            if chart_type == "折れ線グラフ":
                ax1.plot(df_filtered[x_column], df_filtered[col], marker='o', label=col)
            elif chart_type == "散布図":
                ax1.scatter(df_filtered[x_column], df_filtered[col], label=f'{col} vs {x_column}')
            elif chart_type == "棒グラフ":
                 ax1.bar(df_filtered[x_column], df_filtered[col], label=col, color='skyblue')

        ax1.set_title(f"{chart_type} of {', '.join(y_columns)} by {x_column}")
        ax1.set_xlabel(x_column)
        ax1.set_ylabel(", ".join(y_columns))
        ax1.legend(title="データ系列")
        ax1.grid(axis='y', linestyle='--')
    
    # StreamlitでMatplotlibのFigureを表示 (最後に一度だけ実行)
    st.pyplot(fig)

if __name__ == "__main__":
    main()