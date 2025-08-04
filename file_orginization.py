import os
import re
import shutil
from pathlib import Path


notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def natural_sort_key(s) -> list:
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', str(s))]


def organize(folder_path: str, starting_note: str, n_velocities: int) -> dict[list]:
    """
    :param folder_path: path to samples folder
    :param starting_note: first file note (i.e. C)
    :param n_velocities: number of samples per note
    :return:
    """

    i = 0
    n = 0
    octave = 0
    starting_note_index = notes.index(starting_note)
    mapping = {}
    files = sorted(os.listdir(folder_path), key=natural_sort_key)
    for file in files:
        n = i + starting_note_index
        note = notes[(n // n_velocities) % len(notes)]
        index = n % n_velocities
        if f"{note}{octave}" not in mapping:
            mapping[f"{note}{octave}"] = {}
        mapping[f"{note}{octave}"][file] = f"{note}{octave}_{index}"
        ext = file.split(".")[-1]
        shutil.copy(Path(folder_path, file), f"./mappings/{note}{octave}_{index}.{ext}")
        i += 1
        if note == "B" and index == n_velocities - 1:
            octave += 1
    return mapping
