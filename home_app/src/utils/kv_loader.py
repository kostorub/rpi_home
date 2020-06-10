import os

from kivy.lang import Builder


def load_all_kv(path):
    path = os.path.join(os.curdir, path)
    try:
        paths = os.listdir(path)
    except NotADirectoryError:
        return
    for item in paths:
        new_way = os.path.join(path, item)
        if item.endswith(".kv"):
            print(new_way)
            Builder.load_file(new_way)
        else:
            load_all_kv(new_way)
