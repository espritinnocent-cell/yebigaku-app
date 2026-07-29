import json
import os
import sqlite3

# backendディレクトリの絶対パス
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def export_data():
    print(f"📁 読み込み対象DB: {DB_PATH}")

    # DBが存在するかチェック
    if not os.path.exists(DB_PATH) or os.path.getsize(DB_PATH) == 0:
        print("❌ データベースファイルが存在しないか、空です。")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        # lawarticle（条文）テーブルから全データを取得
        cursor.execute("SELECT * FROM lawarticle")
        rows = cursor.fetchall()

        # 辞書（オブジェクト）の配列に変換
        articles = [dict(row) for row in rows]

        # 出力先: frontend/public/laws.json
        frontend_public_dir = os.path.abspath(
            os.path.join(BASE_DIR, "..", "frontend", "public")
        )
        os.makedirs(frontend_public_dir, exist_ok=True)
        output_path = os.path.join(frontend_public_dir, "laws.json")

        # 配列そのままの形でJSONファイルとして保存
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)

        print(
            f"🎉 データの書き出しが完了しました！ ({len(articles)}件の条文データを保存)"
        )
        print(f"保存先: {output_path}")

    except Exception as e:
        print(f"❌ 書き出し中にエラーが発生しました: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    export_data()
