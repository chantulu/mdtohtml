import re
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_blocks_longer(markdown):
    ret = []
    status = 0 # 0 = no block 1 = block
    block = ""
    for i,line in enumerate(markdown.split("\n")):
        if block.strip() != "" and status == 0:
            ret.append(block.strip())
            block = ""
        if line == "":
            status = 0
        if line.strip() != "":
            block += "\n"
            block += line
            status = 1
        if block.strip() != "" and i == len(markdown.split("\n")) -1:
            ret.append(block.strip()) # if we are left with something at the end append it
    return ret

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    re_heading = "^#{1,6}\\s.+"
    re_il = "^([0-9])\\.\\s.+"
    if block.strip().startswith("```") and block.strip().endswith("```"):
        return "code"
    if re.match(re_heading, block):
        return "heading"
    isquote = False
    isul = False
    prev_li = float('-inf')
    isli = False
    for line in block.split("\n"):
        if line.startswith(">"):
            isquote = True
        else:
            isquote = False
        if line.startswith("* ") or line.startswith("- "):
            isul = True
        else:
            isul = False
        if re.match(re_il, line):
            match = re.search(re_il, line)
            if prev_li == float("-inf"):
                prev_li = int(match.group(1))
                isli = True
            elif int(match.group(1)) == prev_li + 1:
                prev_li = int(match.group(1))
            else:
                isli = False
    if isquote == True:
        return "quote"
    if isul == True:
        return "unordered_list"
    if isli == True:
        return "ordered_list"
    return "paragraph"


def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def block_to_html_node(block, type):
    # 'code', 'heading', 'quote', 'unordered_list', 'ordered_list', 'paragraph'
    html_node = None
    hcount = 0
    if type == "heading":
        for i in range(0, len(block)):
            if block[i] == "#":
                hcount += 1
            else:
                break
        html_node = LeafNode(f"h{hcount}", block.replace("#"*hcount, "").strip())
        return html_node
    
    if type == "code":
       return ParentNode("code",[LeafNode("pre",block.strip("```"))])
    if type == "quote":
       raw_block = ""
       for line in block.split("\n"):
           raw_block += line.lstrip(">")
       return LeafNode("blockquote",raw_block.strip())
    if type == "unordered_list":
        leafNodes = []
        for line in block.split("\n"):
            line = line.lstrip("* ").lstrip("- ")
            children = text_to_children(line.replace("\n"," "))
            leafNodes.append(ParentNode("li",children))
        return ParentNode("ul", leafNodes)
    if type == "ordered_list":
        leafNodes = []
        for line in block.split("\n"):
            line = re.sub("^([0-9])\\.\\s","",line)
            children = text_to_children(line.replace("\n"," "))
            leafNodes.append(ParentNode("li",children))
        return ParentNode("ol", leafNodes)
    if type == "paragraph":
        return ParentNode("p",text_to_children(block.replace("\n"," ")))
    

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_node = block_to_html_node(block, block_type)
        nodes.append(html_node)
    return ParentNode("div",nodes)
