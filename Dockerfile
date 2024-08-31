# 特定の最新のPythonバージョンを使用
FROM python:3.12-slim-bookworm

# 作業ディレクトリを設定
WORKDIR /app

# ホストのrequirements.txtファイルをコンテナの作業ディレクトリにコピー
COPY requirements.txt ./

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt