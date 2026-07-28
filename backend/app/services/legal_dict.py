import re

# 法律用語の難読・特殊読み辞書（実務の慣習に基づく読み分け）
LEGAL_DICT = {
    "遺言": "いごん",
    "競売": "けいばい",
    "相殺": "そうさい",
    "瑕疵": "かし",
    "過料": "あやまちりょう",
    "科料": "とがりょう",
    "勾留": "こうりゅう",
    "対抗要件": "たいこうようけん",
    "過失": "かしつ",
}

# 辞書内の単語を「遺言|競売|相殺|...」という1つのパターンにコンパイル
PATTERN = re.compile("|".join(map(re.escape, LEGAL_DICT.keys())))


def replace_legal_terms(text: str) -> str:
    """1回のテキストスキャンで難読漢字を一気にひらがな置換する"""
    return PATTERN.sub(lambda match: LEGAL_DICT[match.group(0)], text)


def prepare_texts(raw_text: str) -> tuple[str, str]:
    """画面表示用テキストと音声読み上げ用テキストを生成する"""
    display_text = raw_text
    audio_text = replace_legal_terms(raw_text)
    return display_text, audio_text
