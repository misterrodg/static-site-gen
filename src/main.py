import os
import shutil
import sys

from pathlib import Path

from parser import extract_title, markdown_to_html_node


base_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(base_dir)

content_dir = os.path.join(root_dir, "content")
docs_dir = os.path.join(root_dir, "docs")
static_dir = os.path.join(root_dir, "static")

def deploy():
    for item in os.listdir(docs_dir):
        item_path = os.path.join(docs_dir, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    shutil.copytree(static_dir, docs_dir, dirs_exist_ok=True)


def generate_page(file_name: str, base_path: str) -> None:
    from_path = os.path.join(content_dir,file_name)
    dest_path = os.path.join(docs_dir,file_name.replace(".md",".html"))
    template_path = os.path.join(root_dir,"template.html")

    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    markdown_file = ""
    with open(from_path,"r") as md:
        markdown_file = md.read()

    template_file = ""
    with open(template_path,"r") as tm:
        template_file = tm.read()

    title = extract_title(markdown_file)
    html_node = markdown_to_html_node(markdown_file)
    html = html_node.to_html()

    template_file = template_file.replace("{{ Title }}", title)
    template_file = template_file.replace("{{ Content }}", html)
    template_file = template_file.replace("href=\"/", f"href=\"{base_path}")
    template_file = template_file.replace("src=\"/", f"src=\"{base_path}")

    p = Path(dest_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path,"w") as f:
        f.write(template_file)

def main():
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    deploy()

    for root, _, files in os.walk(content_dir):
        for f in files:
            rel_path = os.path.relpath(os.path.join(root, f), content_dir)
            generate_page(rel_path, base_path)

if __name__ == "__main__":
    main()

