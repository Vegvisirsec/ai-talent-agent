import argparse
import base64
import html
import re
from pathlib import Path


INLINE_CODE_RE = re.compile(r"`([^`]+)`")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
PLACEHOLDER_IMAGE_RE = re.compile(
    r"!\[[^\]]*Profile Photo[^\]]*\]\((photo-placeholder\.jpg|portrait\.png)\)",
    re.IGNORECASE,
)


def embed_image_src(src: str, base_dir: Path) -> str:
    if src.startswith(("http://", "https://", "data:")):
        return src

    image_path = (base_dir / src).resolve()
    if not image_path.exists():
        return src

    suffix = image_path.suffix.lower()
    mime_type = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }.get(suffix)
    if not mime_type:
        return src

    encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def convert_inline(text: str, base_dir: Path) -> str:
    placeholders = []

    def stash(tag: str) -> str:
        placeholders.append(tag)
        return f"@@PLACEHOLDER{len(placeholders) - 1}@@"

    text = IMAGE_RE.sub(
        lambda m: stash(
            f'<img src="{html.escape(embed_image_src(m.group(2), base_dir), quote=True)}" alt="{html.escape(m.group(1), quote=True)}" class="profile-photo" />'
        ),
        text,
    )
    text = LINK_RE.sub(
        lambda m: stash(
            f'<a href="{html.escape(m.group(2), quote=True)}">{html.escape(m.group(1))}</a>'
        ),
        text,
    )
    text = INLINE_CODE_RE.sub(lambda m: stash(f"<code>{html.escape(m.group(1))}</code>"), text)
    text = BOLD_RE.sub(lambda m: stash(f"<strong>{html.escape(m.group(1))}</strong>"), text)
    text = html.escape(text)

    for idx, tag in enumerate(placeholders):
        text = text.replace(f"@@PLACEHOLDER{idx}@@", tag)
    return text


def markdown_to_html(markdown_text: str, title: str, base_dir: Path) -> str:
    lines = markdown_text.splitlines()
    body = []
    paragraph = []
    in_list = False

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = " ".join(part.strip() for part in paragraph).strip()
            if text:
                body.append(f"<p>{convert_inline(text, base_dir)}</p>")
            paragraph = []

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            body.append("</ul>")
            in_list = False

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            close_list()
            continue

        if stripped == "---":
            flush_paragraph()
            close_list()
            body.append("<hr />")
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            close_list()
            body.append(f"<h1>{convert_inline(stripped[2:].strip(), base_dir)}</h1>")
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            close_list()
            body.append(f"<h2>{convert_inline(stripped[3:].strip(), base_dir)}</h2>")
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            close_list()
            body.append(f"<h3>{convert_inline(stripped[4:].strip(), base_dir)}</h3>")
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            if not in_list:
                body.append("<ul>")
                in_list = True
            body.append(f"<li>{convert_inline(stripped[2:].strip(), base_dir)}</li>")
            continue

        if stripped.endswith("  "):
            paragraph.append(stripped[:-2] + "<br />")
        else:
            paragraph.append(stripped)

    flush_paragraph()
    close_list()

    style = """
:root {
  color-scheme: dark;
  --bg: #0d1117;
  --page: #161b22;
  --text: #e6edf3;
  --muted: #9fb0c3;
  --heading: #f0f6fc;
  --border: #30363d;
  --link: #7cc7ff;
  --code-bg: #1f2630;
  --photo-bg-a: #1a2330;
  --photo-bg-b: #111827;
}
body {
  margin: 0;
  background: radial-gradient(circle at top, #141b24 0%, var(--bg) 55%);
  color: var(--text);
  font-family: "Segoe UI", Arial, sans-serif;
  line-height: 1.5;
}
.page {
  box-sizing: border-box;
  max-width: 920px;
  margin: 24px auto;
  padding: 40px 48px;
  background: var(--page);
  border: 1px solid var(--border);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
}
h1, h2, h3 {
  color: var(--heading);
  margin-top: 0;
}
h1 {
  margin-bottom: 12px;
  font-size: 2rem;
}
h2 {
  margin-top: 28px;
  margin-bottom: 10px;
  font-size: 1.2rem;
  border-bottom: 1px solid var(--border);
  padding-bottom: 4px;
}
h3 {
  margin-top: 18px;
  margin-bottom: 4px;
  font-size: 1rem;
}
p, li {
  font-size: 0.98rem;
}
p {
  color: var(--text);
}
ul {
  margin: 8px 0 12px 20px;
  padding: 0;
}
li {
  margin: 0 0 6px 0;
}
hr {
  border: 0;
  border-top: 1px solid var(--border);
  margin: 18px 0;
}
a {
  color: var(--link);
  text-decoration: none;
}
code {
  background: var(--code-bg);
  padding: 1px 4px;
  border-radius: 4px;
  font-family: Consolas, monospace;
  font-size: 0.94em;
}
.profile-photo {
  display: block;
  width: 140px;
  max-width: 100%;
  height: auto;
  border: 1px solid var(--border);
  margin: 0 0 16px 0;
  object-fit: cover;
}
img.profile-photo[src="photo-placeholder.jpg"] {
  min-height: 170px;
  background: linear-gradient(135deg, var(--photo-bg-a) 0%, var(--photo-bg-b) 100%);
}
@media print {
  body {
    background: #ffffff;
    color: #18212b;
  }
  .page {
    margin: 0;
    max-width: none;
    padding: 0;
    background: #ffffff;
    border: 0;
    box-shadow: none;
  }
  h1, h2, h3 {
    color: #102033;
  }
  h2, hr, .profile-photo {
    border-color: #d9e0e8;
  }
  a {
    color: #0b5cab;
  }
  code {
    background: #eef3f8;
  }
}
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>{style}</style>
</head>
<body>
  <main class="page">
    {''.join(body)}
  </main>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a CV markdown file to clean HTML.")
    parser.add_argument("input", nargs="?", help="Path to the markdown CV file")
    parser.add_argument("--path", dest="input_path", help="Path to the markdown CV file")
    parser.add_argument(
        "-o",
        "--output",
        help="Path to the output HTML file. Defaults to the input filename with .html extension.",
    )
    args = parser.parse_args()

    selected_input = args.input_path or args.input
    if not selected_input:
        parser.error("Provide a markdown CV path either as a positional argument or with --path.")

    input_path = Path(selected_input)
    output_path = Path(args.output) if args.output else input_path.with_suffix(".html")

    markdown_text = input_path.read_text(encoding="utf-8")
    portrait_path = input_path.parent / "portrait.png"
    embedded_portrait = False
    if portrait_path.exists():
        if PLACEHOLDER_IMAGE_RE.search(markdown_text):
            markdown_text = PLACEHOLDER_IMAGE_RE.sub("![Profile Photo](portrait.png)", markdown_text, count=1)
            embedded_portrait = True
        elif not IMAGE_RE.search(markdown_text):
            lines = markdown_text.splitlines()
            if lines and lines[0].startswith("# "):
                lines.insert(1, "")
                lines.insert(2, "![Profile Photo](portrait.png)")
                lines.insert(3, "")
                markdown_text = "\n".join(lines)
            else:
                markdown_text = "![Profile Photo](portrait.png)\n\n" + markdown_text
            embedded_portrait = True
    title = input_path.stem.replace("_", " ").title()
    html_text = markdown_to_html(markdown_text, title, input_path.parent)
    output_path.write_text(html_text, encoding="utf-8")

    print(f"Rendered {input_path} -> {output_path}")
    if embedded_portrait:
        print(f"Embedded portrait from {portrait_path}")
    elif PLACEHOLDER_IMAGE_RE.search(markdown_text):
        print(f"No portrait embedded. Expected file at {portrait_path}")


if __name__ == "__main__":
    main()
