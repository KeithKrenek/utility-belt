# File: create_repo.py
# Minimal script to generate the requested repo scaffolding with empty files.

from pathlib import Path

def main():
    root = Path(".")
    src = "templates"

    # Directories to create (omit tmp/uploads so it can be created at runtime)
    dirs = [
        root / src / "html",
        root / src / "js"
    ]

    # Empty files to create
    files = [
        root / "app.py",
        # root / src / "html" / "server.js",
        # root / src / "js" / "openaiClient.js",
        # root / src / "js" / "resumeSchema.js",
        # root / src / "js" / "optimize.js",
        # root / "public" / "index.html",
    ]

    # Create directories
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # Create empty files
    for f in files:
        f.touch(exist_ok=True)

    print("Scaffold created at:", root.resolve())

if __name__ == "__main__":
    main()
