import asyncio
import json
import sys
from pathlib import Path

# プロジェクトルート (backend/) を sys.path に追加
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.database import create_db_and_tables, engine
from app.models import LawArticle
from app.services.gemini_service import analyze_law_article  # 追加
from app.services.law_fetcher import LAW_ID_MAP, fetch_law_xml, parse_law_articles
from app.services.legal_dict import prepare_texts
from app.services.tts_service import generate_speech_and_vtt
from sqlmodel import Session, select


async def import_law_target_articles(
    law_name: str, target_article_numbers: list[str] | None = None
):
    if law_name not in LAW_ID_MAP:
        print(f"エラー: {law_name} は LAW_ID_MAP に登録されていません。")
        return

    law_info = LAW_ID_MAP[law_name]
    print(f"--- 【{law_name}】のデータを e-Gov API から取得中... ---")

    xml_text = await fetch_law_xml(law_info["id"])
    parsed_articles = parse_law_articles(xml_text, law_name, law_info["num"])
    print(f"取得完了: 全 {len(parsed_articles)} 条文が見つかりました。")

    create_db_and_tables()

    with Session(engine) as session:
        for item in parsed_articles:
            art_num = str(item["article_number"])

            if target_article_numbers and art_num not in target_article_numbers:
                continue

            statement = select(LawArticle).where(
                LawArticle.law_name == law_name,
                LawArticle.article_number == art_num,
            )
            if session.exec(statement).first():
                print(f"スキップ: {law_name} 第{art_num}条 は登録済みです。")
                continue

            raw_text = str(item["text"])

            print(f"[{law_name} 第{art_num}条] Gemini AIで要約・解説文を生成中...")
            try:
                # 1. Gemini API で解析
                ai_result = await analyze_law_article(law_name, art_num, raw_text)

                # 2. 生成された音声用解説テキストを、さらに難読漢字辞書に通す
                _, audio_text = prepare_texts(ai_result.audio_explanation)

                # 3. 音声(MP3)と字幕(VTT)の生成
                print(f"[{law_name} 第{art_num}条] 音声と字幕を生成中...")
                file_base = f"law_{law_name}_{art_num}"
                mp3_path, vtt_path = await generate_speech_and_vtt(
                    text=audio_text, output_filename_base=file_base
                )

                # 4. DBへ保存（リストはJSON文字列に変換）
                law_article = LawArticle(
                    law_num=str(item["law_num"]),
                    law_name=law_name,
                    article_number=art_num,
                    article_title=item["article_title"],
                    text=raw_text,
                    purpose=ai_result.purpose,
                    requirements=json.dumps(ai_result.requirements, ensure_ascii=False),
                    effects=json.dumps(ai_result.effects, ensure_ascii=False),
                    main_issues=json.dumps(ai_result.main_issues, ensure_ascii=False),
                    reading_text=audio_text,
                    audio_file_path=mp3_path,
                    vtt_subtitles=vtt_path,
                )

                session.add(law_article)
                session.commit()
                print(f"★ 保存成功: {law_name} 第{art_num}条\n")

            except Exception as e:
                print(
                    f"エラー: {law_name} 第{art_num}条 の処理中に問題が発生しました。詳細: {e}"
                )


async def main():
    # 憲法21条と民法709条でパイプラインの最終テスト
    await import_law_target_articles("日本国憲法", target_article_numbers=["21"])
    await import_law_target_articles("民法", target_article_numbers=["709"])


if __name__ == "__main__":
    asyncio.run(main())
