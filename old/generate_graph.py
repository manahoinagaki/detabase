# /workspaces/detabase/matplotlib.py

# 1. ライブラリのインポート
import matplotlib.pyplot as plt # グラフ描画に使用
import numpy as np # 数値計算に使用
import io # メモリ上のバイナリデータ操作に使用
import base64 # Base64エンコードに使用
import sqlite3 # SQLiteデータベース操作に使用
import pandas as pd # データ操作に使用
import numpy as np # 例のデータ生成に使用
import os # ファイル操作に使用

# 簡単なSQLiteデータベースを作成・接続する関数 (テスト用)
def setup_database():
    # データベースファイル名を指定
    db_name = 'sales_data.db'
    
    # ファイルが既に存在する場合は削除して再作成
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
    
    # ダミーデータを挿入
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

# データベースをセットアップ
DB_FILE = setup_database()

# SQLiteデータベースに接続
conn = sqlite3.connect(DB_FILE)

# SQLクエリの定義
sql_query = "SELECT month, revenue FROM monthly_sales ORDER BY month"

# クエリを実行し、結果をPandasデータフレームに格納
df = pd.read_sql_query(sql_query, conn)

# 接続を閉じる
conn.close()

# データフレームの確認（オプション）
# print(df)

# 2. データの準備

# # 円グラフの例
# sizes = [30, 25, 20, 25] # 四半期ごとの売上貢献度
# labels = ['Q1', 'Q2', 'Q3', 'Q4'] # 各要素のラベル
# explode = (0.1, 0, 0, 0) # Q1を少し目立たせる（オプション）
# colors = ['lightcoral', 'gold', 'lightskyblue', 'lightgreen']

# # ヒストグラムの例
# data_scores = np.random.normal(loc=70, scale=10, size=500) # 500人の従業員の評価スコア（正規分布に従う乱数を想定）
# # loc: 平均値 (70), scale: 標準偏差 (10), size: データ数 (500)

# # 散布図の例
# x_data = np.random.rand(50) * 10 #（X軸）：ランダムなデータ
# y_data = x_data * 2 + np.random.randn(50) * 5 + 10 #（Y軸）：広告費と弱い正の相関を持たせる

# # 棒グラフの例
# categories = ['Marketing', 'Sales', 'Development', 'HR'] # 部署（カテゴリ）
# hours = [45, 52, 60, 38] # 各部署の平均作業時間
# x_pos = np.arange(len(categories)) # X軸として使用するためにカテゴリのインデックスを作成

# # 折れ線グラフの例
# x = np.linspace(-2 * np.pi, 2 * np.pi, 100) # -2πから2πまでの等間隔な100個のデータを作成
# y = np.sin(x) # 対応するy軸のデータとしてsin関数を計算


# 3. グラフの描画
fig, ax = plt.subplots() # FigureとAxesを同時に作成する

# # 円グラフを描画 (plt.pie を使用)
# # Figureのサイズを調整して、円形が歪まないようにすることが一般的
# fig, ax = plt.subplots(figsize=(8, 8))
# ax.pie(
#     sizes, 
#     explode=explode, 
#     labels=labels, 
#     colors=colors,
#     # autopct: 割合をパーセント表示 ('%1.1f%%' は小数点以下1桁表示)
#     autopct='%1.1f%%',
#     shadow=True, 
#     startangle=90
# )
# # 円が正円になるように調整
# ax.axis('equal') 
# ax.set_title('Quarterly Sales Contribution')

# # ヒストグラムを描画 (plt.hist を使用)
# # bins=15: データを15個の区間（ビン）に分割
# ax.hist(data_scores, bins=15, color='teal', edgecolor='black') 

# ax.set_title('Distribution of Employee Performance Scores') 
# ax.set_xlabel('Performance Score')
# ax.set_ylabel('Frequency (Number of Employees)')

# ax.legend() や ax.grid() は必須ではないが、必要に応じて追加可能

# # 散布図を描画 (plt.scatter を使用)
# ax.scatter(x_data, y_data, color='red', alpha=0.6, label='Sales Data') 
# ax.set_title('Sales vs. Advertising Spend (Scatter Plot)') 
# ax.set_xlabel('Advertising Spend (Units)')
# ax.set_ylabel('Sales (Units)')
# ax.legend()
# ax.grid(True)

# # 棒グラフを描画
ax.bar(df['month'], df['revenue'], color='purple') 
ax.set_title('Monthly Revenue from SQL Database') 
ax.set_xlabel('Month')
ax.set_ylabel('Revenue (JPY)')
ax.grid(axis='y', linestyle='--')

# # 棒グラフを描画 (plt.bar を使用)
# ax.bar(x_pos, hours, color=['skyblue', 'salmon', 'lightgreen', 'gold']) 
# ax.set_title('Average Weekly Work Hours by Department') 
# ax.set_xlabel('Department')
# ax.set_ylabel('Average Hours')
# # X軸の目盛をカテゴリ名に設定
# ax.set_xticks(x_pos)
# ax.set_xticklabels(categories)
# ax.grid(axis='y', linestyle='--') # Y軸方向のグリッドのみを表示

# 折れ線グラフの例
# ax.plot(x, y, label='sin(x)', color='blue', linestyle='--') # 線のスタイルなどを指定
# ax.set_title('Sine Wave') # グラフのタイトルを設定
# # X軸とY軸のラベルを設定
# ax.set_xlabel('X-axis (radians)')
# ax.set_ylabel('Y-axis')
# ax.legend() # 凡例を表示
# ax.grid(True) # グリッド（目盛線）を表示


# 4. グラフをメモリ上にPNG形式で保存
buf = io.BytesIO()
fig.savefig(buf, format='png', dpi=100)
plt.close(fig) # メモリの解放

# 5. メモリ上の画像データをBase64でエンコード
data = base64.b64encode(buf.getbuffer()).decode("ascii")

# 6. HTMLコードのテンプレート作成
html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Matplotlib HTML Output</title>
</head>
<body>
    <h1>Pythonで生成したグラフ</h1>
    <img src='data:image/png;base64,{data}' alt='Matplotlib Graph'>
</body>
</html>
"""

# 7. HTMLファイルとして出力
file_name = 'sql_graph_output.html'
with open(file_name, 'w') as f:
    f.write(html_template)

print(f"'{file_name}' が作成されました。ブラウザで開いてください。")

# 折れ線グラフ     plt.plot(x, y)	時系列データ、関数の描画
# 散布図           plt.scatter(x, y)	2つの変数の関係性の確認
# 棒グラフ         plt.bar(x, height)	カテゴリごとの数量の比較
# ヒストグラム     plt.hist(data, bins)	データ分布の確認
# 円グラフ         plt.pie(data, labels)	全体に対する比率の表現