import pytest

from markdown_it import MarkdownIt

pytest.importorskip("linkify_it")


def test_token_levels():
    mdit = MarkdownIt(options_update={"linkify": True}).enable("linkify")
    tokens = mdit.parse("www.python.org")
    inline = tokens[1]
    assert inline.type == "inline"
    assert inline.children
    link_open = inline.children[0]
    assert link_open.type == "link_open"
    link_text = inline.children[1]
    assert link_text.type == "text"
    link_close = inline.children[2]
    assert link_close.type == "link_close"

    # Assert that linkify tokens have correct nesting levels
    assert link_open.level == 0
    assert link_text.level == 1
    assert link_close.level == 0


@pytest.mark.parametrize(
    ("src", "expected"),
    [
        # the scheme taken from the text before "[" is as long as the matched URL
        (
            "abcdefgh[http://s://",
            '<p>abcdefgh[<a href="http://s">http://s</a>://</p>\n',
        ),
        (
            "abcdefghi[https://s://",
            '<p>abcdefghi[<a href="https://s">https://s</a>://</p>\n',
        ),
        # image labels are validated the same way
        (
            "abcdefgh![http://s://",
            '<p>abcdefgh![<a href="http://s">http://s</a>://</p>\n',
        ),
    ],
)
def test_linkify_advances_after_scheme_before_link_label(src: str, expected: str):
    """The rule must move forward when it runs while a link label is validated."""
    assert MarkdownIt("gfm-like").render(src) == expected
