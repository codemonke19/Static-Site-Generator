import unittest
from gencontent import extract_title

class TestBlockToBlockType(unittest.TestCase):
    def test_extract_title1(self):
        md = """
## some text
# some other text
### some more text
"""
        title = extract_title(md)
        self.assertEqual(title, "some other text")

    def test_extract_title2(self):
        md = """
## Blog posts

- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)
- [Why Tom Bombadil Was a Mistake](/blog/tom)
- [The Unparalleled Majesty of "The Lord of the Rings"](/blog/majesty)
"""
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()