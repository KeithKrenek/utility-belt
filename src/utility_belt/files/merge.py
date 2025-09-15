\
    """
    Utilities for merging text-friendly files into a single UTF-8 .txt.
    """
    from pathlib import Path
    from datetime import datetime

    DEFAULT_EXTS = {
        ".txt", ".md", ".py", ".json", ".yaml", ".yml", ".toml",
        ".csv", ".tsv", ".xml", ".ini", ".cfg", ".html", ".css", ".js", ".ts"
    }

    DEFAULT_EXCLUDES = {"node_modules", ".git", "__pycache__", "build", "dist", ".venv", ".mypy_cache"}

    def is_excluded(path: Path, exclude_substrings):
        p = str(path).lower()
        return any(substr.lower() in p for substr in exclude_substrings)

    def safe_read_text(path: Path, max_bytes=None) -> str:
        if max_bytes is not None and path.stat().st_size > max_bytes:
            raise ValueError(f"File too large ({path.stat().st_size} bytes)")
        # sniff for null bytes
        try:
            with open(path, "rb") as rb:
                head = rb.read(2048)
                if b"\x00" in head:
                    raise UnicodeDecodeError("utf-8", head, 0, 1, "binary data detected")
        except Exception:
            pass
        try:
            return path.read_text(encoding="utf-8", errors="strict")
        except Exception:
            try:
                return path.read_text(encoding="utf-8", errors="replace")
            except Exception:
                return path.read_text(encoding="latin-1", errors="replace")

    def discover_files(root: Path, include_exts=DEFAULT_EXTS, exclude_substrings=DEFAULT_EXCLUDES):
        files = []
        for p in sorted(root.rglob("*")):
            if not p.is_file():
                continue
            if include_exts and p.suffix.lower() not in include_exts:
                continue
            if is_excluded(p, exclude_substrings):
                continue
            files.append(p)
        return files

    def merge_files_to_text(
        input_dir: Path,
        output_txt: Path,
        include_exts=DEFAULT_EXTS,
        exclude_substrings=DEFAULT_EXCLUDES,
        max_file_bytes: int | None = 2 * 1024 * 1024,
        include_headers: bool = True,
        include_eof_markers: bool = True,
        use_relative_paths: bool = True,
    ) -> dict:
        """
        Merge files from input_dir into output_txt. Returns a summary dict.
        """
        root = input_dir.resolve()
        files = discover_files(root, include_exts, exclude_substrings)
        written = 0
        skipped = 0
        err_files: list[tuple[str, str]] = []
        output_txt.parent.mkdir(parents=True, exist_ok=True)

        with open(output_txt, "w", encoding="utf-8") as out:
            out.write("# Merged Text Export\n")
            out.write(f"# Source root: {root}\n")
            out.write(f"# Timestamp: {datetime.utcnow().isoformat()}Z\n")
            out.write(f"# Files included: {len(files)}\n\n")

            for f in files:
                try:
                    content = safe_read_text(f, max_bytes=max_file_bytes)
                    if include_headers:
                        shown = f.relative_to(root) if use_relative_paths else f.resolve()
                        out.write(f"\n===== FILE: {shown} | SIZE: {f.stat().st_size} bytes =====\n")
                    out.write(content)
                    if include_eof_markers:
                        out.write("\n===== END FILE =====\n")
                    written += 1
                except Exception as e:
                    skipped += 1
                    err_files.append((str(f), str(e)))

        return {
            "root": str(root),
            "output": str(output_txt),
            "discovered": len(files),
            "written": written,
            "skipped": skipped,
            "errors": err_files[:10],
        }
