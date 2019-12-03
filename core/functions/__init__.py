def destructure(obj, *params):
    import operator
    return operator.itemgetter(*params)(obj)

def greet(**kwargs):
    year, day, puzzle = destructure(kwargs, 'year', 'day', 'puzzle')
    print('Advent of Code')
    print(f'-> {year}-{day}-{puzzle}')
    print('--------------')

def load_data(filename):
    with filename.open('r') as handle:
        return handle.read()

def start(fn):
    import pathlib
    base_path = pathlib.Path(__file__).parent.parent / 'data'
    def wrapped(*args, **kwargs):
        greet(**kwargs)
        data = load_data(base_path / f'{kwargs["year"]}.{kwargs["day"]}.txt')
        return fn(data, *args, **kwargs)
    return wrapped

def flatten_json(nested_json):
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            for i, a in enumerate(x):
                flatten(a, name + str(i) + '_')
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out
