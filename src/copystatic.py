import os
import shutil

def dir_to_dir_transfer(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    if not os.path.exists(src):
        raise ValueError("src must be a valid directory")
    copy_dir_contents(src, dst)

def copy_dir_contents(src, dst):
    src_items = os.listdir(src)
    for item in src_items:
        item_path = os.path.join(src, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dst)
        elif os.path.isdir(item_path):
            dst_sub_dir = os.path.join(dst, item)
            os.mkdir(dst_sub_dir)
            copy_dir_contents(item_path, dst_sub_dir)