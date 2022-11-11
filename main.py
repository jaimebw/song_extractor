# -*- coding: utf-8 -*
# author: Jaime Bowen Varela
from pathlib import Path
from pydub import AudioSegment
import re
from tqdm import tqdm
import argparse
import youtube_dl


def download_song(url:str, output_path: Path)-> Path:
    """
    download a song from youtube

    Parameters
    ----------
    url : str
        url of the song
    output_path : Path
        path to the output file

    Returns
    -------
    None
    """
    audio_path = Path(f'{str(output_path)}/song.mp3')
    print(str(audio_path))
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(audio_path),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return audio_path 

def number_first_index(string: str) -> int:
    """
    Returns the index of the first number in a string

    Parameters
    ----------
    string : str

    Returns
    -------
    int
        index of the first number in the string

    """

    return re.search(r"\d", string).start()


def parse_songs(path: Path) -> list:
    """
    Parse the text file containing the songs and timestamps

    Parameters
    ----------
    path : Path
        Path to the text file

    Returns
    -------
    list
        List of dictionaries containing the songs names and timestamps

    """
    with open(path, "r") as f:
        songs = f.readlines()
    song_info = []
    for song in songs:
        index_number = number_first_index(song)
        song_name = song[:index_number]
        song_name = song_name[:-1]
        song_name = song_name.replace("\n", "")
        song_timestamp = song[index_number:]
        song_timestamp = song_timestamp.replace("\n", "")

        song_dict = {"name": song_name, "timestamp": song_timestamp}
        song_info.append(song_dict)
    return song_info


def time_to_seconds(string: str) -> int:
    """
    Converts a string in the format "mm:ss" to seconds

    Parameters
    ----------
    string : str
        String in the format "mm:ss"

    Returns
    -------
    int
        Number of seconds

    """
    time = string.split(":")
    seconds = int(time[0]) * 60 + int(time[1])
    return seconds


def main(
    audio_path: Path,
    song_path: Path,
    cover_path: Path = None,
    album_name: str = None,
    artist_name: str = None,
) -> None:
    """ 
    Main function
    """
    processed_song_path = Path("processed_songs")

    if not processed_song_path.exists():
        processed_song_path.mkdir()

    if not album_name and not artist_name:
        meta_dict = dict()
    else:
        meta_dict = {"album": album_name, "artist": artist_name}

    sound = AudioSegment.from_file(audio_path)
    songs_info = parse_songs(song_path)
    last_index = len(songs_info) - 1
    
    for index, song_info in enumerate(tqdm(songs_info)):
        tstamp0 = time_to_seconds(song_info["timestamp"]) * 1000
        if index != last_index:
            tstamp1 = time_to_seconds(songs_info[index + 1]["timestamp"]) * 1000
            song_clip = sound[tstamp0:tstamp1]
        else:
            song_clip = sound[tstamp0:]
        meta_dict["track"] = f"{index+1}/{len(songs_info)}"
        song_clip.export(
            processed_song_path / f"{song_info['name']}.mp3",
            format="mp3",
            tags=meta_dict,
            cover=str(Path) if cover_path else None,
        )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()    
    parser.add_argument("-a", "--audio_path", help="Path to the audio file")
    parser.add_argument("-u","--url", help="url of the song", type=str,default=None)
    parser.add_argument(
        "-s",
        "--song_path",
        help="Path to the text file containing the songs and timestamps",
    )
    parser.add_argument(
        "-c", "--cover_path", help="Path to the cover image", default=None
    )
    parser.add_argument("-n", "--album_name", help="Album name", default=None)
    parser.add_argument("-r", "--artist_name", help="Artist name", default=None)
    args = parser.parse_args()
    
    if args.url:
        args.audio_path = download_song(args.url, Path())
        print(args.audio_path)
    
    if (not args.url) and (not args.audio_path):
        raise ValueError("You must provide a path to the audio file and or a youtube url")
    
    if not args.song_path:
        raise ValueError("You must provide a path to the song list")
    
    main(
        args.audio_path,
        args.song_path,
        args.cover_path,
        args.album_name,
        args.artist_name,
    )