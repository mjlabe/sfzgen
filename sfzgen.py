import click
from file_orginization import organize


# @click.command()
# @click.option("-f", '--folder-path', help='Folder containing files to organize')
# @click.option("-s", '--starting-note', default='C', help='Starting note (e.g. C, C#, D, etc.)')
# @click.option("-n", '--n-velocities', default=5, help='Number of velocity layers per note', type=int)
def main(folder_path: str, starting_note:str="C", n_velocities: int=5):
    file_mapping = organize(folder_path, starting_note, n_velocities)
    print("\nFinal mapping:")
    for group, mapping in file_mapping.items():
        print(group)
        for file, note_name in mapping.items():
            print(f"{file}: {note_name}")


if __name__ == "__main__":
    main("./Bounces", "C", 5)
