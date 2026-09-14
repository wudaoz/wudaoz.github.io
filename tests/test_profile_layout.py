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

    def test_sidebar_uses_the_rectangular_portrait_photo(self):
        avatars = self.document.find_all(tag="img")
        portrait = next(
            (
                image
                for image in avatars
                if image.attrs.get("src") == "assets/img/weiheng-wu-portrait.jpg"
            ),
            None,
        )
        self.assertIsNotNone(portrait)
        self.assertEqual(portrait.attrs.get("alt"), "Portrait of Weiheng Wu")

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

        school_links = [
            link.attrs.get("href", "")
            for link in about[0].find_all(tag="a")
            if "ucas.ac.cn" in link.attrs.get("href", "")
            or "smu.edu.sg" in link.attrs.get("href", "")
        ]
        self.assertEqual(school_links, [])

    def test_google_scholar_profile_is_linked(self):
        scholar_links = [
            link.attrs.get("href")
            for link in self.document.find_all(tag="a")
            if link.attrs.get("title") == "Google Scholar"
        ]
        self.assertEqual(
            scholar_links,
            [
                "https://scholar.google.com.hk/citations?user=1LfIf6MAAAAJ&hl=zh-CN"
            ],
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

    def test_services_follow_publications_and_match_cv(self):
        sections = self.document.find_all(tag="div", class_name="section")
        section_ids = [section.attrs.get("id") for section in sections]
        self.assertLess(section_ids.index("publications"), section_ids.index("services"))
        self.assertLess(section_ids.index("services"), section_ids.index("research"))

        services = self.document.find_all(tag="div", element_id="services")
        self.assertEqual(len(services), 1)
        heading = services[0].find_all(tag="h3", class_name="section-title")
        self.assertEqual([node.text() for node in heading], ["Services"])
        self.assertIn("External Reviewer", services[0].text())
        self.assertIn("2023 - Present", services[0].text())

        labels = services[0].find_all(tag="dt")
        values = services[0].find_all(tag="dd")
        self.assertEqual([node.text() for node in labels], ["Journals", "Conferences"])
        self.assertEqual(
            [node.text() for node in values],
            [
                "IEEE TDSC · IEEE TIFS · IEEE ToN · IEEE TASE · IEEE ToR",
                "WWW 2025 & 2026 · AAAI 2026 & 2027 · ICASSP 2026",
            ],
        )


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


class TypographyStyleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.css = (ROOT / "assets/css/theme-claude.css").read_text(encoding="utf-8")

    def test_approved_google_fonts_are_loaded(self):
        self.assertIn(
            "family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600",
            self.html,
        )
        self.assertIn("family=Source+Sans+3:wght@400;500;600;700", self.html)
        self.assertIn("display=swap", self.html)

    def test_active_theme_stylesheet_is_cache_busted(self):
        self.assertIn(
            'href="./assets/css/theme-claude.css?v=20260914-portrait"',
            self.html,
        )

    def test_theme_defines_editorial_and_interface_stacks(self):
        self.assertIn(
            '--claude-font-editorial: "Newsreader", Georgia, "Times New Roman", serif;',
            self.css,
        )
        self.assertIn(
            '--claude-font-interface: "Source Sans 3", -apple-system, '
            'BlinkMacSystemFont, "Segoe UI", sans-serif;',
            self.css,
        )

    def test_type_roles_are_mapped(self):
        self.assertRegex(
            self.css,
            r"body\.theme-claude\s*\{[^}]*font-family: "
            r"var\(--claude-font-editorial\);",
        )
        self.assertRegex(
            self.css,
            r"\.top-nav\s*\{[^}]*font-family: var\(--claude-font-interface\);",
        )
        self.assertRegex(
            self.css,
            r"\.publications\s*\{[^}]*font-family: "
            r"var\(--claude-font-interface\);",
        )
        self.assertRegex(
            self.css,
            r"\.site-footer\s*\{[^}]*font-family: "
            r"var\(--claude-font-interface\);",
        )

    def test_email_keeps_monospace_role(self):
        match = re.search(r"\.site-email\s*\{([^}]+)\}", self.css)
        self.assertIsNotNone(match)
        self.assertIn(
            'font-family: "Ubuntu Mono", "SF Mono", monospace;', match.group(1)
        )

    def test_selected_typography_metrics_match_the_1b_preview(self):
        expected_rules = {
            ".site-name": (
                "font-family: var(--claude-font-editorial);",
                "font-size: 31px;",
                "font-weight: 600;",
                "line-height: 1.05;",
            ),
            ".section-title": (
                "font-family: var(--claude-font-editorial);",
                "font-size: 20px;",
                "font-weight: 600;",
                "line-height: 1.2;",
            ),
            "#about-me .section-body": (
                "font-family: var(--claude-font-editorial);",
                "font-size: 17px;",
                "line-height: 1.55;",
            ),
        }

        for selector, declarations in expected_rules.items():
            match = re.search(re.escape(selector) + r"\s*\{([^}]+)\}", self.css)
            self.assertIsNotNone(match, selector)
            for declaration in declarations:
                self.assertIn(declaration, match.group(1), selector)

    def test_content_links_have_visible_hover_and_focus_states(self):
        base = re.search(r"\.section-body a\s*\{([^}]+)\}", self.css)
        self.assertIsNotNone(base)
        self.assertIn("color: var(--claude-text);", base.group(1))
        self.assertIn("transition: color 0.18s ease;", base.group(1))

        self.assertRegex(
            self.css,
            r"\.section-body a:hover,\s*body\.theme-claude "
            r"\.section-body a:focus-visible\s*\{[^}]*"
            r"color: var\(--claude-accent\);",
        )
        self.assertRegex(
            self.css,
            r"\.section-body a strong\s*\{[^}]*color: inherit;",
        )

    def test_venue_and_services_styles_are_defined(self):
        for selector in (".venue-full", ".venue-ranking"):
            match = re.search(re.escape(selector) + r"\s*\{([^}]+)\}", self.css)
            self.assertIsNotNone(match, selector)
            self.assertIn("color: var(--claude-secondary);", match.group(1), selector)

        self.assertIn("body.theme-claude .services-list", self.css)
        self.assertRegex(
            self.css,
            r"@media \(max-width: 640px\)[\s\S]*"
            r"\.services-list > div\s*\{[^}]*grid-template-columns: 1fr;",
        )

    def test_portrait_dimensions_are_rectangular_and_responsive(self):
        frame = re.search(r"\.image\.avatar\s*\{([^}]+)\}", self.css)
        self.assertIsNotNone(frame)
        self.assertIn("width: 220px;", frame.group(1))
        self.assertIn("height: 280px;", frame.group(1))
        self.assertIn("overflow: hidden;", frame.group(1))
        self.assertIn("border-radius: 0;", frame.group(1))

        image = re.search(r"\.image\.avatar img\s*\{([^}]+)\}", self.css)
        self.assertIsNotNone(image)
        self.assertIn("width: 100%;", image.group(1))
        self.assertIn("height: 100%;", image.group(1))
        self.assertIn("object-position: center;", image.group(1))
        self.assertIn("transform: scale(1.25);", image.group(1))
        self.assertIn("transform-origin: 50% 44%;", image.group(1))

        tablet_css = self.css.split("@media (max-width: 1080px)", 1)[1].split(
            "@media (max-width: 640px)", 1
        )[0]
        tablet = re.search(r"\.image\.avatar\s*\{([^}]+)\}", tablet_css)
        self.assertIsNotNone(tablet)
        self.assertIn("width: 170px;", tablet.group(1))
        self.assertIn("height: 216px;", tablet.group(1))

        mobile_css = self.css.split("@media (max-width: 480px)", 1)[1]
        mobile = re.search(r"\.image\.avatar\s*\{([^}]+)\}", mobile_css)
        self.assertIsNotNone(mobile)
        self.assertIn("width: 150px;", mobile.group(1))
        self.assertIn("height: 190px;", mobile.group(1))


if __name__ == "__main__":
    unittest.main()
