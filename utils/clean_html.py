import re


def clean(html: str) -> str:
    """Remove HTML markup from the given string."""
    # Remove inline JavaScript/CSS, HTML comments, and HTML tags
    cleaned_html = re.sub(
        r"(?is)<(script|style).*?>.*?(</\1>)|<!--(.*?)-->[\n]?|<(?s).*?>",
        "",
        html.strip(),
    )

    # Deal with whitespace and HTML entities
    cleaned_html = re.sub(r"&nbsp;|  |\t|&.*?;[0-9]*&.*?;|&.*?;", "", cleaned_html)

    return cleaned_html.strip()
