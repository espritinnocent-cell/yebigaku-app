import asyncio
import sys
from pathlib import Path

# プロジェクトルート (backend/) を sys.path に追加
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.services.gemini_service import analyze_law_article


async def main():
    law_name = "民法"
    article_number = "709"
    text = "故意又は過失によって他人の権利又は法律上保護される利益を侵害した者は、これによって生じた損害を賠償する責任を負う。"

    print(f"--- 【{law_name} 第{article_number}条】の解析を Gemini API に依頼中... ---")

    try:
        result = await analyze_law_article(law_name, article_number, text)

        reqs = "\n".join([f"- {req}" for req in result.requirements])
        effs = "\n".join([f"- {eff}" for eff in result.effects])
        issues = "\n".join([f"- {iss}" for iss in result.main_issues])

        print("\n【解析成功！ Geminiからの構造化レスポンス】")
        print(f"■ 趣旨:\n{result.purpose}\n")
        print(f"■ 要件:\n{reqs}\n")
        print(f"■ 効果:\n{effs}\n")
        print(f"■ 主要論点:\n{issues}\n")
        print(f"■ 耳学用音声解説テキスト:\n{result.audio_explanation}\n")

    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    asyncio.run(main())
