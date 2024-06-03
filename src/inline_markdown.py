
from textnode import TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    valid_types = {"text": "text", "code": "code", "italic": "italic", "bold": "bold"}
    
    if text_type not in valid_types:
        raise Exception("Invalid text type")

    retList = []
    
    delimited_type = "invalid"
    if delimiter == "`":
        delimited_type = valid_types["code"]
    elif delimiter == "*":
        delimited_type = valid_types["italic"] 
    elif delimiter == "**":
        delimited_type = valid_types["bold"]
    
    for node in old_nodes:
        # Skip any node not of text type
        if node.text_type != "text":
            retList.append(node)
            continue
        
        split_text = node.text.split(delimiter)
        # If the text doesn't contain the delimiter, add the node as is
        if len(split_text) == 1:
            retList.append(node)
            continue
        
        # Process the node splitting by delimiter
        state = 0  # 0 means text, 1 means delimited text
        for i, segment in enumerate(split_text):
            if state == 0:
                if segment != "":
                    retList.append(TextNode(segment, "text"))
                if i != len(split_text)-1:
                    state = 1 #do not update the last one
            else:
                if segment != "":
                    retList.append(TextNode(segment, delimited_type))
                if i != len(split_text)-1:
                    state = 0 #do not update the last one
        if state == 1:
            raise Exception(f"missing clossing {delimiter}\nfor text:{node.text}\ndelimiter:{delimiter}\ndelimiter_type:{delimited_type}\nstate={state}\n{retList}")
    return retList

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    return split_nodes_image_link(old_nodes,"image")
def split_nodes_link(old_nodes):
    return split_nodes_image_link(old_nodes,"link")
def split_nodes_image_link(old_nodes,node_type):
    retList = []
    for node in old_nodes:
        if node_type == "link":
            extracted_nodes = extract_markdown_links(node.text)
        else:
            extracted_nodes = extract_markdown_images(node.text)
        if len(extracted_nodes) == 0:
            retList.append(node)
            continue
        node_text = node.text
        for ei in extracted_nodes:
            split_text = node_text.split(f"{"!" if node_type != "link" else ""}[{ei[0]}]({ei[1]})",1)
            if len(split_text) == 1:
                retList.append(node)
                continue
            if split_text[0] != "":
                retList.append(TextNode(split_text[0],"text"))
            retList.append(TextNode(ei[0], "link" if node_type == "link" else "image", ei[1]))
            node_text = split_text[1]
        if len(node_text) > 0:
            retList.append(TextNode(node_text,"text"))
    return retList

def text_to_textnodes(text):
    nodes = [TextNode(text, "text")]
    for delimeter in ["**","*","`"]:
        nodes = split_nodes_delimiter(nodes,delimeter,"text")
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

# Example for testing:
# node = TextNode("This is `code` block", "text")
# new_nodes = split_nodes_delimiter([node], "`", "code")
# print(new_nodes)
# node = TextNode("`code` block aaaa `more code block` bbbb `and more here`", "text")
# new_nodes = split_nodes_delimiter([node], "`", "code")
# print(new_nodes)
# node = TextNode("this is a bad code block `code block", "text")
# new_nodes = split_nodes_delimiter([node], "`", "code")
# print(new_nodes)
# print('**bb** aaa'.split("**"))

# node = TextNode(
#     "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and some text here",
#     "text",
# )
# new_nodes = split_nodes_image([node])
# print(new_nodes)
# node = TextNode(
#     "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
#     "text",
# )
# new_nodes = split_nodes_link([node])
# print(new_nodes)

# print(text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"))