FROM pytorch/pytorch:2.0.1-cuda11.8-cudnn8-runtime

# 基本ツールとFFmpeg（音声処理に必要）
RUN apt-get update && apt-get install -y git ffmpeg libsndfile1 && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリ
WORKDIR /app

# Python依存関係
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコード
COPY app.py .

# 起動コマンド（FastAPIをUvicornで実行）
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
