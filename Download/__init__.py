#!/usr/bin/env python
import gzip
import os
import tempfile
import urllib.request
import subprocess


def downloadFile(url: str) -> str:
    tmpName = tempfile.mkstemp(suffix=".pyJParse")
    os.close(tmpName[0])
    tmpName = tmpName[1]
    with urllib.request.urlopen(url) as response:
        with gzip.GzipFile(fileobj=response) as uncompressed:
            file_header = uncompressed.read()
            with open(tmpName, "wb") as f:
                f.write(file_header)
    return tmpName


def cleanup(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)