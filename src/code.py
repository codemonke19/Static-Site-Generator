from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("invalid Markdown syntax")
        for i, part in enumerate(parts):
            if i % 2 == 0 and part != "":
                new_nodes.append(TextNode(text=part, text_type=TextType.TEXT))
            elif i % 2 != 0 and part != "":
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        images = extract_markdown_images(text)
        if not images:
            new_nodes.append(node)
            continue
        for (alt, url) in images:
            pattern = f"![{alt}]({url})"
            before, after = text.split(pattern, 1)
            if before != "":
                new_nodes.append(TextNode(before,TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = after
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        text = node.text
        links = extract_markdown_links(text)
        if not links:
            new_nodes.append(node)
            continue
        for (anchor, url) in links:
            pattern = f"[{anchor}]({url})"
            before, after = text.split(pattern, 1)
            if before != "":
                new_nodes.append(TextNode(before,TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            text = after
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    list_of_blocks = []
    for block in blocks:
        striped_block = block.strip()
        if striped_block != "":
            list_of_blocks.append(striped_block)
    return list_of_blocks
