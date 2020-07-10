import unittest
import base64
from base64_encoder import utf8_to_base64 as custom_encoder


def standard_encoder(inp_str):
    inp_bytes = inp_str.encode("UTF-8")

    encoded_bytes = base64.b64encode(inp_bytes)
    encoded_str = encoded_bytes.decode("UTF-8")

    return encoded_str


class TestEncoder(unittest.TestCase):
    def setUp(self):
        self.arr = [
            '',
            'hello, world!',
            'Man is distinguished, not only by his reason, but by this singular passion from other animals, which is a lust of the mind, that by a perseverance of delight in the continued and indefatigable generation of knowledge, exceeds the short vehemence of any carnal pleasure.',
            'Строка с русскими буквами.',
            '✌ ☀'
        ]

    def test_encoder(self):
        for text in self.arr:
            self.assertEqual(standard_encoder(text), custom_encoder(text))


if __name__ == '__main__':
    unittest.main()
