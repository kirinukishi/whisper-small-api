# ベースイメージ: PyTorch + CUDA + cuDNN 開発環境
FROM pytorch/pytorch:2.0.1-cuda11.8-cudnn8-runtime


# 作業ディレクトリを設定
WORKDIR /app

# 基本ツールのインストール（git, ffmpeg など）
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Pythonライブラリをインストール
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# アプリケーションコードをコピー
COPY app.py .

# FastAPI を uvicorn で起動
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
