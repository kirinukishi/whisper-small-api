from fastapi import FastAPI, UploadFile, File
import uvicorn
import os
from faster_whisper import WhisperModel

app = FastAPI()

# モデルを初期化（Smallモデル）
model = WhisperModel("small", device="cuda", compute_type="float16")

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    # 一時ファイルに保存
    temp_file = "temp_audio.wav"
    with open(temp_file, "wb") as f:
        f.write(await file.read())

    # 音声を文字起こし
    segments, info = model.transcribe(temp_file)

    # SRT形式に変換
    srt_output = []
    for i, segment in enumerate(segments, start=1):
        start = segment.start
        end = segment.end
        text = segment.text.strip()
        srt_output.append(f"{i}\n{format_timestamp(start)} --> {format_timestamp(end)}\n{text}\n")

    os.remove(temp_file)
    return {"srt": "".join(srt_output)}

def format_timestamp(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds * 1000) % 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
