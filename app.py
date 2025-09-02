import os
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import PlainTextResponse
from faster_whisper import WhisperModel
import tempfile

app = FastAPI(title="Whisper Small API")

# Whisper Small を初期化（GPU利用）
model = WhisperModel("small", device="cuda", compute_type="float16")

def format_timestamp(seconds: float) -> str:
    """秒数をSRT形式のタイムスタンプに変換"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds * 1000) % 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"

def format_text_for_subtitles(text: str, max_len: int = 12) -> str:
    """
    テロップ用に文字数を制限
    - 1行あたり max_len 文字以内
    - 2行まで
    - 句読点は削除し、必要ならスペースに置換
    """
    text = text.replace("、", " ").replace("。", " ")
    chunks = [text[i:i+max_len] for i in range(0, len(text), max_len)]
    return "\n".join(chunks[:2])

@app.post("/transcribe", response_class=PlainTextResponse)
async def transcribe(file: UploadFile = File(...)):
    # 一時ファイルに保存
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    # 文字起こし実行
    segments, _ = model.transcribe(tmp_path, beam_size=5)

    # SRT形式で組み立て
    srt_output = []
    for idx, seg in enumerate(segments, start=1):
        start = format_timestamp(seg.start)
        end = format_timestamp(seg.end)
        text = format_text_for_subtitles(seg.text.strip())
        srt_output.append(f"{idx}\n{start} --> {end}\n{text}\n")

    os.remove(tmp_path)  # 後片付け
    return "\n".join(srt_output)
