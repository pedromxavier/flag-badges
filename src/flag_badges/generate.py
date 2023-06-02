from pathlib import Path

from .api import create_badge
from .codes import CODES

def generate_readme(root_path: Path):
    root_path = root_path.resolve()
    file_path = root_path.joinpath("README.md")
    data_path = root_path.joinpath("badges")

    path_list = data_path.glob("*.svg")
    href_list = []

    for href_path in path_list:
        href_path = href_path.resolve().relative_to(root_path)
        code = href_path.stem
        name = CODES[code]
        href = f"[![{name}]({href_path})]({href_path})"
        href_list.append(href)

    href = "\n".join(href_list)

    text = f"""
# flag-badges

made in `<flag>` badges for your projects

## Flags
{href}

---

Powered by [flagsapi](https://flagsapi.com/)
"""

    with open(file_path, "w") as fp:
        fp.write(text)

    return None

def generate_badges(root_path: Path, code_list: list):
    data_path = root_path.joinpath("badges")
    data_path.mkdir(parents=True, exist_ok=True)

    for code in code_list:
        flag_path = data_path.joinpath(f"{code}.svg")

        if not flag_path.exists():
            try:
                create_badge(code, flag_path)
            except:
                print(f"Badge failed: '{code}'")

    return None

def generate_cmd(args):
    root_path = Path(args.path)
    code_list = list(CODES.keys())
    
    generate_badges(root_path, code_list)
    generate_readme(root_path)

    return None