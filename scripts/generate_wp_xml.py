#!/usr/bin/env python3
"""
WordPress XML Compiler for Coverstar Kids Parties Local SEO Landing Pages.
Compiles HTML templates into a single WXR XML file for bulk importing into WordPress.
"""

import os
import re
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
from datetime import datetime

def extract_meta_content(html_content, tag_name, attr_name="name", attr_value=""):
    pattern = rf'<meta\s+{attr_name}=["\']{re.escape(attr_value)}["\']\s+content=["\'](.*?)["\']'
    match = re.search(pattern, html_content, re.IGNORECASE)
    if match:
        return match.group(1)
    return ""

def extract_title(html_content):
    match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
    if match:
        return match.group(1)
    return "Coverstar Kids Parties Landing Page"

def extract_body(html_content):
    match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return html_content.strip()

def build_wxr_xml(templates_dir, output_xml_path):
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pub_date = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

    xml_header = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"
    xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wp="http://wordpress.org/export/1.2/"
>
<channel>
    <title>Coverstar Kids Parties Export</title>
    <link>https://coverstarkidsparties.co.uk</link>
    <description>Local SEO Landing Pages for Coverstar Kids Parties Liverpool</description>
    <pubDate>{pub_date}</pubDate>
    <language>en-GB</language>
    <wp:wxr_version>1.2</wp:wxr_version>
    <wp:base_site_url>https://coverstarkidsparties.co.uk</wp:base_site_url>
    <wp:base_blog_url>https://coverstarkidsparties.co.uk</wp:base_blog_url>
    <wp:author>
        <wp:author_id>1</wp:author_id>
        <wp:author_login><![CDATA[admin]]></wp:author_login>
        <wp:author_email><![CDATA[admin@coverstarkidsparties.co.uk]]></wp:author_email>
        <wp:author_display_name><![CDATA[Coverstar Admin]]></wp:author_display_name>
    </wp:author>
"""

    items_xml = ""

    post_id = 1000
    for filename in sorted(os.listdir(templates_dir)):
        if not filename.endswith(".html") or filename.startswith("keyword"):
            continue

        file_path = os.path.join(templates_dir, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        page_title = extract_title(content)
        meta_desc = extract_meta_content(content, "meta", attr_name="name", attr_value="description")
        body_content = extract_body(content)

        slug = os.path.splitext(filename)[0].replace("-base", "")
        if slug == "index" or slug == "service":
            slug = "kids-parties-liverpool"

        post_id += 1

        items_xml += f"""
    <item>
        <title><![CDATA[{page_title}]]></title>
        <link>https://coverstarkidsparties.co.uk/{slug}/</link>
        <pubDate>{pub_date}</pubDate>
        <dc:creator><![CDATA[admin]]></dc:creator>
        <guid isPermaLink="false">https://coverstarkidsparties.co.uk/?page_id={post_id}</guid>
        <description></description>
        <content:encoded><![CDATA[{body_content}]]></content:encoded>
        <excerpt:encoded><![CDATA[]]></excerpt:encoded>
        <wp:post_id>{post_id}</wp:post_id>
        <wp:post_date><![CDATA[{now_str}]]></wp:post_date>
        <wp:post_date_gmt><![CDATA[{now_str}]]></wp:post_date_gmt>
        <wp:comment_status><![CDATA[closed]]></wp:comment_status>
        <wp:ping_status><![CDATA[closed]]></wp:ping_status>
        <wp:post_name><![CDATA[{slug}]]></wp:post_name>
        <wp:status><![CDATA[publish]]></wp:status>
        <wp:post_parent>0</wp:post_parent>
        <wp:menu_order>0</wp:menu_order>
        <wp:post_type><![CDATA[page]]></wp:post_type>
        <wp:post_password><![CDATA[]]></wp:post_password>
        <wp:is_sticky>0</wp:is_sticky>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_yoast_wpseo_title]]></wp:meta_key>
            <wp:meta_value><![CDATA[{page_title}]]></wp:meta_value>
        </wp:postmeta>
        <wp:postmeta>
            <wp:meta_key><![CDATA[_yoast_wpseo_metadesc]]></wp:meta_key>
            <wp:meta_value><![CDATA[{meta_desc}]]></wp:meta_value>
        </wp:postmeta>
    </item>
"""

    xml_footer = """
</channel>
</rss>
"""

    full_xml = xml_header + items_xml + xml_footer

    os.makedirs(os.path.dirname(output_xml_path), exist_ok=True)
    with open(output_xml_path, "w", encoding="utf-8") as f:
        f.write(full_xml)

    print(f"Successfully compiled WordPress XML export: {output_xml_path}")

if __name__ == "__main__":
    templates_directory = os.path.join(os.path.dirname(__file__), "..", "templates")
    output_path = os.path.join(os.path.dirname(__file__), "..", "coverstar_pages_import.xml")
    build_wxr_xml(templates_directory, output_path)
