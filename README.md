# letterboxd2jellyfin

Quick Python script to convert a letterboxd list (eg `https://letterboxd.com/matchup/list/scream-ranked/`)
into a [Jellyfin-compatible library structure](https://jellyfin.org/docs/general/server/media/movies/)
of stub files.

## Install

```sh
pipx install letterboxd2jellyfin
```

## Why

This is for the niche use case where you:

1. Have a physical media collection that you haven't ripped
2. You would like to browse that collection in Jellyfin
3. You have a public list in Letterboxd of all the movies you own

This script will read the list from Letterboxd and copy a stub `.mp4` file to
the appropriate location.

### For example:

```sh
$ letterboxd2jellyfin  -o 'deleteme' -url https://letterboxd.com/matchup/list/scream-ranked/
parsing URL
Loading playlist `scream-ranked` from username `matchup`...
done!
This playlist has 6 entries
creating stub file  deleteme/Scream (1996)/Scream (1996).mp4
creating stub file  deleteme/Scream 4 (2011)/Scream 4 (2011).mp4
creating stub file  deleteme/Scream 2 (1997)/Scream 2 (1997).mp4
creating stub file  deleteme/Scream VI (2023)/Scream VI (2023).mp4
creating stub file  deleteme/Scream (2022)/Scream (2022).mp4
creating stub file  deleteme/Scream 3 (2000)/Scream 3 (2000).mp4
all done!
```

A stub video file for Blu-rays and DVDs is included, or you can provide your own
with `-dvd`.

## Usage

```sh
$ letterboxd2jellyfin  --help
usage: Turn a Letterboxd list into a Jellyfin library structure, using a stub video file.

options:
  -h, --help            show this help message and exit
  -o, --output-path OUTPUT_PATH
                        Output Jellyfin library path. Should include "Movies" at the end (eg /path/to/library/Movies)
  -u, --username USERNAME
                        Letterboxd username
  -p, --playlist-slug PLAYLIST_SLUG
                        The playlist slug (eg "scream-ranked" from https://letterboxd.com/matchup/list/scream-ranked/)
  -url, --playlist-url PLAYLIST_URL
                        Attempt to parse a letterboxd playlist URL, overrides --username and --playlist-slug (eg "https://letterboxd.com/matchup/list/scream-ranked/")
  -v, --video_file VIDEO_FILE
                        Override the stub video file to put in the library
  -dvd                  Use the build-in DVD placeholder video file instead of the blu-ray one
```