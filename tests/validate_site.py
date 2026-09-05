#!/usr/bin/env python3
"""Dependency-free static checks for the published NightTalk support site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.ids, self.links, self.tags, self.canonical = path, set(), [], [], []
        self.stack = []
        self.feed(path.read_text())
        assert not self.stack, (path.name, "unclosed tags", self.stack)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append(tag)
        if tag not in {"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"}:
            self.stack.append(tag)
        if "id" in a:
            assert a["id"] not in self.ids, (self.path.name, "duplicate id", a["id"])
            self.ids.add(a["id"])
        if tag == "a":
            assert a.get("href"), (self.path.name, "empty href")
            self.links.append(a["href"])
        if tag == "link":
            if a.get("rel") == "canonical": self.canonical.append(a["href"])
            elif a.get("href"): self.links.append(a["href"])
        if tag == "html": assert a.get("lang") == "en"
        if tag == "img": assert "alt" in a
    def handle_endtag(self, tag):
        assert self.stack and self.stack.pop() == tag, (self.path.name, "unbalanced", tag)
pages = {p.name: Page(p) for p in ROOT.glob("*.html")}
expected = {"index.html","tutorial.html","documentation.html","support.html","privacy.html","terms.html","404.html"}
assert set(pages) == expected
count = 0
for name,p in pages.items():
    assert p.tags.count("h1") == 1, name
    assert p.tags.count("main") == 1 and "main-content" in p.ids, name
    assert "script" not in p.tags and "form" not in p.tags and "iframe" not in p.tags, name
    assert p.canonical == ["https://minh.systems/Nighttalk/" + ("" if name == "index.html" else name)]
    for required in ["tutorial.html","documentation.html","support.html","privacy.html","terms.html","mailto:mip@gmx.biz"]:
        assert required in p.links, (name, "missing navigation", required)
    for link in p.links:
        u = urlsplit(link)
        if u.scheme == "mailto":
            assert u.path == "mip@gmx.biz", (name, "unexpected support address")
        elif not u.scheme:
            target = ROOT / (unquote(u.path) or name)
            assert target.is_file(), (name, "broken link", link)
            if u.fragment: assert u.fragment in pages[target.name].ids, (name, "broken anchor",link)
        else: assert u.scheme == "https", (name, "insecure link",link)
        count += 1
sitemap = ET.parse(ROOT / "sitemap.xml")
urls = {n.text for n in sitemap.findall(".//{*}loc")}
assert urls == {p.canonical[0] for n,p in pages.items() if n != "404.html"}
css = (ROOT / "assets/styles.css").read_text()
assert "prefers-color-scheme:dark" in css and "prefers-reduced-motion:reduce" in css
assert "focus-visible" in css and "@media(max-width:700px)" in css
def luminance(s):
    rgb = [int(s[i:i+2],16)/255 for i in (1,3,5)]
    c = [v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4 for v in rgb]
    return sum(a*b for a,b in zip(c,[.2126,.7152,.0722]))
def contrast(a,b):
    x,y = sorted([luminance(a),luminance(b)])
    return (y+.05)/(x+.05)
pairs = [("#172e3b","#f4f7f8"),("#4f6571","#ffffff"),("#4f6571","#e8f0f2"),("#07564f","#ffffff"),
         ("#ffffff","#09675e"),("#e6f0f4","#0d202b"),("#aec2cc","#173442"),("#a7ebd5","#122b37"),
         ("#c9dde4","#0b242f"),("#0b302a","#a7ebd5"),("#b3cbd5","#0b242f")]
for a,b in pairs:
    assert contrast(a,b) >= 4.5, (a,b,contrast(a,b))
print(f"PASS: {len(pages)} pages; {count} links; sitemap; structure; email-only support; {len(pairs)} text contrast pairs.")
print("Static checks only: browser rendering, keyboard interaction, and screen-reader QA remain separate.")
