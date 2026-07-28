from pathlib import Path

import edge_tts

# 使用する日本語音声モデル（明るく読みやすい標準モデル）
VOICE = "ja-JP-NanamiNeural"


def ticks_to_vtt_timestamp(ticks: int) -> str:
    """100ナノ秒単位(ticks)のタイムスタンプを WebVTT形式 (HH:MM:SS.mmm) に変換"""
    ms = ticks // 10000
    seconds = ms // 1000
    milliseconds = ms % 1000
    minutes = seconds // 60
    hours = minutes // 60
    minutes = minutes % 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


async def generate_speech_and_vtt(
    text: str, output_filename_base: str, static_dir: str = "static/audio"
) -> tuple[str, str]:
    """テキストからMP3音声とWebVTT字幕ファイルを生成する関数

    Returns:
        tuple[str, str]: (MP3相対パス, VTT相対パス)
    """
    output_dir = Path(static_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    mp3_path = output_dir / f"{output_filename_base}.mp3"
    vtt_path = output_dir / f"{output_filename_base}.vtt"

    communicate = edge_tts.Communicate(text, VOICE)

    vtt_lines = ["WEBVTT\n"]
    cue_index = 1

    with open(mp3_path, "wb") as mp3_file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                mp3_file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                offset = chunk["offset"]
                duration = chunk["duration"]
                word = chunk["text"]

                start_time = ticks_to_vtt_timestamp(offset)
                end_time = ticks_to_vtt_timestamp(offset + duration)

                vtt_lines.append(f"{cue_index}")
                vtt_lines.append(f"{start_time} --> {end_time}")
                vtt_lines.append(f"{word}\n")
                cue_index += 1

    # WebVTTファイルの保存
    with open(vtt_path, "w", encoding="utf-8") as vtt_file:
        vtt_file.write("\n".join(vtt_lines))

    # 相対パスを返却（Web配信・DB保存用）
    relative_mp3_path = f"static/audio/{output_filename_base}.mp3"
    relative_vtt_path = f"static/audio/{output_filename_base}.vtt"

    return relative_mp3_path, relative_vtt_path
