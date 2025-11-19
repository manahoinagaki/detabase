import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3 
import numpy as np 
import os 
import plotly.express as px

# --- 1. データベース設定関数 (SQLiteテストデータ作成) ---
def setup_database():
    """SQLiteデータベースを作成し、地理情報付きのダミーデータを挿入する。"""
    db_name = 'sales_data.db' 
    
    # ファイルが既に存在する場合は削除
    if os.path.exists(db_name):
        os.remove(db_name)
        
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # テーブル作成: 地理情報 (latitude, longitude, region_name) を追加
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS monthly_sales ( 
            month TEXT,
            revenue INTEGER,
            products_sold INTEGER,
            latitude REAL,       
            longitude REAL,      
            region_name TEXT     
        )
    ''')
    
    # 夜間光データに見立てたダミーデータを挿入 (緯度・経度を含む)
    # 緯度, 経度, 地域名, 月, 売上(輝度), 製品数
    data = [ 
        ('1月', 15000, 150, 35.6895, 139.6917, '東京'),
        ('2月', 22000, 180, 34.6937, 135.5023, '大阪'),
        ('3月', 18000, 160, 33.5904, 130.4017, '福岡'),
        ('4月', 25000, 210, 34.3963, 132.4594, '広島'),
        ('5月', 30000, 250, 35.1815, 136.9066, '名古屋'),
        ('1月', 12000, 100, 34.6937, 135.5023, '大阪'), # 時系列データのために大阪の1月を追加
    ]
    cursor.executemany('INSERT INTO monthly_sales VALUES (?, ?, ?, ?, ?, ?)', data)
    conn.commit()
    conn.close()
    
    return db_name

# --- 2. データ取得関数 (SQLite専用) ---
@st.cache(allow_output_mutation=True)
def get_data():
    """SQLiteデータベースからデータを取得し、Pandas DataFrameとして返す"""
    
    conn = None 
    df = pd.DataFrame() # 戻り値のDataFrameを初期化
    
    # 1. SQLiteテストDBの作成と接続
    DB_FILE = setup_database()
    
    try:
        conn = sqlite3.connect(DB_FILE)
        # 地理情報を含むすべての列を取得
        sql_query = "SELECT month, revenue, products_sold, latitude, longitude, region_name FROM monthly_sales"
        df = pd.read_sql_query(sql_query, conn)
    except Exception as e:
        st.error(f"SQLiteデータ取得中にエラーが発生しました: {e}")
    finally:
        if conn:
            conn.close()
            
    return df

# --- 3. アプリのメインロジック ---
def main():
    st.set_page_config(layout="wide") # 画面を広く使う
    st.title("🛰️ 夜間光データ分析ダッシュボード")
    
    # データベースのセットアップとデータ取得
    df = get_data() 
    
    if df.empty:
        st.error("データソースへの接続に失敗しました。アプリを再起動してください。")
        return
    
    # --- 共通の列オプションを定義 (フィルタリング前) ---
    # 注: X軸の選択肢として使用するため、フィルタリング前に定義するのが安全です。
    column_options = df.columns.tolist()
    
    # --- サイドバー設定とフィルタリング ---
    all_months = df['month'].unique().tolist() 
    all_regions = df['region_name'].unique().tolist()
    
    st.sidebar.header("設定とフィルタ")
    
    # --- 0. 期間フィルタリング ---
    selected_months = st.sidebar.multiselect( 
        "0. 表示する期間（月）を選択",
        all_months,
        default=all_months
    )
    
    if not selected_months:
        st.warning("表示する月を選択してください。")
        return
    
    # 期間でフィルタリング
    df_filtered = df[df['month'].isin(selected_months)].copy()
    
    # --- C. 数値列の抽出（フィルタリング後に実行）---
    # numeric_cols と column_options (フィルタ後の列) を定義し直す
    numeric_cols = df_filtered.select_dtypes(include=np.number).columns.tolist()
    # column_options = df_filtered.columns.tolist() # X軸はフィルタ前のオプションを使っても良いが、ここではフィルタ後の列名を使うのが一般的
    
    # --- A. グラフの種類選択 (地図は固定) ---
    chart_type_options = ["折れ線グラフ", "棒グラフ", "散布図", "複合グラフ", "ヒストグラム", "円グラフ"]
    chart_type = st.sidebar.selectbox(
        "1. 時系列・分布グラフの種類を選択",
        chart_type_options
    )

    # --- B. 地域検索/選択 (地図連動用) ---
    selected_region = st.sidebar.selectbox(
        "2. 詳細分析する地域を選択",
        options=['すべて'] + all_regions
    )
    
    # --- 数値列の抽出（ヒストグラム/円グラフの選択肢を制限するため） ---
    numeric_cols = df_filtered.select_dtypes(include=np.number).columns.tolist()
    column_options = df_filtered.columns.tolist()

    # --- C'. X軸/カテゴリの選択 --- (定義済み column_options を使用)
    x_column = st.sidebar.selectbox(
        "2. X軸 (カテゴリ/時系列) のデータを選択",
        column_options, # <-- ここで column_options が確実に定義されている
        index=0 
    )

    # --- C. Y軸/値の選択 (グラフの種類に応じて制御) ---
    # 地図以外のグラフで使うY軸の選択
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
        y_columns = st.sidebar.multiselect( 
            f"3. Y軸 (値) のデータを選択 (1つのみ)",
            numeric_cols, # 数値列のみを使用
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
    
    # --- D. グラフ描画実行前のチェック ---
    if not y_columns:
        st.warning("Y軸にデータを選択してください。")
        return
    
    # --- データの準備 ---
    df_map = df_filtered.copy()
    
    # --- メイン画面 ---
    
    # --- 4. 地図の描画 (メイン画面 - 地図は固定配置) ---
    st.header("💡 地域別 夜間光強度マップ")
    
    # Plotly Expressでインタラクティブな散布図マップを生成
    # 
    fig_map = px.scatter_mapbox(
        df_map, 
        lat="latitude", 
        lon="longitude", 
        color="revenue", # 輝度を 'revenue' (売上) の値に見立てて色とサイズに反映
        size="revenue", 
        hover_name="region_name", 
        color_continuous_scale=px.colors.sequential.Plasma,
        zoom=3.5, 
        height=500,
        title=f"夜間光データの地理的分布 ({', '.join(selected_months)})"
    )
    
    fig_map.update_layout(mapbox_style="carto-positron")
    fig_map.update_layout(margin={"r":0,"t":20,"l":0,"b":0})
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    # --- 5. 連動した時系列/分布グラフの表示 (地図の下に配置) ---
    
    # --- ヒストグラムのスライダー設定 ---
    bins = 10
    if chart_type == "ヒストグラム":
        max_bins = len(df_filtered[y_columns[0]].unique())
        bins = st.sidebar.slider(
            "4. ビン数 (Bins) を選択",
            min_value=1,
            max_value=max_bins if max_bins >= 1 else 1,
            value=min(10, max_bins if max_bins >= 1 else 1)
        )
    
    st.header(f"📈 {selected_region} のデータ分析 ({chart_type})")
    
    # Matplotlib Figureの初期化とサイズ調整
    if chart_type == "円グラフ":
        fig, ax1 = plt.subplots(figsize=(8, 8))
    else:
        fig, ax1 = plt.subplots(figsize=(10, 5)) 

    # --- データ準備: 選択地域のみを抽出 (グラフ用) ---
    if selected_region != 'すべて':
        df_chart = df_filtered[df_filtered['region_name'] == selected_region].copy()
    else:
        # 'すべて' の場合、複数の地域のデータが混在しているため、そのまま使用
        df_chart = df_filtered.copy()


    # --- グラフ描画ロジック ---

    if chart_type == "複合グラフ" and len(y_columns) == 2:
        ax2 = ax1.twinx() 
        ax1.bar(df_chart[x_column], df_chart[y_columns[0]], color='skyblue', label=y_columns[0], alpha=0.6)
        ax1.set_ylabel(y_columns[0], color='skyblue')
        ax1.tick_params(axis='y', labelcolor='skyblue')
        ax2.plot(df_chart[x_column], df_chart[y_columns[1]], marker='o', color='red', label=y_columns[1])
        ax2.set_ylabel(y_columns[1], color='red')
        ax2.tick_params(axis='y', labelcolor='red')
        ax1.set_title(f"複合グラフ: {y_columns[0]} と {y_columns[1]} の比較")

    elif chart_type == "ヒストグラム":
        ax1.hist(df_chart[y_columns[0]], bins=bins, color='orange', edgecolor='black') 
        ax1.set_title(f"{y_columns[0]} の分布")

    elif chart_type == "円グラフ":
        labels = df_chart[x_column]
        sizes = df_chart[y_columns[0]]
        explode = tuple([0.1] + [0] * (len(sizes) - 1))
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax1.axis('equal') 
        ax1.set_title(f"{y_columns[0]} の内訳 ({x_column}別)")

    else:
        # 単純な単軸グラフ (Line, Scatter, Bar)
        for col in y_columns:
            if chart_type == "折れ線グラフ":
                ax1.plot(df_chart[x_column], df_chart[col], marker='o', label=col)
            elif chart_type == "散布図":
                ax1.scatter(df_chart[x_column], df_chart[col], label=f'{col} vs {x_column}')
            elif chart_type == "棒グラフ":
                 ax1.bar(df_chart[x_column], df_chart[col], label=col, color='skyblue')

        ax1.set_title(f"{chart_type} of {', '.join(y_columns)} by {x_column}")
        
    # すべてのグラフに共通の軸ラベル、凡例、グリッド設定
    ax1.set_xlabel(x_column)
    ax1.set_ylabel(", ".join(y_columns))
    ax1.legend(title="データ系列")
    ax1.grid(axis='y', linestyle='--')
    
    # グラフの表示
    st.pyplot(fig)
    
    st.subheader("全データテーブル")
    st.dataframe(df_filtered)


if __name__ == "__main__":
    main()