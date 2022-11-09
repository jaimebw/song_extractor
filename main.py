#!/usr/bin/env python
# -*- coding: utf-8 -*
# author: Jaime Bowen Varela
from pathlib import Path
from pydub import AudioSegment
import re
from tqdm import tqdm


def number_first_index(string):
    return re.search(r"\d", string).start()

# delete last char of string

def parse_songs(path):
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
        song_dict = {
            "name": song_name,
            "timestamp": song_timestamp
        }
        song_info.append(song_dict)
    return song_info

def time_to_seconds(string):
    time = string.split(":")
    seconds = int(time[0]) * 60 + int(time[1])
    return seconds

if __name__ == "__main__":
    path_to_audio = Path("Joji - Chloe Burbank Vol. 1 (23 Track Album)-qOm-trHYlh8.m4a")
    path_to_cover = Path("cover.png")
    meta_dict = {
        "album" : "Chloe Burbank Vol. 1",
        "artist":"Joji"}

    song_path = Path("processed_songs")

    if not song_path.exists():
        song_path.mkdir()
    
    path_to_song = Path("song_list.txt")
    sound = AudioSegment.from_file(path_to_audio)
    songs_info = parse_songs(path_to_song)
    last_index = len(songs_info) - 1
    for index, song_info in enumerate(tqdm(songs_info)):
        tstamp0 = time_to_seconds(song_info["timestamp"])*1000
        if index != last_index:
            tstamp1 = time_to_seconds(songs_info[index+1]["timestamp"])*1000
            song_clip = sound[tstamp0:tstamp1]
        else:
            song_clip = sound[tstamp0:]
        song_clip.export(song_path / f"{song_info['name']}.mp3", format="mp3",
        tags = meta_dict,cover = str(path_to_cover)) 
        
    


