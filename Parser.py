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
    parser.add_argument("--noautoconfig", type=str, help="Don't parse autoconfig")
    parser.add_argument("--noserverinfo", type=str, help="Don't parse serverinfo")
    parser.add_argument("--noevents", type=str, help="Don't parse events")
    parser.add_argument("--nochangelog", type=str, help="Don't parse changelog")
    parser.add_argument("--nosync", type=str, help="Don't parse sync")
    args = parser.parse_args()

    url = args.url
    parsed_url = urlparse(url)

    scheme: str = parsed_url.scheme
    scheme = scheme.capitalize()

    pAutoconfig = True if args.noautoconfig is None else False
    pServerinfo = True if args.noserverinfo is None else False
    pEvents = True if args.noevents is None else False
    pChangelog = True if args.nochangelog is None else False
    pSync = True if args.nosync is None else False

    x = repository.parse(url, scheme, parseAutoconf=pAutoconfig, parseServerinfo=pServerinfo, parseEvents=pEvents,
                         parseChangelog=pChangelog, parseSync=pSync)
    x["TYPE"] = "A3S"
    x["VERSION"] = "1.0.0"  # Change major on any change, that breaks json parsing !
    x_j = json.dumps(x, indent=True)

    with open(args.filename, "w") as f:
        f.write(x_j)
