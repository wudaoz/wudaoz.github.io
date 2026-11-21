from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def front_matter(path):
    match = FRONT_MATTER.match(path.read_text(encoding="utf-8"))
    return match.group(1) if match else None


class BlogStructureTest(unittest.TestCase):
    def test_site_config_routes_posts_under_blog(self):
        config = (ROOT / "_config.yml").read_text(encoding="utf-8")
        self.assertIn("permalink: /blog/:year/:month/:title/", config)
        self.assertIn("layout: post", config)
        self.assertIn('url: "https://wudaoz.github.io"', config)

    def test_layouts_render_page_content(self):
        default = (ROOT / "_layouts/default.html").read_text(encoding="utf-8")
        post = (ROOT / "_layouts/post.html").read_text(encoding="utf-8")
        self.assertIn("{{ content }}", default)
        self.assertIn("assets/css/blog.css", default)
        self.assertIn("layout: default", front_matter(ROOT / "_layouts/post.html"))
        self.assertIn("{{ content }}", post)
        self.assertIn("page.title", post)

    def test_blog_index_lists_all_posts(self):
        index = ROOT / "blog/index.html"
        matter = front_matter(index)
        self.assertIsNotNone(matter)
        self.assertIn("layout: default", matter)
        self.assertIn("permalink: /blog/", matter)
        self.assertIn("{% for post in site.posts %}", index.read_text(encoding="utf-8"))

    def test_posts_are_named_and_described(self):
        posts = sorted((ROOT / "_posts").glob("*.md"))
        self.assertGreaterEqual(len(posts), 1)
        for post in posts:
            self.assertRegex(post.name, r"^\d{4}-\d{2}-\d{2}-[a-z0-9-]+\.md$")
            matter = front_matter(post)
            self.assertIsNotNone(matter, post.name)
            self.assertRegex(matter, r"(?m)^title: .+", post.name)
            date = re.search(r"(?m)^date: (\d{4}-\d{2}-\d{2})", matter)
            self.assertIsNotNone(date, post.name)
            self.assertEqual(date.group(1), post.name[:10], post.name)

    def test_homepage_shows_latest_posts_and_links_to_blog(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertTrue(html.startswith("---\n"), "index.html needs front matter")
        self.assertIn("{% for post in site.posts limit:3 %}", html)
        self.assertIn('<a href="./blog/">All posts &rarr;</a>', html)


if __name__ == "__main__":
    unittest.main()
