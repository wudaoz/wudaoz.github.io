from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class Node:
    def __init__(self, tag="document", attrs=None, parent=None):
        self.tag = tag
        self.attrs = dict(attrs or [])
        self.parent = parent
        self.children = []

    def text(self):
        parts = []
        for child in self.children:
            parts.append(child.text() if isinstance(child, Node) else child)
        return " ".join("".join(parts).split())

    def has_class(self, class_name):
        return class_name in self.attrs.get("class", "").split()

    def find_all(self, tag=None, element_id=None, class_name=None):
        matches = []
        for child in self.children:
            if not isinstance(child, Node):
                continue
            if (
                (tag is None or child.tag == tag)
                and (element_id is None or child.attrs.get("id") == element_id)
                and (class_name is None or child.has_class(class_name))
            ):
                matches.append(child)
            matches.extend(child.find_all(tag, element_id, class_name))
        return matches


class DocumentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.root = Node()
        self.current = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.current)
        self.current.children.append(node)
        if tag not in VOID_TAGS:
            self.current = node

    def handle_endtag(self, tag):
        node = self.current
        while node is not self.root and node.tag != tag:
            node = node.parent
        if node is not self.root:
            self.current = node.parent

    def handle_data(self, data):
        self.current.children.append(data)


def parse_document():
    parser = DocumentParser()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    return parser.root


class ProfileContentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = parse_document()

    def test_navigation_uses_local_safe_homepage_link(self):
        links = self.document.find_all(tag="a")
        homepage = next(
            (link for link in links if link.text() == "Wu's Homepage"), None
        )
        self.assertIsNotNone(homepage)
        self.assertEqual(homepage.attrs.get("href"), "./index.html")

    def test_smu_email_is_displayed_and_linked(self):
        email_text = self.document.find_all(tag="p", class_name="site-email")
        self.assertEqual([node.text() for node in email_text], ["whwu [at] smu.edu.sg"])

        email_links = [
            node.attrs.get("href")
            for node in self.document.find_all(tag="a")
            if node.attrs.get("title") == "Email"
        ]
        self.assertEqual(email_links, ["mailto:whwu@smu.edu.sg"])

    def test_about_me_describes_research_and_david_lo(self):
        about = self.document.find_all(tag="div", element_id="about-me")
        self.assertEqual(len(about), 1)
        about_text = about[0].text()
        self.assertIn("intrusion detection systems for network security", about_text)
        self.assertIn("security issues in AI and agents", about_text)
        self.assertIn("Prof. David Lo (ACM and IEEE Fellow)", about_text)

        david_links = [
            link
            for link in about[0].find_all(tag="a")
            if link.text() == "Prof. David Lo"
        ]
        self.assertEqual(len(david_links), 1)
        self.assertEqual(
            david_links[0].attrs.get("href"),
            "http://www.mysmu.edu/faculty/davidlo/",
        )

    def test_metadata_reflects_current_research(self):
        metadata = {
            node.attrs.get("name"): node.attrs.get("content", "")
            for node in self.document.find_all(tag="meta")
            if node.attrs.get("name")
        }
        self.assertIn("AI and agent security", metadata["description"])
        self.assertIn("Agent Security", metadata["keywords"])

    def test_education_and_experience_share_one_timeline(self):
        sections = self.document.find_all(tag="div", class_name="section")
        section_ids = [section.attrs.get("id") for section in sections]
        self.assertIn("education-experience", section_ids)
        self.assertNotIn("education", section_ids)
        self.assertNotIn("experience", section_ids)

        merged = self.document.find_all(tag="div", element_id="education-experience")
        self.assertEqual(len(merged), 1)
        heading = merged[0].find_all(tag="h3", class_name="section-title")
        self.assertEqual([node.text() for node in heading], ["Education & Experience"])

        timeline_items = merged[0].find_all(tag="div", class_name="timeline-item")
        expected_leads = [
            "Singapore Management University (SMU)",
            "Alibaba Group",
            "University of Chinese Academy of Sciences (UCAS)",
            "Shenzhen University (SZU)",
        ]
        self.assertEqual(len(timeline_items), 4)
        self.assertEqual(
            [
                item.find_all(tag="p", class_name="exp-title")[0].text()
                for item in timeline_items
            ],
            expected_leads,
        )

    def test_publications_heading_is_selected_publications(self):
        publications = self.document.find_all(tag="div", element_id="publications")
        heading = publications[0].find_all(tag="h3", class_name="section-title")
        self.assertEqual([node.text() for node in heading], ["Selected Publications"])


class TimelineStyleTest(unittest.TestCase):
    def test_marker_is_centered_on_line_in_both_stylesheets(self):
        for relative_path in (
            "assets/css/theme-claude.css",
            "assets/css/style-no-dark-mode_old.css",
        ):
            css = (ROOT / relative_path).read_text(encoding="utf-8")
            match = re.search(r"\.timeline-item::after\s*\{([^}]+)\}", css)
            self.assertIsNotNone(match, relative_path)
            declarations = match.group(1)
            self.assertIn("box-sizing: border-box;", declarations, relative_path)
            self.assertIn("left: -25px;", declarations, relative_path)
            self.assertIn("width: 12px;", declarations, relative_path)
            self.assertIn("height: 12px;", declarations, relative_path)


if __name__ == "__main__":
    unittest.main()
