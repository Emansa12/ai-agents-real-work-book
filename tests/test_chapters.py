"""Tests for chapter list configuration."""

from src.chapters import CHAPTERS, all_chapter_indices, get_chapter_by_index


def test_chapter_list_not_empty() -> None:
    assert len(CHAPTERS) > 0


def test_chapter_titles_unique() -> None:
    titles = [chapter.title for chapter in CHAPTERS]
    assert len(titles) == len(set(titles))


def test_includes_bidi_chapter() -> None:
    titles = [chapter.title.lower() for chapter in CHAPTERS]
    assert any("hebrew" in title and "english" in title for title in titles)


def test_no_static_lecture_body_wording() -> None:
    forbidden = (
        "copy this lecture",
        "use the course pdf as primary source",
        "static lecture body",
    )
    for chapter in CHAPTERS:
        title_lower = chapter.title.lower()
        for phrase in forbidden:
            assert phrase not in title_lower


def test_get_chapter_by_index() -> None:
    chapter = get_chapter_by_index(1)
    assert chapter.index == 1
    assert "Introduction" in chapter.title


def test_all_chapter_indices() -> None:
    indices = all_chapter_indices()
    assert indices == list(range(1, len(CHAPTERS) + 1))
