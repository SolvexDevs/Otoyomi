import requests
from pydub import AudioSegment
import io

# テキストをファイルに書き込む
text = "こんにちは、音声合成の世界へようこそ"
with open("text.txt", "w", encoding="utf-8") as file:
    file.write(text)

# 音声合成クエリを作成
with open("text.txt", "r", encoding="utf-8") as file:
    text_data = file.read()

query_url = "http://192.168.1.15:50021/audio_query"
query_params = {"speaker": 1, "text": text_data}
query_response = requests.post(query_url, params=query_params)

with open("query.json", "w", encoding="utf-8") as file:
    file.write(query_response.text)

# 音声合成を実行
synthesis_url = "http://192.168.1.15:50021/synthesis"
synthesis_headers = {"Content-Type": "application/json"}
with open("query.json", "r", encoding="utf-8") as file:
    synthesis_data = file.read()

synthesis_response = requests.post(synthesis_url, headers=synthesis_headers, params={"speaker": 1}, data=synthesis_data)

# 24000Hz で生成された音声を読み込み、44100Hz に変換
original_audio = AudioSegment.from_wav(io.BytesIO(synthesis_response.content))
resampled_audio = original_audio.set_frame_rate(44100)

# 変換後の音声ファイルを保存
resampled_audio.export("audio_44100.wav", format="wav")