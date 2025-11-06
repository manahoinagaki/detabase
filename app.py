import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import numpy as np

# --- 1. データベース設定関数 (以前のコードから流用) ---
# ここに setup_database 関数（SQLite接続とダミーデータ作成）を定義します。
def setup_database():
    # ... (前回のsetup_database関数の内容をそのままここに貼り付け) ...
    db_name = 'sales_data.db'
    
    # 既存ファイルの削除と再作成
    if os.path.exists(db_name):
        os.remove(db_name)
        
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monthly_sales (
            month TEXT,
            revenue INTEGER,
            products_sold INTEGER
        )
    ''')
    
    data = [
        ('Jan', 15000, 150),
        ('Feb', 22000, 180),
        ('Mar', 18000, 160),
        ('Apr', 25000, 210),
        ('May', 30000, 250)
    ]
    cursor.executemany('INSERT INTO monthly_sales VALUES (?, ?, ?)', data)
    conn.commit()
    conn.close()
    
    return db_name

# --- 2. データ取得関数 ---
@st.cache_data
def get_data(db_file):
    """データベースからデータを取得し、Pandas DataFrameとして返す"""
    conn = sqlite3.connect(db_file)
    # すべてのデータを取得
    df = pd.read_sql_query("SELECT * FROM monthly_sales", conn)
    conn.close()
    return df

# --- 3. アプリのメインロジック ---
def main():
    st.title("📊 SQLデータ可視化アプリ (Streamlit)")
    
    # データベースのセットアップとデータ取得
    DB_FILE = setup_database()
    df = get_data(DB_FILE)
    
    # データフレームを表示（オプション）
    st.subheader("取得データ（Pandas DataFrame）")
    st.dataframe(df)

    st.sidebar.header("設定")
    
    # --- A. グラフの種類選択 (最優先事項) ---
    chart_type = st.sidebar.selectbox(
        "1. グラフの種類を選択してください",
        ["折れ線グラフ (Line)", "棒グラフ (Bar)", "散布図 (Scatter)"]
    )
    
    # 軸の選択肢として、DataFrameの列名（month, revenue, products_sold）を使用
    column_options = df.columns.tolist() 

    # --- B. X軸/カテゴリの選択 ---
    x_column = st.sidebar.selectbox(
        "2. X軸 (カテゴリ/時系列) のデータを選択",
        column_options,
        index=0 # デフォルトで 'month' を選択
    )
    
    # --- C. Y軸/値の選択 (複数選択を可能にする) ---
    y_columns = st.sidebar.multiselect(
        "3. Y軸 (値) のデータを選択 (複数選択可)",
        column_options,
        default=['revenue'] # デフォルトで 'revenue' を選択
    )
    
    # --- D. グラフ描画 ---
    if not y_columns:
        st.warning("Y軸にデータを選択してください。")
        return

    st.subheader(f"{chart_type} の結果")

    # MatplotlibのFigureを生成
    fig, ax = plt.subplots(figsize=(10, 5))
    
    for col in y_columns:
        if chart_type == "折れ線グラフ (Line)":
            ax.plot(df[x_column], df[col], marker='o', label=col)
        elif chart_type == "棒グラフ (Bar)":
            # 棒グラフは複数系列を並べる（または積み上げる）工夫が必要だが、ここではシンプルに並べる
            width = 0.8 / len(y_columns)
            offset = [i * width - (len(y_columns) - 1) * width / 2 for i in range(len(y_columns))]
            
            # 棒グラフの描画を一旦シンプルにするため、Y軸が単一の場合のみ実行
            if len(y_columns) == 1:
                 ax.bar(df[x_column], df[col], label=col, color='skyblue')
            else:
                 # 複数棒グラフの描画は複雑なので、一旦警告を出すか、最初の1つだけ描画する
                 st.warning("複数データでの棒グラフ描画は、現在サポートされていません。一つだけ選択してください。")
                 ax.bar(df[x_column], df[y_columns[0]], label=y_columns[0], color='skyblue')
                 break
                 
        elif chart_type == "散布図 (Scatter)":
            ax.scatter(df[x_column], df[col], label=f'{col} vs {x_column}')

    ax.set_title(f"{chart_type} of {', '.join(y_columns)} by {x_column}")
    ax.set_xlabel(x_column)
    ax.set_ylabel(", ".join(y_columns))
    ax.legend(title="データ系列")
    ax.grid(axis='y', linestyle='--')
    
    # StreamlitでMatplotlibのFigureを表示
    st.pyplot(fig)

if __name__ == "__main__":
    import os
    main()