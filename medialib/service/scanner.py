import os
import json

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __repr__(self):
        return str(self.__dict__)

def scan_dir(path):
    metafile = 'metadata.json'
    mediadir  = '.media'
    medialist = []

    for root, dirs, files in os.walk(path, followlinks=True):
        if metafile in files:
            metastream = open(os.path.join(root, metafile), 'r')
            metadata = json.load(metastream)

            metadata['cover'] = os.path.realpath(os.path.join(root, metadata['cover']))

            for idx, val in enumerate(metadata['files']):
                metadata['files'][idx] = os.path.realpath(os.path.join(root, val))

            medialist.append(Struct(**metadata))
            next

        for dirname in dirs:
            if not dirname.endswith(mediadir):
                dirs.remove(dirname)

        dirs.sort()

    return medialist
