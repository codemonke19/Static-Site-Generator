from enum import Enum

class TextType(Enum)
    PLAIN_TEXT = "text"
    BOLD_TEXT = "**text**"
    ITALIC_TEXT = "_text_"
    CODE_TEXT = "`text`"
    LINKS = "[anchor text](url)"
    IMAGES = "![alt text](url)"

class TextNode()