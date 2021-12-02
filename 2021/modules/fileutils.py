from modules import config

def load_raw(day):
    target = config.DATA_PATH / f'day-{day}.txt'
    with open(target, 'r') as handle:
        return handle.read().strip()

def load_lines(day):
    raw = load_raw(day)

    return [line.strip() for line in raw.split('\n') if line]
