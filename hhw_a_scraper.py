import requests
from pathlib import Path

HONEY_HUNTER_URL    = 'https://genshin.honeyhunterworld.com/img/'
CHARACTER_ASSET_URL = HONEY_HUNTER_URL + 'char/'
WEAPON_ASSET_URL    = HONEY_HUNTER_URL + 'art/a_'

CHARACTER_SUFFIXES = ['.png', '_face.png', '_side.png', '_gacha_card.png', '_gacha_splash.png']
WEAPON_SUFFIXES = ['.png', '_a.png', '_gacha.png']

def fetch_character(character, out_dir=Path('.')):
    char_url = CHARACTER_ASSET_URL + character

    for suffix in CHARACTER_SUFFIXES:
        resp = requests.get(char_url + suffix)
        if resp.status_code == 200:
            with open(out_dir / (character + suffix), 'wb') as outfile:
                for chunk in resp:
                    outfile.write(chunk)


def fetch_weapon(weapon_id, out_dir=Path('.')):
    weapon_url = WEAPON_ASSET_URL + weapon_id

    for suffix in WEAPON_SUFFIXES:
        resp = requests.get(weapon_url + suffix)
        if resp.status_code == 200:
            with open(out_dir / ('a_' + weapon_id + suffix), 'wb') as outfile:
                for chunk in resp:
                    outfile.write(chunk)

def fetch_asset(id, outdir):
    if not id:
        return

    if id.isnumeric():
        fetch_weapon(id, outdir)
    else:
        fetch_character(id, outdir)

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('id', type=str, nargs='?', help='id or name to fetch')
    parser.add_argument('-i', '--input', dest='infile', help='Input file containing list of items to fetch')
    parser.add_argument('-o', '--output', dest='outdir', help="Output for downloaded files")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    infile = args.infile
    outdir = Path('.')
    if args.outdir:
        outdir = Path(args.outdir)
    if infile:
        with open(infile, 'r') as ff:
            for line in ff:
                fetch_asset(line.rstrip(), outdir)
    else:
        id = args.id
        fetch_asset(id, outdir)