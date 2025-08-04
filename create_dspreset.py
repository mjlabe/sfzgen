midi_map = {
    60: {
        "organ": 60,
        "piano": 95
    }
}


def get_template(template_path: str="./template.dspreset") -> (list[list[str]], list[list[str]]):
    with open(template_path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f.readlines()]
        for i, line in enumerate(lines):
            if line.lstrip().startswith("<groups"):
                return lines[:i + 1], lines[i - 1:]
    return lines, []  # If text not found


def generate_regions(file_mapping: dict, n_samples: int, crossfade_percentage: int=25, midi_start=60, instrument="piano") -> list:
    dspreset = []
    note = midi_map[midi_start][instrument]
    for group, mapping in file_mapping.items():
        dspreset.append(
            f'    <group rootNote="{note}" loNote="{note}" hiNote="{note}">'
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
            dspreset.append(
                f'      <sample path="{sample_path}" loVel="{lovel}" hiVel="{hivel}"/>'
            )
            sample_number += 1
        dspreset.append(
            f'      <effects/>'
        )
        dspreset.append(
            f'    </group>'
        )
        note -= 1
    return dspreset


def generate_dspreset(file_mapping, n_samples):
    dspreset_template = get_template()
    generated_sfz = generate_regions(file_mapping=file_mapping, n_samples=n_samples)
    sfz = dspreset_template[0] + generated_sfz + dspreset_template[1]
    with open("./soundfont/sfzgen.dspreset", "w") as f:
        f.write("\n".join(sfz))