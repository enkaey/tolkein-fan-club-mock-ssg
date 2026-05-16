import os
import shutil

def delete_and_recreate(dir: str = "public") -> None:
    abs_path = os.path.abspath(dir)

    # Only try to delete if the directory actually exists
    if os.path.exists(abs_path):
        shutil.rmtree(abs_path)

    # Recreate it fresh
    os.mkdir(abs_path)

def copy_static_files(src: str = "static", dst: str = "public") -> None:
    # Create a clean-slate EXACTLY ONCE for the public directory
    delete_and_recreate(dst)

    # Start the recursion from the top
    recursive_copy(src, dst)


def recursive_copy(src: str, dst: str) -> None:
    # This helper only walks and copies, it never deletes anything!
    abs_path_src =  os.path.abspath(src)
    abs_path_dst = os.path.abspath(dst)

    src_lsd = os.listdir(abs_path_src)

    for child in src_lsd:
        full_child_path = os.path.join(abs_path_src, child)
        full_child_path_dst = os.path.join(abs_path_dst, child)
        
        if os.path.isfile(full_child_path):
            shutil.copy(full_child_path, full_child_path_dst, follow_symlinks=True)

        if os.path.isdir(full_child_path):
            os.mkdir(full_child_path_dst)
            recursive_copy(full_child_path, full_child_path_dst)