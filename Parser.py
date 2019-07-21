#!/usr/bin/env python
import argparse
import json
from urllib.parse import urlparse

import repository

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", metavar='url', type=str,
                        help="Examples: ftp://arma.example.com/.a3s/ or http://arma3.example.ru/test/.a3s")
    parser.add_argument("filename", metavar='filename', type=str, help="Output filename")
    args = parser.parse_args()

    url = args.url
    parsed_url = urlparse(url)

    scheme: str = parsed_url.scheme
    scheme = scheme.capitalize()

    x = repository.parse(url, scheme)
    x_j = json.dumps(x, indent=True)

    with open(args.filename, "w") as f:
        f.write(x_j)
