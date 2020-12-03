import pathlib

root_path = pathlib.Path(__file__).parent.parent

def file_to_lines(*path_parts):
    import functools
    target = functools.reduce(lambda a,b: a/b, path_parts, root_path)

    with open(target, 'r') as handle:
        data = handle.read()

    return [d.strip() for d in data.split('\n') if d]
