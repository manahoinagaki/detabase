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
    
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS monthly_sales ( 
            month TEXT,
            revenue INTEGER,
            products_sold INTEGER
        )
    ''')
    # テーブル作成SQL文の実行
    
    data = [ #テーブルに挿入する実際のデータ（タプルのリスト）
        ('1月', 15000, 150),
        ('2月', 22000, 180),
        ('3月', 18000, 160),
        ('4月', 25000, 210),
        ('5月', 30000, 250)
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
    
    # 接続オブジェクトを初期化
    conn = None
    
    try:
        conn = sqlite3.connect(db_file)  #SQLiteデータベースに接続
        df = pd.read_sql_query("SELECT * FROM monthly_sales", conn) 
        #SQLクエリを実行し、結果をPandasデータフレームに格納(全データ取得)


    except sqlite3.OperationalError as e:
        # データベース接続やクエリのエラーを捕捉
        st.error(f"データベースの操作エラーが発生しました: {e}")
        return pd.DataFrame() # 空のDataFrameを返す
    
    finally:
        # --- 終了処理ブロック (try/except の結果に関わらず実行) ---
        # 接続が確立されていた場合のみ、接続を閉じる
        if conn:
            conn.close()
            
            return df #データフレームを返す
 # 推奨: グラフ化に必要な列だけを取得したり、特定の条件で絞り込んだりするようにSQLクエリを変更できます（例: "SELECT month, revenue FROM monthly_sales WHERE revenue > 10000"）。

# --- 3. アプリのメインロジック ---
def main():
    st.title("SQLデータ可視化アプリ (Streamlit)") # アプリのタイトル表示
    
    # データベースのセットアップとデータ取得
    DB_FILE = setup_database()  #DB初期化
    df = get_data(DB_FILE)  #データ取得
    
    # エラーハンドリング: データ取得に失敗した場合
    if df.empty:
        return
    
    # --- フィルタリング機能のために、すべての月のリストを取得 ---
    all_months = df['month'].unique().tolist() #フィルタ選択肢準備 
    # df の month 列から、重複のないユニークな月名（"Jan", "Feb" など）を抽出し、リストとして保持
    
    st.subheader("取得データ（Pandas DataFrame）") 
    st.dataframe(df) #データ表示 全体をアプリのメイン画面に表示

    st.sidebar.header("設定")
    
    # --- 0. フィルタリング機能の追加 ---
    selected_months = st.sidebar.multiselect( #月の選択ウィジェット
                                            #  サイドバーに、all_months を選択肢とする複数選択ドロップダウンを
                                            # 表示。ユーザーの選択結果が selected_months に格納される。
        "0. 表示する月を選択 (フィルタリング)",
        all_months,
        default=all_months # デフォルトでは全ての月を選択
    )
    
    df_filtered = df[df['month'].isin(selected_months)] #データフィルタリング
    #df の month 列の値が、ユーザーが選んだ selected_months リストに含まれる行だけを抽出し、df_filtered として定義します。以降のグラフ描画ではこのフィルタ済みデータが使用されます。

    # 空の選択肢チェック
    if selected_months:
        df_filtered = df[df['month'].isin(selected_months)]
    else:
        st.warning("表示する月を選択してください。")
        return # 月が選択されていない場合は描画を中止
    
    # --- 数値列の抽出（ヒストグラム/円グラフの選択肢を制限するため） ---
    # 数値型の列（revenue, products_sold）だけを抽出します
    numeric_cols = df_filtered.select_dtypes(include=np.number).columns.tolist()
    
    # すべての列の選択肢
    column_options = df_filtered.columns.tolist()
    
     # st.title(...)	アプリタイトル表示	メイン画面の一番上にタイトルを表示します。
     # DB_FILE = setup_database()	DB初期化	テスト用のSQLiteファイルを作成/再作成し、そのファイル名を取得します。
     # df = get_data(DB_FILE)	データ取得	データベースに接続し、全てのデータをPandas DataFrame (df) として取得します。
     # all_months = df['month'].unique().tolist()	フィルタ選択肢準備	df の month 列から、重複のないユニークな月名（"Jan", "Feb" など）を抽出し、リストとして保持します。
     # st.dataframe(df)	データ表示	ユーザーにフィルタ前の元データ（DataFrame）全体をアプリのメイン画面に表示します。
     # st.sidebar.multiselect(...)	月の選択ウィジェット	サイドバーに、all_months を選択肢とする複数選択ドロップダウンを表示します。ユーザーの選択結果が selected_months に格納されます。
     # df_filtered = df[df['month'].isin(selected_months)]	データフィルタリング	df の month 列の値が、ユーザーが選んだ selected_months リストに含まれる行だけを抽出し、df_filtered として定義します。以降のグラフ描画ではこのフィルタ済みデータが使用されます。
     # if selected_months: ... else: return	空の選択肢チェック	ユーザーがすべての月の選択を解除した場合、st.warning を表示し、return で関数（アプリの実行）を中断します。これは、空のデータでグラフ描画処理に進むのを防ぐ、重要なガード処理です。
    
    # --- A. グラフの種類選択 (最優先事項) ---
    chart_type = st.sidebar.selectbox(
        "1. グラフの種類を選択してください",
        ["折れ線グラフ", "棒グラフ", "散布図", "複合グラフ", "ヒストグラム", "円グラフ"]
    )

    column_options = df.columns.tolist()

     # chart_type = ...	結果の変数	ユーザーが選択したグラフの種類（例: "棒グラフ"）が格納される最重要変数です。
     # st.sidebar.selectbox(...)	Streamlitウィジェット	Streamlitのサイドバーにドロップダウンリストを作成します。ユーザーはここから1つの項目を選択できます。
     # "1. グラフの種類を選択してください"	ラベル	サイドバーに表示されるウィジェットのタイトルです。
     # [...]	選択肢	ドロップダウンリストに表示される、利用可能なグラフの種類のリストです。
     # column_options = ...	列名のリスト	df.columns.tolist() によって、データフレームのすべての列名をリストとして取得します。このリストが、X軸・Y軸設定ウィジェットの選択肢として再利用されます。

    # --- B. X軸/カテゴリの選択 ---
    x_column = st.sidebar.selectbox(
        "2. X軸 (カテゴリ/時系列) のデータを選択",
        column_options,
        index=0 # デフォルトで 'month' を選択
    )
     # x_column = ...	結果の変数	ユーザーが選択したX軸の列名（文字列）が格納されます。グラフ描画ロジックの df[x_column] の部分で使用されます。
     # st.sidebar.selectbox(...)	Streamlitウィジェット	サイドバーにドロップダウンリストを作成します。これは st.multiselect と異なり、常に一つの選択肢のみを選ばせます。
     # "2. X軸 (カテゴリ/時系列) のデータを選択"	ラベル	サイドバーに表示されるウィジェットのタイトルです。
     # column_options	選択肢	前のステップで取得された、データフレームのすべての列名のリストです。
     # index=0	デフォルト値	ドロップダウンリストの最初の項目（今回のデータでは "month"）を初期状態で選択状態にします。
    
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
     # if chart_type == "..."	制御フロー	前のステップで選択されたグラフの種類（chart_type）に応じて、後の処理を分岐させます。
     # max_select	選択制限変数	Streamlitの max_selections パラメータに渡すための変数。グラフの種類によって、これが 2 または 1 に設定されます。
     # default_select	初期選択値	選択肢を初期状態で表示するためのリストです。複合グラフではrevenueとproducts_soldをデフォルトに設定するなど、ユーザー体験を向上させています。
     # st.sidebar.multiselect(...)	Streamlitウィジェット	Y軸の選択に使用されるウィジェットです。max_selectを設定することで、選択可能な最大数を制御しています。
     # y_columns	結果の変数	ユーザーが選択した1つまたは複数のY軸の列名（リスト）が格納されます。これがグラフの縦軸データになります。
    
    # --- D. グラフ描画 ---
    if not y_columns:
        st.warning("Y軸にデータを選択してください。")
        return
    
    # --- ビン数スライダーの追加 (ヒストグラムの場合のみ) ---
    bins = 10
    if chart_type == "ヒストグラム (Hist)":
        # データのユニークな値の数を上限とします
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
     #入力チェック: y_columns（ユーザーが選択したY軸のデータ列リスト）が空でないか確認します。
     # ガード節: y_columns が空の場合、警告を表示し、return によってこれ以降の描画処理をすべて中断します。これは、データがない状態で描画関数を実行し、エラーが発生するのを防ぐための必須の安全策（ガード節）です。
     # セクションヘッダー表示: アプリのメイン画面に、選択されたグラフの種類（例: "折れ線グラフ (Line) の結果"）をサブヘッダーとして表示し、グラフの表示エリアであることを示します。
     # Matplotlibの初期化とサイズ調整:
     # 円グラフ判定: chart_type が "円グラフ (Pie)" の場合、figsize=(8, 8) の正方形のキャンバスを作成します。これは、円グラフが歪まずに正円としてきれいに表示されるようにするためです。
     # その他のグラフ: それ以外のグラフ（棒、折れ線など）の場合は、figsize=(10, 5) の標準的な横長のキャンバスを作成します。
     # どちらの場合も、キャンバス全体を指す fig (Figure) と、描画領域を指す ax1 (Axis 1) という2つの主要なMatplotlibオブジェクトを準備します。
     
     # if not y_columns: ... return	ガード節 (必須)	Y軸データが選択されていない場合にアプリのクラッシュを防ぎ、ユーザーに操作を促すための安全機構です。
     # st.subheader(...)	Streamlit表示	グラフの上に表示される見出しです。f-stringで動的な情報（選択されたグラフの種類）を表示しています。
     # plt.subplots(...)	Matplotlib初期化	Matplotlibでグラフを描画するためのキャンバス（fig）と、座標系（ax1）を同時に作成する関数です。
     # figsize=(8, 8) / figsize=(10, 5)	サイズ調整	グラフがブラウザで表示される際のアスペクト比（縦横比）と基本サイズを指定しています。円グラフの場合は正方形が標準です。
     # fig, ax1	Matplotlibオブジェクト	fig はファイルとして保存したり、Streamlitに出力したりするオブジェクト。ax1 は実際に点や線、軸を描画していくためのオブジェクトです。
    
    
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

        ax1.set_title(f"複合グラフ: {y_columns[0]} と {y_columns[1]} の比較")
        ax1.set_xlabel(x_column)

        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines + lines2, labels + labels2, loc='upper left')
        ax1.grid(axis='y', linestyle='--')
        
         #目的: 異なる単位を持つ2つのデータ系列（例: 売上と製品数）を、一つのグラフに表示します。
         # ロジック:
         # ax2 = ax1.twinx() を使って、ax1 と X軸を共有し、Y軸を独立させた第2軸 (ax2) を作成します。
         # 最初のデータ (y_columns[0]) を ax1 に棒グラフ (ax1.bar) で描画し、軸を水色で装飾します。
         # 2番目のデータ (y_columns[1]) を ax2 に折れ線グラフ (ax2.plot) で描画し、軸を赤色で装飾します。
         # 凡例 (ax1.legend) は、両方の軸の情報を集めて統合し、グラフの判読性を高めています。

    elif chart_type == "ヒストグラム (Hist)":
        # ヒストグラム
        # 選択された bins 変数を使用
        ax1.hist(df_filtered[y_columns[0]], bins=bins, color='orange', edgecolor='black') 
        ax1.set_title(f"{y_columns[0]} の分布 (ヒストグラム)")
        ax1.set_xlabel(y_columns[0])
        ax1.set_ylabel("度数 (Frequency)")
        ax1.grid(axis='y', linestyle='--')
        
         # 目的: 選択された一つの数値データの度数分布を視覚化します。
         # ロジック: ax1.hist() 関数を使用します。bins=3 はデータ数に対して少なすぎる可能性があるため、より適切な値（例えば bins=len(df) や bins=10 など）に調整するのが望ましいです。

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
         # 目的: X軸（カテゴリ）に対するY軸（値）の比率を視覚化します。
         # ロジック: ax1.pie() 関数を使用します。
         # explode を使って最初の要素を少し飛び出させ、強調表示しています。
         # autopct='%1.1f%%' で、各スライスに**割合（パーセント）**を表示しています。
         # ax1.axis('equal') は、グラフが歪まずに正円として表示されるようにするために必須です。

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
        
         # 目的: 選択されたすべてのY軸データを、X軸を共有する単一の軸 (ax1) 上に重ねて表示します。
         # ロジック: for col in y_columns: ループを使い、選択されたすべてのデータ系列に対して、chart_type に応じた適切な描画関数（ax1.plot, ax1.scatter, ax1.bar）を呼び出します。
    
     # ax2 = ax1.twinx()	第2軸の作成	X軸を共有し、独立したY軸（右側）を追加します。複合グラフに必須です。
     # ax1.bar(...)	棒グラフ	X軸をカテゴリとし、Y軸の値を棒の長さとして描画します。
     # ax2.plot(...)	折れ線グラフ	X軸の推移に対するY軸の連続的な変化を描画します。
     # ax.tick_params(...)	軸の装飾	軸の目盛りやラベルの色をデータ系列の色と合わせることで、複合グラフの判読性を高めています。
     # ax1.hist(...)	ヒストグラム	データの分布を区間（ビン）ごとの度数で表示します。
     # ax1.pie(...)	円グラフ	値の合計に対する各要素の比率を扇形として表示します。
     
    # StreamlitでMatplotlibのFigureを表示 (最後に一度だけ実行)
    st.pyplot(fig)
    # st.pyplot(fig)	最終出力	作成したMatplotlibのFigureオブジェクト (fig) をStreamlitに渡し、ブラウザのアプリ画面に描画します。

if __name__ == "__main__":
    main()
     # 条件チェック: Pythonインタープリタは、スクリプトを実行するとき、特別な変数 __name__ に値を設定します。
     # スクリプトが直接実行された場合（例: python app.py）: __name__ は文字列 "__main__" になります。
     # スクリプトが別のファイルにインポートされた場合（例: import app）: __name__ はスクリプト名（この場合は "app"）になります。
     # アプリの起動: この if 文により、app.py が直接起動されたときにのみ、アプリの全ロジックを含む main() 関数が呼び出され、Streamlitアプリが開始されます。
     # これは、テストやライブラリとしての再利用の際に、意図しないアプリの起動を防ぐための、Pythonにおける標準的なベストプラクティスです。
    
     # if __name__ == "__main__":	エントリーポイントの定義	「このファイルがメインとして実行されている場合のみ、次のブロックを実行せよ」という条件文です。
     # __name__	特殊変数	現在のモジュールの名前を格納するPythonの組み込み変数です。
     # "__main__"	メイン実行の識別子	スクリプトが直接実行されたことを示す特別な値です。
     # main()	メインロジックの呼び出し	複合グラフ、フィルタリング、UI設定など、アプリ全体を定義する関数を実行します。