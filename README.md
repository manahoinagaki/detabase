# detabase
野中先生からの課題
 python generate_graph.py
 python3 -m http.server 8000

 streamlit run app.py

 source .venv/bin/activate
 streamlit run app.py

 ステップ 1: PostgreSQLサーバーの起動あなたがPostgreSQLをどのように実行しているかに応じて、適切なコマンドを実行してください。
 実行環境  起動コマンドの例
 Dockerコンテナ  docker start <コンテナ名またはID>
 macOS (Homebrew)  brew services start postgresqlLinux (systemd)sudo systemctl start postgresqlWindowsサービス  Windowsサービスマネージャーから起動する、またはコマンドプロンプトで net start postgresql-x6x (バージョンによる)

 ./.venv/bin/python -m streamlit run app.pydocker ps
 docker run --name pg_app -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres