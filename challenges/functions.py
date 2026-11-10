from html import escape

import nh3
import requests
from markdown_it import MarkdownIt
from pygments import highlight as _pygments_highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.token import STANDARD_TYPES
from pygments.util import ClassNotFound

URL = "https://emkc.org/api/v2/piston/execute"

DATA = {
    "language": "python",
    "version": "3.10.0",
    "files": [
        {
            "name": "test.py",
            "content": "",
        },
        {
            "name": "main.py",
            "content": "",
        },
    ],
}


def run_code(solution, test_case):
    DATA["files"][0]["content"] = test_case
    DATA["files"][1]["content"] = solution
    output = requests.post(URL, json=DATA)

    # print(f"{output = }, {output.content = }, {output.text = }, {output.raw = }")

    return output.json()


def prepare_test_case(test_case):
    return "from main import *\n" + test_case


# --- Markdown rendering -------------------------------------------------

#: CSS class wrapping a highlighted code block. The matching rules live in
#: ``static/style.css`` and are regenerated with::
#:
#:     python -c "from pygments.formatters import HtmlFormatter; \
#:         print(HtmlFormatter(style='default').get_style_defs('.codehilite'))"
CODE_CSS_CLASS = "codehilite"

# ``nowrap`` keeps Pygments from adding its own <div><pre>; we emit the wrapper
# ourselves so the result starts with "<pre", which is what markdown-it looks
# for to decide the block is already rendered.
_FORMATTER = HtmlFormatter(nowrap=True)


def _highlight(code: str, language: str, attrs: str) -> str:
    """Highlight a fenced code block, or return "" to let markdown-it escape it."""
    if not language:
        return ""
    try:
        lexer = get_lexer_by_name(language)
    except ClassNotFound:
        return ""
    body = _pygments_highlight(code, lexer, _FORMATTER)
    return (
        f'<pre class="{CODE_CSS_CLASS}">'
        f'<code class="language-{escape(language)}">{body}</code>'
        "</pre>"
    )


_MARKDOWN = (
    MarkdownIt("commonmark", {"highlight": _highlight, "html": False})
    .enable("table")
    .enable("strikethrough")
)


# Short class names Pygments emits for syntax tokens ("k", "nf", "s2", ...),
# plus the wrappers we and the old pandoc-rendered rows rely on.
_ALLOWED_CLASSES = frozenset(v for v in STANDARD_TYPES.values() if v) | {
    CODE_CSS_CLASS,
    "sourceCode",
}
_ALLOWED_CLASS_PREFIXES = ("language-",)

_ALLOWED_TAGS = nh3.ALLOWED_TAGS | {"tfoot"}
_ALLOWED_ATTRIBUTES = {
    **nh3.ALLOWED_ATTRIBUTES,
    "code": {"class"},
    "pre": {"class"},
    "span": {"class"},
    "div": {"class"},
}


def _attribute_filter(tag: str, attribute: str, value: str) -> str | None:
    """Keep only class names we actually style; drop everything else."""
    if attribute != "class":
        return value
    kept = [
        name
        for name in value.split()
        if name in _ALLOWED_CLASSES or name.startswith(_ALLOWED_CLASS_PREFIXES)
    ]
    return " ".join(kept) or None


def sanitize(html: str) -> str:
    """Strip anything that could execute from a block of HTML.

    Applied both when rendering new markdown and again at display time, so
    rows written before sanitizing existed are cleaned up on the way out.
    """
    return nh3.clean(
        html,
        tags=_ALLOWED_TAGS,
        attributes=_ALLOWED_ATTRIBUTES,
        attribute_filter=_attribute_filter,
        link_rel="nofollow noopener noreferrer",
    )


def markdown(source: str) -> str:
    """Render user supplied markdown to HTML that is safe to embed."""
    return sanitize(_MARKDOWN.render(source or ""))
