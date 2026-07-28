import xml.etree.ElementTree as ET

import httpx

# 代表的な法律の e-Gov 法令ID マッピング
LAW_ID_MAP = {
    "日本国憲法": {"id": "321CONSTITUTION", "num": "昭和二十一年憲法"},
    "民法": {"id": "129AC0000000089", "num": "明治二十九年法律第八十九号"},
    "刑法": {"id": "140AC0000000045", "num": "明治四十年法律第四十五号"},
}


async def fetch_law_xml(law_id: str) -> str:
    """e-Gov APIから指定された法令IDのXMLを取得する"""
    url = f"https://elaws.e-gov.go.jp/api/1/lawdata/{law_id}"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url, timeout=30.0)
        response.raise_for_status()
        return response.text


def parse_law_articles(
    xml_content: str, law_name: str, law_num: str
) -> list[dict[str, str | None]]:
    """e-Gov XMLを解析して条文単位のデータリストを作成する"""
    root = ET.fromstring(xml_content)
    articles: list[dict[str, str | None]] = []

    for article in root.findall(".//Article"):
        # e-Gov XMLの <Article Num="21"> 属性から半角数字の条文番号を取得
        num_attr = article.attrib.get("Num")

        # ArticleTitle (例: "第二十一条")
        article_title_elem = article.find("./ArticleTitle")
        title_text = (
            article_title_elem.text.strip()
            if article_title_elem is not None and article_title_elem.text
            else ""
        )

        # 条文番号の特定（Num属性優先）
        if num_attr:
            article_number = num_attr
        elif title_text:
            article_number = title_text.replace("第", "").replace("条", "").strip()
        else:
            continue

        # 見出し/キャプション (例: "(不法行為による損害賠償)")
        caption_elem = article.find("./ArticleCaption")
        article_title = (
            caption_elem.text.strip()
            if caption_elem is not None and caption_elem.text
            else (title_text if title_text else None)
        )

        # 本文の抽出と結合
        sentences: list[str] = []
        for sentence in article.findall(".//ParagraphSentence/Sentence"):
            if sentence.text:
                sentences.append(sentence.text.strip())

        text = "\n".join(sentences)
        if not text:
            continue

        articles.append(
            {
                "law_num": law_num,
                "law_name": law_name,
                "article_number": article_number,
                "article_title": article_title,
                "text": text,
            }
        )

    return articles
