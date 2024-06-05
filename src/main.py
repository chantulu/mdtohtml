from block_markdown import markdown_to_html_node
from textnode import TextNode
from htmlnode import LeafNode
import os
import shutil
import re

def get_real_path(relative_path):
  """
  Converts a relative path to a real path using the os.path.realpath function.

  Args:
      relative_path (str): The relative path to convert.

  Returns:
      str: The real path on the system.
  """

  current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current directory
  real_path = os.path.realpath(os.path.join(current_dir, relative_path))
  return real_path

def main():
    # tnode = TextNode("This is a text node", "bold", "https://www.boot.dev")
    # print(tnode)
    copy_static()
    generate_page("../content/index.md","../template.html","../public/index.html")
    generate_pages_recursive()
    

def generate_pages_recursive(path = "", is_root=True):
    source = "content"
    if is_root == True:
        path=source
    child_items = []
    if os.path.isdir(path):
        child_items = os.listdir(path)
    for ci in child_items:
        ci_fp = path + "/" + ci
        if os.path.isfile(ci_fp) and ci_fp[-3:] == ".md":
            generate_page(f"../{ci_fp}","../template.html",f"../public{ci_fp[len(source):-2]}html")
        else:
            generate_pages_recursive(ci_fp,False)

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line.lstrip("# ")
    raise Exception("all pages must have an h1")

def generate_page(from_path, template_path, dest_path):
    from_path = get_real_path(from_path)
    template_path = get_real_path(template_path)
    dest_path = get_real_path(dest_path)
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as markdown:
        with open(template_path, "r") as template:
            mdn = markdown.read()
            title = extract_title(mdn)
            html = markdown_to_html_node(mdn).to_html()
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, "w") as destination:
                final_file = template.read().replace('{{ Title }}', title)
                final_file = final_file.replace("{{ Content }}", html)
                destination.write(final_file)

def copy_static(path = "", is_root=True):
    source = "static"
    dest = "public"
    if is_root == True:
        shutil.rmtree(dest)
        os.mkdir(dest)
        path=source
    child_items = []
    if os.path.isdir(path):
        child_items = os.listdir(path)
    for ci in child_items:
        ci_fp = path + "/" + ci
        if os.path.isfile(ci_fp):
            cp_dest = re.sub(f"^{source}",dest,ci_fp)
            os.makedirs(os.path.dirname(cp_dest), exist_ok=True)
            shutil.copy(ci_fp, cp_dest)
        else:
            copy_static(ci_fp,False)

main()