from main import *


def test_main():
    path_to_audio = Path("tests/data/song.mp3")
    path_to_song = Path("tests/data/song_list.txt")
    main(path_to_audio, path_to_song)
