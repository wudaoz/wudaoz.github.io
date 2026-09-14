from html.parser import HTMLParser
from pathlib import Path
import unittest


class PublicationsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_section = False
        self.section_depth = 0
        self.in_list = False
        self.current = None
        self.active_field = None
        self.in_author_strong = False
        self.in_author_sup = False
        self.entries = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = attributes.get("class", "").split()

        if tag == "div" and attributes.get("id") == "publications":
            self.in_section = True
            self.section_depth = 1
            return

        if not self.in_section:
            return

        if tag == "div":
            self.section_depth += 1

        if tag == "ol" and "bibliography" in classes:
            self.in_list = True
        elif tag == "li" and self.in_list:
            self.current = {
                "title": [],
                "href": None,
                "author": [],
                "bold_author": [],
                "author_sup_count": 0,
                "venue_short": [],
                "venue_full": [],
                "venue_ranking": [],
            }
        elif tag == "div" and self.current:
            for field in (
                "title",
                "author",
                "venue_short",
                "venue_full",
                "venue_ranking",
            ):
                if field in classes:
                    self.active_field = field
        elif tag == "a" and self.current and self.active_field == "title":
            self.current["href"] = attributes.get("href")
        elif tag == "strong" and self.current and self.active_field == "author":
            self.in_author_strong = True
        elif tag == "sup" and self.current and self.active_field == "author":
            self.current["author_sup_count"] += 1
            self.in_author_sup = True

    def handle_endtag(self, tag):
        if not self.in_section:
            return

        if tag == "strong":
            self.in_author_strong = False
        elif tag == "sup":
            self.in_author_sup = False
        elif tag == "li" and self.current:
            self.entries.append(self.current)
            self.current = None
            self.active_field = None
        elif tag == "ol":
            self.in_list = False
        elif tag == "div":
            self.section_depth -= 1
            if self.section_depth == 0:
                self.in_section = False

    def handle_data(self, data):
        if not self.current or not self.active_field:
            return

        self.current[self.active_field].append(data)
        if (
            self.active_field == "author"
            and self.in_author_strong
            and not self.in_author_sup
        ):
            self.current["bold_author"].append(data)


def normalized(parts):
    return " ".join("".join(parts).split())


class PublicationsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (Path(__file__).resolve().parents[1] / "index.html").read_text(
            encoding="utf-8"
        )
        parser = PublicationsParser()
        parser.feed(cls.html)
        cls.entries = parser.entries

    def test_selected_publications_are_in_reverse_chronological_order(self):
        expected_titles = [
            "Cutting the Fuse: Actionable APT Attack Blocking in Provenance-based IDS",
            "Sentient: Detecting APTs Via Capturing Indirect Dependencies and Behavioral Logic",
            "SAURONEYES: Disentangling Voluminous Logs to Unveil Camouflaged Attack Intentions",
            "Brewing Vodka: Distilling Pure Knowledge for Lightweight Threat Detection in Audit Logs",
        ]

        self.assertEqual(
            [normalized(entry["title"]) for entry in self.entries], expected_titles
        )

    def test_titles_link_to_https_sources(self):
        self.assertEqual(len(self.entries), 4)
        for entry in self.entries:
            self.assertIsNotNone(entry["href"])
            self.assertTrue(entry["href"].startswith("https://"))

        self.assertNotIn("BTDA:", self.html)
        self.assertNotIn("ICASSP55912", self.html)

    def test_weiheng_wu_is_bold_and_equal_contribution_is_marked(self):
        for entry in self.entries:
            self.assertEqual(normalized(entry["bold_author"]), "Weiheng Wu")

        sauroneyes = self.entries[2]
        self.assertEqual(sauroneyes["author_sup_count"], 2)
        self.assertIn("* indicates equal contribution.", self.html)

    def test_venue_names_and_rankings_use_separate_lines(self):
        expected_venues = [
            (
                "USENIX Security 2026",
                "35th USENIX Security Symposium",
                "CCF-A · CORE A*",
            ),
            (
                "AAAI 2026",
                "40th AAAI Conference on Artificial Intelligence",
                "CCF-A · CORE A*",
            ),
            (
                "IEEE TIFS 2025",
                "IEEE Transactions on Information Forensics and Security",
                "CCF-A",
            ),
            (
                "WWW 2025",
                "The ACM Web Conference",
                "CCF-A · CORE A*",
            ),
        ]

        self.assertEqual(
            [
                (
                    normalized(entry["venue_short"]),
                    normalized(entry["venue_full"]),
                    normalized(entry["venue_ranking"]),
                )
                for entry in self.entries
            ],
            expected_venues,
        )


if __name__ == "__main__":
    unittest.main()
