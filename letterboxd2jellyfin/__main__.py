#! /bin/python
from letterboxdpy.list import List
import os
from pathlib import Path
import shutil
import argparse
import re
import importlib

STUB_FILE = importlib.resources.path("letterboxd2jellyfin", "bluray.mp4")
DVD_STUB = importlib.resources.path("letterboxd2jellyfin", "dvd.mp4")


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="letterboxd2jellyfin",
        usage="Turn a Letterboxd list into a Jellyfin library structure, using a stub video file.",
    )
    parser.add_argument(
        "-o",
        "--output-path",
        help='Output Jellyfin library path. Should include "Movies" at the end (eg /path/to/library/Movies)',
        required=True,
        type=str,
    )
    parser.add_argument("-u", "--username", help="Letterboxd username", type=str)
    parser.add_argument(
        "-p",
        "--playlist-slug",
        help='The playlist slug (eg "scream-ranked" from https://letterboxd.com/matchup/list/scream-ranked/)',
        type=str,
    )
    parser.add_argument(
        "-url",
        "--playlist-url",
        help='Attempt to parse a letterboxd playlist URL, overrides --username and --playlist-slug (eg "https://letterboxd.com/matchup/list/scream-ranked/")',
        type=str,
    )
    parser.add_argument(
        "-v",
        "--video_file",
        help="Override the stub video file to put in the library",
        type=str,
    )
    parser.add_argument(
        "-dvd",
        help="Use the build-in DVD placeholder video file instead of the blu-ray one",
        action="store_true",
    )

    return parser.parse_args()


def main():
    args = parse_arguments()

    if args.playlist_url is not None:
        print("parsing URL")
        result = re.search(r"letterboxd\.com\/(.*)\/list\/(.*)", args.playlist_url)
        groups = result.groups()
        if len(groups) != 2:
            print(f"failed to parse the username and url from `{args.playlist_url}`!")
            exit(1)
        args.username = groups[0]
        args.playlist_slug = groups[1].removesuffix("/")

    print(f"Loading playlist `{args.playlist_slug}` from username `{args.username}`...")
    list_instance = List(args.username, args.playlist_slug)
    print("done!")
    movies = list_instance.movies
    print(f"This playlist has {len(movies)} entries")

    if args.video_file is None:
        stub = STUB_FILE
        if args.dvd:
            stub = DVD_STUB

        with stub as stub_path:
            args.video_file = str(stub_path)

    for _, movie in movies.items():
        # {'slug': 'reservoir-dogs', 'name': 'Reservoir Dogs', 'year': 1992, 'url': 'https://letterboxd.com/film/reservoir-dogs/'}
        movie_name = f"{movie['name']} ({movie['year']})"
        movie_folder = os.path.join(args.output_path, movie_name)

        movie_file = os.path.join(movie_folder, movie_name + ".mp4")
        os.makedirs(movie_folder, exist_ok=True)

        if not Path(movie_file).is_file():
            print("creating stub file ", movie_file)
            shutil.copy(args.video_file, movie_file)

    print("all done!")


if __name__ == "__main__":
    main()
