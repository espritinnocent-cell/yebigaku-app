from app.config import settings
from google import genai
from google.genai import types
from pydantic import BaseModel, Field


class ArticleAnalysis(BaseModel):
    """条文のAI要約・論点解析結果モデル"""

    purpose: str = Field(description="条文の趣旨・目的の要約（1〜2文で簡潔に）")
    requirements: list[str] = Field(description="要件（適用条件）のリスト")
    effects: list[str] = Field(description="効果（法律上の帰結）のリスト")
    main_issues: list[str] = Field(
        description="予備試験・司法試験で頻出の主要論点・解釈上のポイント"
    )
    audio_explanation: str = Field(
        description="耳学（音声解説）用に最適化した解説文。接続詞を補い、聴くだけで頭に入る丁寧な講義調テキスト"
    )


def get_gemini_client() -> genai.Client:
    """Gemini API クライアントの初期化"""
    if (
        not settings.gemini_api_key
        or settings.gemini_api_key == "your_gemini_api_key_here"
    ):
        raise ValueError(
            "GEMINI_API_KEY が .env に正しく設定されていません。Google AI Studio から API キーを取得して .env に記載してください。"
        )
    return genai.Client(api_key=settings.gemini_api_key)


async def analyze_law_article(
    law_name: str, article_number: str, text: str
) -> ArticleAnalysis:
    """Gemini 2.0 Flash を使用して条文を解析・要約・音声解説テキスト化する"""
    client = get_gemini_client()

    prompt = f"""
あなたは司法試験予備試験の優秀な講師です。
以下の法律条文について、受験生が効率よく暗記・想起できるように趣旨、要件、効果、重要論点を抽出し、音声学習（耳学）用の講義テキストを作成してください。

【対象条文】
{law_name} 第{article_number}条
{text}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ArticleAnalysis,
            temperature=0.2,
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini API からの応答が空でした。")

    return ArticleAnalysis.model_validate_json(response.text)
