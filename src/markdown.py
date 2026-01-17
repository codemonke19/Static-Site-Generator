from enum import Enum
from htmlnode import HTMLNode, ParentNode, text_node_to_html_node
from code import markdown_to_blocks, text_to_textnodes
from textnode import TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def heading_counter(text):
    count = 0
    for character in text:
        if character == "#":
            count += 1
        else:
            break
    return count

def line_cleaner(text, character):
    lines = text.split("\n")
    stripped_lines = []
    for line in lines:
        stripped_line = line.lstrip(f"{character} ")
        if stripped_line != "":
            stripped_lines.append(stripped_line)
    return stripped_lines

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith("#"):
        count = heading_counter(lines[0])
        if 1 <= count <= 6 and len(lines[0]) > count and lines[0][count] == " ":
            return BlockType.HEADING
    if block.startswith("```"):
        if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
            return BlockType.CODE
    if block.startswith("> "):
        is_quote = True
        for line in lines:
            if not line.startswith("> "):
                is_quote = False
                break
        if is_quote:
            return BlockType.QUOTE
    if block.startswith("- "):
        is_unordered_list = True
        for line in lines:
            if not line.startswith("- "):
                is_unordered_list = False
                break
        if is_unordered_list:
            return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        is_ordered_list = True
        expected = 1
        for line in lines:
            if line.startswith(f"{expected}. "):
                expected += 1
            else:
                is_ordered_list = False
                break
        if is_ordered_list:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            paragraph_text = " ".join(block.split("\n"))
            text_nodes = text_to_textnodes(paragraph_text)
            inline_child = []
            for node in text_nodes:
                inline_child.append(text_node_to_html_node(node))
            children.append(ParentNode("p", inline_child))
        elif block_type == BlockType.HEADING:
            count = heading_counter(block)
            heading_text = block[count + 1:]
            text_nodes = text_to_textnodes(heading_text)
            inline_child = []
            for node in text_nodes:
                inline_child.append(text_node_to_html_node(node))
            children.append(ParentNode(f"h{count}", inline_child))
        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            inner_text = "\n".join(lines[1:-1]) + "\n"
            text_node = TextNode(inner_text, TextType.CODE)
            code_node = text_node_to_html_node(text_node)
            children.append(ParentNode("pre", [code_node]))
        elif block_type == BlockType.QUOTE:
            stripped_lines = line_cleaner(block, ">")
            quote_text = " ".join(stripped_lines)
            text_nodes = text_to_textnodes(quote_text)
            inline_child = []
            for node in text_nodes:
                inline_child.append(text_node_to_html_node(node))
            children.append(ParentNode("blockquote", inline_child))
        elif block_type == BlockType.UNORDERED_LIST:
            list_items = line_cleaner(block, "-")
            li_nodes = []
            for item_text in  list_items:
                text_nodes = text_to_textnodes(item_text)
                inline_child = []
                for node in text_nodes:
                    inline_child.append(text_node_to_html_node(node))
                li_nodes.append(ParentNode("li", inline_child))  
            children.append(ParentNode("ul", li_nodes))
        elif block_type == BlockType.ORDERED_LIST:
            items = []
            for line in block.split("\n"):
                line = line.strip()
                if not line:
                    continue
                dot_index = line.find(". ")
                if dot_index != -1:
                    item_text = line[dot_index + 2:]
                    items.append(item_text)
            li_nodes = []
            for item_text in items:
                text_nodes = text_to_textnodes(item_text)
                inline_children = []
                for node in text_nodes:
                    inline_children.append(text_node_to_html_node(node))
                li_nodes.append(ParentNode("li", inline_children))
            children.append(ParentNode("ol", li_nodes))


    return ParentNode("div", children)
            
        
