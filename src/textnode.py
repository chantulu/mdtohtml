from htmlnode import LeafNode

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text;
        self.text_type = text_type;
        self.url = url;

    def __eq__(self, other_node):
        return (
                self.text == other_node.text
                and self.text_type == other_node.text_type
                and self.url == other_node.url
                )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


def text_node_to_html_node(text_node):
    valid_types = ["text","bold","italic","code","link","image"]
    if text_node.text_type not in valid_types:
        raise Exception("invalid text node type")
    if text_node.text_type == valid_types[0]:
        return LeafNode(None,text_node.text)
    if text_node.text_type == valid_types[1]:
        return LeafNode("b",text_node.text)
    if text_node.text_type == valid_types[2]:
        return LeafNode("i",text_node.text)
    if text_node.text_type == valid_types[3]:
        return LeafNode("code",text_node.text)
    if text_node.text_type == valid_types[4]:
        return LeafNode("a",text_node.text,{"href": text_node.url, "alt": text_node.text})
    if text_node.text_type == valid_types[5]:
        return LeafNode("img",text_node.text,{"src": text_node.url})



