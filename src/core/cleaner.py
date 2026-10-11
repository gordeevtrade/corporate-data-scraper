"""
HTML Sanitizer and Markdown Converter.
Strips boilerplate, navigation, scripts, and styling to produce clean LLM-ready content.
"""

from bs4 import BeautifulSoup
import re

TAGS_TO_REMOVE = [
    "script", "style", "nav", "footer", "header", "noscript",
    "svg", "iframe", "button", "input", "form", "aside"
]

def clean_html_to_markdown(html_content: str) -> str:
    """
    Parses raw HTML, removes noisy web chrome, and returns clean structured Markdown.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove unwanted tags
    for tag_name in TAGS_TO_REMOVE:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    # Get body or fallback to root
    body = soup.body if soup.body else soup

    lines = []
    for element in body.find_all(["h1", "h2", "h3", "h4", "p", "li", "a", "span", "div"]):
        # Only take direct elements or leaf blocks to avoid duplicates
        text = element.get_text(separator=" ", strip=True)
        if not text or len(text) < 2:
            continue

        if element.name in ["h1", "h2"]:
            lines.append(f"\n## {text}\n")
        elif element.name in ["h3", "h4"]:
            lines.append(f"\n### {text}\n")
        elif element.name == "li":
            lines.append(f"- {text}")
        elif element.name == "p" and len(text) > 20:
            lines.append(f"{text}\n")

    raw_md = "\n".join(lines)
    # Deduplicate redundant consecutive blank lines
    clean_md = re.sub(r"\n{3,}", "\n\n", raw_md).strip()

    return clean_md
