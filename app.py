import streamlit as st # Streamlitライブラリをインポート
import matplotlib.pyplot as plt # グラフ描画に使用
import pandas as pd # データ操作に使用
import sqlite3  # SQLiteデータベース操作に使用
import numpy as np  # 数値計算に使用 (重複を削除)
import os # ファイル操作に使用 (ここに追加)

# --- 1. データベース設定関数 ---
def setup_database():# SQLiteデータベースを作成し、ダミーデータを挿入する。
    
    db_name = 'sales_data.db' #作成するSQLiteファイル名の定義
    
    if os.path.exists(db_name): #osモジュールを使って、指定したファイル名が既に存在するかのチェック。
        os.remove(db_name) #既存のファイルを削除
        
    conn = sqlite3.connect(db_name) #SQLiteデータベースに接続, 新規作成
    cursor = conn.cursor() #カーソルオブジェクトを作成
    
    cursor.execute('''  # テーブル作成SQL文の実行
        CREATE TABLE IF NOT EXISTS monthly_sales ( 
            month TEXT,
            revenue INTEGER,
            products_sold INTEGER
        )
    ''')
    
    data = [ #テーブルに挿入する実際のデータ（タプルのリスト）
        ('Jan', 15000, 150),
        ('Feb', 22000, 180),
        ('Mar', 18000, 160),
        ('Apr', 25000, 210),
        ('May', 30000, 250)
    ]
    cursor.executemany('INSERT INTO monthly_sales VALUES (?, ?, ?)', data)
    #複数のレコードを一度にテーブルへ挿入するSQL文を実行
    conn.commit() #挿入したデータをデータベースファイルに永続的に保存（コミット）します。
    conn.close() #データベース接続を閉じます。
    
    return db_name #作成したデータベースファイル名を返す

# --- 2. データ取得関数 ---
@st.cache_data # Streamlitのキャッシュデコレーターを使用して、データ取得を効率化
def get_data(db_file): #データベースファイル名を引数に取る
    """データベースからデータを取得し、Pandas DataFrameとして返す"""
    conn = sqlite3.connect(db_file) #SQLiteデータベースに接続
    df = pd.read_sql_query("SELECT * FROM monthly_sales", conn) 
    #SQLクエリを実行し、結果をPandasデータフレームに格納(全データ取得)
    conn.close() #接続を閉じる
    return df #データフレームを返す
# 推奨: グラフ化に必要な列だけを取得したり、特定の条件で絞り込んだりするようにSQLクエリを変更できます（例: "SELECT month, revenue FROM monthly_sales WHERE revenue > 10000"）。

# --- 3. アプリのメインロジック ---
def main():
    st.title("📊 SQLデータ可視化アプリ (Streamlit)")
    
    # データベースのセットアップとデータ取得
    DB_FILE = setup_database()
    df = get_data(DB_FILE)
    
    # --- フィルタリング機能のために、すべての月のリストを取得 ---
    all_months = df['month'].unique().tolist()
    
    st.subheader("取得データ（Pandas DataFrame）")
    st.dataframe(df)

    st.sidebar.header("設定")
    
    # --- 0. フィルタリング機能の追加 ---
    selected_months = st.sidebar.multiselect(
        "0. 表示する月を選択 (フィルタリング)",
        all_months,
        default=all_months # デフォルトでは全ての月を選択
    )

    # 選択された月でデータフレームをフィルタリングする
    if selected_months:
        df_filtered = df[df['month'].isin(selected_months)]
    else:
        st.warning("表示する月を選択してください。")
        return # 月が選択されていない場合は描画を中止
    
    # --- A. グラフの種類選択 (最優先事項) ---
    chart_type = st.sidebar.selectbox(
        "1. グラフの種類を選択してください",
        ["折れ線グラフ (Line)", "棒グラフ (Bar)", "散布図 (Scatter)", 
         "複合グラフ (Bar + Line)", "ヒストグラム (Hist)", "円グラフ (Pie)"]
    )
    
    column_options = df.columns.tolist() 

    # --- B. X軸/カテゴリの選択 ---
    x_column = st.sidebar.selectbox(
        "2. X軸 (カテゴリ/時系列) のデータを選択",
        column_options,
        index=0 # デフォルトで 'month' を選択
    )
    
    # --- C. Y軸/値の選択 (グラフの種類に応じて制御) ---
    if chart_type == "複合グラフ (Bar + Line)":
        max_select = 2
        default_select = ['revenue', 'products_sold']
        y_columns = st.sidebar.multiselect(
            "3. Y軸 (値) のデータを選択 (必ず2つ選択してください)",
            column_options,
            default=default_select,
            max_selections=max_select
        )
    elif chart_type in ["ヒストグラム (Hist)", "円グラフ (Pie)"]:
        max_select = 1
        default_select = ['revenue'] if chart_type == "ヒストグラム (Hist)" else ['revenue']
        y_columns = st.sidebar.multiselect(
            f"3. Y軸 (値) のデータを選択 (1つのみ)",
            column_options,
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

    st.subheader(f"{chart_type} の結果")

    # Matplotlib Figureの初期化とサイズ調整
    if chart_type == "円グラフ (Pie)":
        fig, ax1 = plt.subplots(figsize=(8, 8))
    else:
        fig, ax1 = plt.subplots(figsize=(10, 5)) 

    # --- グラフの種類ごとのロジック ---

    if chart_type == "複合グラフ (Bar + Line)" and len(y_columns) == 2:
        # 複合グラフ (棒 + 折れ線)
        ax2 = ax1.twinx() 
        
        ax1.bar(df[x_column], df[y_columns[0]], color='skyblue', label=y_columns[0], alpha=0.6)
        ax1.set_ylabel(y_columns[0], color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue')
        
        ax2.plot(df[x_column], df[y_columns[1]], marker='o', color='red', label=y_columns[1])
        ax2.set_ylabel(y_columns[1], color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        ax1.set_title(f"複合グラフ: {y_columns[0]} と {y_columns[1]} の比較")
        ax1.set_xlabel(x_column)

        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines + lines2, labels + labels2, loc='upper left')
        ax1.grid(axis='y', linestyle='--')

    elif chart_type == "ヒストグラム (Hist)":
        # ヒストグラム
        ax1.hist(df[y_columns[0]], bins=3, color='orange', edgecolor='black')
        ax1.set_title(f"{y_columns[0]} の分布 (ヒストグラム)")
        ax1.set_xlabel(y_columns[0])
        ax1.set_ylabel("度数 (Frequency)")
        ax1.grid(axis='y', linestyle='--')

    elif chart_type == "円グラフ (Pie)":
        # 円グラフ
        labels = df[x_column]
        sizes = df[y_columns[0]]
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
            if chart_type == "折れ線グラフ (Line)":
                ax1.plot(df[x_column], df[col], marker='o', label=col)
            elif chart_type == "散布図 (Scatter)":
                ax1.scatter(df[x_column], df[col], label=f'{col} vs {x_column}')
            elif chart_type == "棒グラフ (Bar)":
                 ax1.bar(df[x_column], df[col], label=col, color='skyblue')
                 
        ax1.set_title(f"{chart_type} of {', '.join(y_columns)} by {x_column}")
        ax1.set_xlabel(x_column)
        ax1.set_ylabel(", ".join(y_columns))
        ax1.legend(title="データ系列")
        ax1.grid(axis='y', linestyle='--')
    
    # StreamlitでMatplotlibのFigureを表示 (最後に一度だけ実行)
    st.pyplot(fig)

if __name__ == "__main__":
    main()