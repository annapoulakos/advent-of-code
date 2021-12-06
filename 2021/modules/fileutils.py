from modules import config

def load_raw(day, test=False):
    fn = 'day-' + ('ex-' if test else '') + f'{day}.txt'
    target = config.DATA_PATH / fn
    with open(target, 'r') as handle:
        return handle.read().strip()

def load_lines(day, test=False):
    raw = load_raw(day, test)

    return [line.strip() for line in raw.split('\n') if line]
