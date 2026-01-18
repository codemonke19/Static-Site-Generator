from copystatic import dir_to_dir_transfer
from gencontent import generate_pages_recursive
import sys

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    dir_to_dir_transfer(
        "./static",
        "./docs",
        )
    generate_pages_recursive(
        "./content",
        "./template.html",
        "./docs",
        basepath
        )
main()
