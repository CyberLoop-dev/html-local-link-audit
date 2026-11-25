import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"])
        if tag.lower() == "a" and values.get("name"):
            self.ids.add(values["name"])
        for attribute in ("href", "src"):
            value = values.get(attribute)
            if value:
                self.links.append((attribute, value, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def parse_page(path: Path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    parser.close()
    return parser


def inside_root(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def audit_site(target: Path):
    target = target.resolve()
    if target.is_file():
        root = target.parent
        pages = [target] if target.suffix.lower() in (".html", ".htm") else []
    else:
        root = target
        pages = sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in (".html", ".htm"))

    cache = {}
    issues = []

    def get_parser(page: Path):
        if page not in cache:
            cache[page] = parse_page(page)
        return cache[page]

    for page in pages:
        parser = get_parser(page)
        for attribute, raw, line in parser.links:
            parts = urlsplit(raw.strip())
            if parts.scheme or parts.netloc or not raw.strip():
                continue

            relative_path = unquote(parts.path)
            if relative_path.startswith("/"):
                candidate = root / relative_path.lstrip("/")
            elif relative_path:
                candidate = page.parent / relative_path
            else:
                candidate = page

            resolved = candidate.resolve()
            if not inside_root(resolved, root):
                problem = "outside-root"
            else:
                if resolved.is_dir():
                    resolved = resolved / "index.html"
                if not resolved.is_file():
                    problem = "missing-file"
                else:
                    problem = ""
                    if parts.fragment and resolved.suffix.lower() in (".html", ".htm"):
                        if unquote(parts.fragment) not in get_parser(resolved).ids:
                            problem = "missing-fragment"

            if problem:
                issues.append({
                    "file": str(page.relative_to(root)),
                    "line": line,
                    "attribute": attribute,
                    "target": raw,
                    "problem": problem,
                })
    return pages, issues


def main():
    parser = argparse.ArgumentParser(description="Audit local HTML links without fetching external URLs.")
    parser.add_argument("path", type=Path, help="HTML file or site directory")
    parser.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = parser.parse_args()
    if not args.path.exists():
        parser.error(f"path does not exist: {args.path}")
    pages, issues = audit_site(args.path)
    result = {"pages_scanned": len(pages), "issue_count": len(issues), "issues": issues}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Scanned {len(pages)} HTML page(s); found {len(issues)} issue(s).")
        for issue in issues:
            print(f"{issue['file']}:{issue['line']}: {issue['problem']} {issue['attribute']}={issue['target']}")
    raise SystemExit(1 if issues else 0)


if __name__ == "__main__":
    main()
