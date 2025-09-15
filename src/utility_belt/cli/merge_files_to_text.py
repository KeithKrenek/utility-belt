import argparse
from pathlib import Path
from utility_belt.files.merge import merge_files_to_text, DEFAULT_EXTS, DEFAULT_EXCLUDES

def parse_exts(value: str):
    if not value:
        return DEFAULT_EXTS
    parts = [p.strip().lower() for p in value.split(",")]
    return {p if p.startswith(".") else "." + p for p in parts if p}

def parse_excludes(value: str):
    if not value:
        return DEFAULT_EXCLUDES
    return {p.strip() for p in value.split(",") if p.strip()}

def main():
    ap = argparse.ArgumentParser(description="Merge text-friendly files into one .txt")
    ap.add_argument("--input-dir", "-i", type=Path, required=True, help="Folder to scan")
    ap.add_argument("--output", "-o", type=Path, required=True, help="Output .txt path")
    ap.add_argument("--exts", help="Comma-separated extensions (e.g., '.py,.md,.txt')")
    ap.add_argument("--exclude", help="Comma-separated substrings to exclude (e.g., 'node_modules,.git')")
    ap.add_argument("--max-bytes", type=int, default=2*1024*1024, help="Max bytes per file")
    ap.add_argument("--no-headers", action="store_true", help="Do not include per-file headers")
    ap.add_argument("--no-eof", action="store_true", help="Do not include end-of-file markers")
    ap.add_argument("--absolute", action="store_true", help="Use absolute paths in headers")

    args = ap.parse_args()
    include_exts = parse_exts(args.exts)
    exclude = parse_excludes(args.exclude)

    summary = merge_files_to_text(
        input_dir=args.input_dir,
        output_txt=args.output,
        include_exts=include_exts,
        exclude_substrings=exclude,
        max_file_bytes=args.max_bytes,
        include_headers=not args.no_headers,
        include_eof_markers=not args.no_eof,
        use_relative_paths=not args.absolute,
    )
    print("Merged:", summary["written"], "files into", summary["output"])
    if summary["skipped"]:
        print("Skipped:", summary["skipped"])
    if summary["errors"]:
        print("Errors (first few):")
        for p, e in summary["errors"]:
            print(" -", p, "->", e)

if __name__ == "__main__":
    main()
