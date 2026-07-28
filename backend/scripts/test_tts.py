import asyncio
import sys
from pathlib import Path

# プロジェクトルート (backend/) を sys.path に追加して app モジュールを認識させる
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.services.legal_dict import prepare_texts
from app.services.tts_service import generate_speech_and_vtt


async def main():
    raw_text = "遺言により競売手続きを開始し、相手方の相殺主張を排斥する。"
    display_text, audio_text = prepare_texts(raw_text)

    print(f"【表示用テキスト】: {display_text}")
    print(f"【音声用テキスト】: {audio_text}")
    print("音声と字幕を生成中...")

    mp3_path, vtt_path = await generate_speech_and_vtt(
        text=audio_text, output_filename_base="test_speech"
    )

    print("生成成功！")
    print(f"MP3ファイル: {mp3_path}")
    print(f"VTT字幕ファイル: {vtt_path}")


if __name__ == "__main__":
    asyncio.run(main())
