from .codes import CODES

def list_cmd(args):
    for (code, name) in CODES.items():
        print(f"{code}: {name}")

    return None
