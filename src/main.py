from copystatic import dir_to_dir_transfer
from gencontent import generate_pages_recursive

def main():
    dir_to_dir_transfer(
        "./static",
        "./public",
        )
    generate_pages_recursive(
        "./content",
        "./template.html",
        "./public"
        )
main()
