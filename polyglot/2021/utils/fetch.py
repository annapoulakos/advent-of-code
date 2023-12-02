import argparse, os
import requests
from bs4 import BeautifulSoup


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int)
    parser.add_argument('day', type=int)

    return parser.parse_args()

def main():
    args = get_args()

    header = {
        'Cookie': f'session={os.environ.get("AOC_SESSION_COOKIE")}',
    }
    url = f'https://adventofcode.com/{args.year}/day/{args.day}'

    response = requests.get(url, headers=header)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, features="html.parser")
    code = next((x for x in soup.find_all('code')), None)
    if code is not None: code = code.contents[0]

    print(code)


if __name__ == '__main__':
    main()
