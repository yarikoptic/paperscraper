import logging
import pandas as pd
import pytest
from scholarly._proxy_generator import MaxTriesExceededException


from paperscraper.scholar import (
    get_and_dump_scholar_papers,
    get_citations_from_title,
    get_scholar_papers,
)

logging.disable(logging.INFO)


@pytest.fixture(autouse=True)
def handle_scholar_exceptions(caplog):
    caplog.set_level(logging.INFO)
    try:
        yield
    except MaxTriesExceededException as e:
        logging.info(f"MaxTriesExceededException caught: {e}")
        pytest.skip("Skipping test due to MaxTriesExceededException")


class TestScholar:

    def test_citations(self):
        num = get_citations_from_title("GT4SD")
        assert isinstance(num, int)
        assert num > 0

    def test_dump_search(self, tmpdir):
        temp_dir = tmpdir.mkdir("scholar_papers")
        output_filepath = temp_dir.join("results.jsonl")
        get_and_dump_scholar_papers("GT4SD", str(output_filepath))
        assert output_filepath.check(file=1)

    def test_basic_search(self):
        results = get_scholar_papers("GT4SD")
        assert len(results) > 0  # Ensure we get some results
        assert isinstance(results, pd.DataFrame)
        assert all(
            [
                x in results.columns
                for x in [
                    "title",
                    "abstract",
                    "citations",
                    "year",
                    "authors",
                    "journal",
                ]
            ]
        )