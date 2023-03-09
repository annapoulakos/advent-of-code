import pathlib

store = pathlib.Path().cwd() / 'game-data.json'
if not store.exists():
    with store.open(mode='w+') as handle:
        handle.write('{}')
