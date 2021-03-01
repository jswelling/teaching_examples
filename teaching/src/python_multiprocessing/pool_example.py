#!/usr/bin/env python

from multiprocessing import Pool
from pathlib import Path
import hashlib

NPROCS = 5

def compute_md5sum(file_path):
    # BUF_SIZE is totally arbitrary, change for your app!
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    md5 = hashlib.md5()

    if file_path.is_file():
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)

    return str(file_path), md5.hexdigest()


def path_gen(dir_path):
    for filepath in dir_path.glob('**/*'):
        yield filepath.absolute()

def main():
    dir_path = Path('/tmp')
    with Pool(processes=NPROCS) as pool:
        for file_name, hashcode in pool.imap_unordered(compute_md5sum,
                                                       path_gen(dir_path)):
            print(file_name, hashcode)
                                                       

if __name__ == "__main__":
    main()
