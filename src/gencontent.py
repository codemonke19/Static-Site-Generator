import os
from markdown import heading_counter, markdown_to_html_node
from htmlnode import HTMLNode, ParentNode

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("#"):
            count = heading_counter(line)
            if count == 1:
                temp = line.lstrip("#")
                title = temp.strip()
                return title
    raise Exception("Markdown file needs a title")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating from {from_path} to {dest_path} using {template_path}")
    md = open(from_path).read()
    template = open(template_path).read()
    html_node = markdown_to_html_node(md)
    html_string = html_node.to_html()
    title = extract_title(md)
    temp = template.replace("{{ Title }}", title)
    html = temp.replace("{{ Content }}",html_string)
    dirpath = os.path.dirname(dest_path)
    if dirpath != "":
        os.makedirs(dirpath, exist_ok=True)
    dest = open(dest_path, "w")
    dest.write(html)
    dest.close()