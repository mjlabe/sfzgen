def get_template(template_path: str="./template.sfz") -> list:
    return open(template_path).readlines()


def generate_regions(file_mapping: dict, n_samples: int, crossfade_percentage: int=25, midi_start=60) -> list:
    sfz = []
    midi_note = midi_start
    for group, mapping in file_mapping.items():
        sfz.append(
            f"<group>key={midi_note}"
        )

        sample_number = 0
        sample_span = 127 // n_samples
        for _, sample_path in mapping.items():
            lovel = sample_number * sample_span
            lovel = lovel - int((crossfade_percentage / 100) * sample_span)
            hivel = (sample_number + 1) * sample_span
            hivel = hivel + int((crossfade_percentage / 100) * sample_span)
            if sample_number == 0:
                lovel = 0
            if sample_number >= n_samples - 1:
                hivel = 127
            sfz.append(
                f"<region>sample={sample_path} lovel={lovel} hilevel={hivel}"
            )
            sample_number += 1
        midi_note += 1
    return sfz


def generate_sfz(file_mapping, n_samples):
    sfz_template = get_template()
    generated_sfz = generate_regions(file_mapping=file_mapping, n_samples=n_samples)
    sfz = sfz_template + generated_sfz
    with open("./soundfont/sfzgen.sfz", "w") as f:
        f.write("\n".join(sfz))