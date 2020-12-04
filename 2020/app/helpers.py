import pathlib

root_path = pathlib.Path(__file__).parent.parent

def file_to_lines(*path_parts):
    return [d for d in file_raw(*path_parts) if d]


def file_raw(*path_parts):
    import functools
    target = functools.reduce(lambda a,b: a/b, path_parts, root_path)

    with open(target, 'r') as handle:
        data = handle.read()

    return [d.strip() for d in data.split('\n')]
