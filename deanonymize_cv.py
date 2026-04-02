import argparse
import json
import re
from pathlib import Path


TOKEN_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


def replace_tokens(text: str, values: dict[str, str], strict: bool):
    missing = set()

    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        if key in values:
            return str(values[key])
        missing.add(key)
        return match.group(0)

    result = TOKEN_RE.sub(repl, text)
    if strict and missing:
        missing_list = ", ".join(sorted(missing))
        raise RuntimeError(f"Missing token values for: {missing_list}")
    return result, sorted(missing)


def main():
    parser = argparse.ArgumentParser(
        description="Replace {{TOKENS}} in a CV markdown file using values from a local JSON file."
    )
    parser.add_argument("input", nargs="?", help="Path to the markdown CV file")
    parser.add_argument("--path", dest="input_path", help="Path to the markdown CV file")
    parser.add_argument("--data", required=True, help="Path to the JSON file containing token values")
    parser.add_argument(
        "-o",
        "--output",
        help="Path to the output markdown file. Defaults to the input filename with .final.md suffix.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if any {{TOKEN}} in the input file is missing from the JSON mapping.",
    )
    args = parser.parse_args()

    selected_input = args.input_path or args.input
    if not selected_input:
        parser.error("Provide a markdown CV path either as a positional argument or with --path.")

    input_path = Path(selected_input)
    data_path = Path(args.data)
    output_path = Path(args.output) if args.output else input_path.with_name(f"{input_path.stem}.final.md")

    markdown_text = input_path.read_text(encoding="utf-8")
    token_values = json.loads(data_path.read_text(encoding="utf-8"))

    if not isinstance(token_values, dict):
        raise RuntimeError("JSON mapping must be an object of TOKEN -> value pairs.")

    rendered_text, missing = replace_tokens(markdown_text, token_values, strict=args.strict)
    output_path.write_text(rendered_text, encoding="utf-8")

    print(f"Rendered {input_path} -> {output_path}")
    if missing:
        print(f"Unresolved tokens left in output: {', '.join(missing)}")


if __name__ == "__main__":
    main()
