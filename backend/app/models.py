from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class ImportanceRank(str, Enum):
    A = "A"
    B = "B"
    C = "C"


class UnderstandingLevel(int, Enum):
    UNLEARNED = 0  # 未学習
    POOR = 1  # 微妙
    GOOD = 2  # 理解
    PERFECT = 3  # 完璧


class CaseMetadata(SQLModel, table=True):
    """判例データ"""

    id: int | None = Field(default=None, primary_key=True)
    case_id: str = Field(index=True, unique=True)  # 例: "case_001"
    title: str  # 例: "マクリーン事件"
    case_number: str | None = None  # 例: "昭和53(行ツ)65"
    date: str | None = None  # 例: "1978-10-04"
    category: str = Field(index=True)  # 例: "憲法"
    importance_rank: ImportanceRank = Field(default=ImportanceRank.C, index=True)
    related_articles: str | None = None  # 例: "憲法第21条"
    keywords: str | None = None  # キーワード（カンマ区切り）
    raw_text: str | None = None  # 判決原文

    # AI生成コンテンツ
    case_summary_ai: str | None = None  # 判旨のAI要約
    issues_ai: str | None = None  # 論点・論証パターン
    reading_text: str | None = None  # 音声読み上げ用ひらがな最適化テキスト

    # 音声・メディア
    audio_file_path: str | None = None  # MP3パス
    vtt_subtitles: str | None = None  # 字幕データ (WebVTT形式)


class LawArticle(SQLModel, table=True):
    """条文データ"""

    id: int | None = Field(default=None, primary_key=True)
    law_num: str = Field(index=True)  # 例: "昭和二十二年法律第五十四号"
    law_name: str = Field(index=True)  # 例: "日本国憲法", "民法"
    article_number: str = Field(index=True)  # 枝番対応のためstr型 (例: "709の2")
    article_title: str | None = None
    text: str  # 条文本文
    reading_text: str | None = None  # 音声読み上げ用テキスト
    audio_file_path: str | None = None
    vtt_subtitles: str | None = None
    # --- Gemini AI による解析データ ---
    purpose: str | None = None
    requirements: str | None = None  # JSON文字列として保存
    effects: str | None = None  # JSON文字列として保存
    main_issues: str | None = None  # JSON文字列として保存
    # --- 音声・字幕 ---
    reading_text: str | None = None
    audio_file_path: str | None = None
    vtt_subtitles: str | None = None


class UserProgress(SQLModel, table=True):
    """学習進捗・復習管理"""

    id: int | None = Field(default=None, primary_key=True)
    item_type: str = Field(index=True)  # "case" または "law"
    item_id: int = Field(index=True)
    understanding_level: UnderstandingLevel = Field(
        default=UnderstandingLevel.UNLEARNED
    )
    play_count: int = Field(default=0)  # 再生回数
    is_bookmarked: bool = Field(default=False)  # ブックマーク
    last_played_at: datetime | None = None
