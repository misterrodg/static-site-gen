import os
import shutil

def deploy():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(base_dir)

    public_dir = os.path.join(root_dir, "public")
    static_dir = os.path.join(root_dir, "static")

    for item in os.listdir(public_dir):
        item_path = os.path.join(public_dir, item)
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    shutil.copytree(static_dir, public_dir, dirs_exist_ok=True)

def main():
    deploy()

if __name__ == "__main__":
    main()

