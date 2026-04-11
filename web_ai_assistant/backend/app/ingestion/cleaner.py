import re


def clean_text(raw_text: str) -> str:
    """
    Cleans crawled webpage text for RAG usage.

    Goals:
    - remove navigation noise
    - remove legal/footer clutter
    - normalize whitespace
    - keep technical content
    - keep headings & code blocks
    """

    if not raw_text:
        return ""

    # normalize line endings
    text = raw_text.replace("\r", "\n")

    # remove multiple blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    lines = text.split("\n")

    cleaned_lines = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        lower = line.lower()

        # remove typical website noise
        noise_patterns = [
            "navigation",
            "menu",
            "search",
            "skip to content",
            "table of contents",
            "on this page",
            "edit this page",
            "previous",
            "next",
            "copyright",
            "all rights reserved",
            "privacy policy",
            "terms of service",
            "cookie",
            "consent",
            "subscribe",
            "sign up",
            "log in",
            "login",
            "logout",
            "register",
            "contact us",
            "about us",
            "follow us",
            "twitter",
            "linkedin",
            "facebook",
            "instagram",
            "youtube",
            "github",
            "slack",
            "discord",
            "newsletter",
            "advertisement",
            "ads",
            "sponsored",
            "feedback",
            "report issue"
        ]

        if any(pattern in lower for pattern in noise_patterns):
            continue

        # remove very short fragments unless code-like
        if len(line) < 25 and not looks_like_code(line):
            continue

        # remove excessive punctuation noise
        if re.fullmatch(r"[-_=*]{3,}", line):
            continue

        cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines)

    # normalize spaces
    cleaned_text = re.sub(r"[ \t]+", " ", cleaned_text)

    return cleaned_text



def looks_like_code(text: str) -> bool:
    """
    Detect if line resembles code snippet.
    """

    code_indicators = [
        "(",
        ")",
        "{",
        "}",
        "[",
        "]",
        "=",
        "==",
        "!=",
        "import ",
        "from ",
        "def ",
        "class ",
        "return ",
        "print(",
        "console.",
        "npm ",
        "pip ",
        "curl ",
        "http",
        "https",
        ".json",
        ".py",
        ".js"
    ]

    return any(token in text for token in code_indicators)