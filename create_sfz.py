def get_template(template_path: str="./template.sfz") -> str:
    return open(template_path).read()


def get_group(mapping: dict) -> list:
