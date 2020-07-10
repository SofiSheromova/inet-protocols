import string
import argparse

alphabet = string.ascii_uppercase + string.ascii_lowercase + \
           string.digits + '+/'


def split_into_chunks(inp_str, chunk_size, fill_char=''):
    splitted = []
    for i in range(0, len(inp_str), chunk_size):
        splitted.append(inp_str[i:i + chunk_size])
    if splitted and fill_char:
        splitted[-1] = splitted[-1].ljust(chunk_size, fill_char)
    return splitted


def utf8_to_base64(inp_str):
    bin_str = ''.join([f"{x:08b}" for x in inp_str.encode('UTF-8')])
    splitted = split_into_chunks(bin_str, 6, '0')
    enc_str = ''.join([alphabet[int(el, 2)] for el in splitted])
    base64_str = enc_str.ljust(len(enc_str) + (4 - len(enc_str) % 4) % 4, '=')
    return base64_str


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'text', type=str, nargs=1,
        help='This text to be encrypted. If the text contains spaces, '
             'use double quotation marks.'
    )

    args = parser.parse_args()
    print(utf8_to_base64(args.text[0]))
