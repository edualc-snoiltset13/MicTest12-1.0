import os
import shutil
import argparse

CATEGORY_MAP = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xls", ".xlsx", ".ppt", ".pptx", ".odt"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".go", ".rs", ".rb", ".php", ".sh"],
    "Data": [".json", ".xml", ".yaml", ".yml", ".sql", ".db", ".csv"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
}


def get_category(extension):
    for category, extensions in CATEGORY_MAP.items():
        if extension.lower() in extensions:
            return category
    return "Other"


def organize(target_dir, dry_run=False):
    if not os.path.isdir(target_dir):
        print(f"Error: '{target_dir}' is not a valid directory.")
        return

    moved = 0
    for filename in os.listdir(target_dir):
        filepath = os.path.join(target_dir, filename)

        if not os.path.isfile(filepath):
            continue

        ext = os.path.splitext(filename)[1]
        if not ext:
            continue

        category = get_category(ext)
        dest_dir = os.path.join(target_dir, category)

        if dry_run:
            print(f"[DRY RUN] {filename} -> {category}/")
        else:
            os.makedirs(dest_dir, exist_ok=True)
            shutil.move(filepath, os.path.join(dest_dir, filename))
            print(f"Moved: {filename} -> {category}/")

        moved += 1

    print(f"\n{'Would move' if dry_run else 'Moved'} {moved} file(s).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files by type.")
    parser.add_argument("directory", help="Directory to organize")
    parser.add_argument("--dry-run", action="store_true", help="Preview without moving files")
    args = parser.parse_args()

    organize(args.directory, dry_run=args.dry_run)
