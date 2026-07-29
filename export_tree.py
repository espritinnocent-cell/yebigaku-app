import os

# 除外したい不要なフォルダ
EXCLUDE_DIRS = {
    "node_modules",
    ".venv",
    ".git",
    "__pycache__",
    "dist",
    "dev-dist",
    ".vscode",
}


def generate_tree(startpath):
    tree_text = ""
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        level = root.replace(startpath, "").count(os.sep)
        indent = " " * 4 * level
        tree_text += f"{indent}{os.path.basename(root)}/\n"
        subindent = " " * 4 * (level + 1)
        for f in files:
            tree_text += f"{subindent}{f}\n"
    return tree_text


if __name__ == "__main__":
    with open("project_structure.txt", "w", encoding="utf-8") as f:
        f.write(generate_tree("."))
    print("ファイル構造を project_structure.txt に保存しました！")
