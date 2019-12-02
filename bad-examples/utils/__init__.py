import pathlib

base_path = pathlib.Path(__file__).parent

def load(filename):
    with open(base_path/filename) as handle:
        return handle.readlines()

def read(filename):
    with open(base_path/filename) as handle:
        return handle.read()

def destructure(obj, *params):
    import operator
    return operator.itemgetter(obj, *params)
