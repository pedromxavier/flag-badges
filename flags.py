import io
import base64
import requests
import tempfile
import numpy as np
from PIL import Image
from pathlib import Path

def download_img(url: str, path: str):
    res = requests.get(url)

    if res.status_code == 200:
        data = res.content
    else:
        return False

    with open(path, 'wb') as fp:
        fp.write(data)

    return True

def download_flag(code: str, path: str, *, style: str = "flat", size: str = 64):
    assert size in (16, 24, 32, 48, 64)
    assert style in ("flat", "shiny")

    url = f"https://flagsapi.com/{code}/{style}/{size}.png"

    return download_img(url, path)

def get_flag_img(code: str, *, style: str = "flat", size: str = 64):
    path = Path(tempfile.mkdtemp()).joinpath(f"{code}.png")

    download_flag(code, path, style=style, size=size)

    return Image.open(path)

def get_alpha_bbox(img: Image.Image):
    alphac = np.array(img)[:,:,3] # get alpha channel

    # get where alpha is not zero
    coords = np.argwhere(alphac)

    # lower bounds
    yl, xl = np.min(coords, axis=0)
    
    # upper bounds
    yu, xu = np.max(coords, axis=0) + 1

    return (xl, yl, xu, yu)

def crop_img(img: Image.Image):
    bbox = get_alpha_bbox(img)

    return img.crop(bbox)

def to_base64(img: Image.Image):
    ptr = io.BytesIO()

    img.save(ptr, format = "PNG")
    
    # reset file pointer to start
    ptr.seek(0)

    # read, encode bytes and decode to string
    return base64.b64encode(ptr.read()).decode()

BADGE_TEMPLATE = """
<svg xmlns="http://www.w3.org/2000/svg" width="{total_width:.2f}" height="{total_height:.2f}" role="img" aria-label="made in BR">
    <title>made in {code}</title>
    <linearGradient id="s" x2="0" y2="100%">
        <stop offset="0" stop-color="#bbb" stop-opacity=".1" />
        <stop offset="1" stop-opacity=".1" />
    </linearGradient>
    <clipPath id="r">
        <rect width="{total_width:.2f}" height="{total_height:.2f}" rx="3" fill="#fff" />
    </clipPath>
    <g clip-path="url(#r)">
        <image
            href="data:image/png;base64,{image_data}"
            x="{text_width:.2f}" y="0"
            width="{img_width:.2f}" height="{img_height:.2f}"
        />
        <rect width="{text_width:.2f}" height="{total_height:.2f}" fill="#555" />
        <rect width="{total_width:.2f}" height="{total_height:.2f}" fill="url(#s)" />
    </g>
    <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="110">
        <text aria-hidden="true" x="285" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="450">made in</text>
        <text x="285" y="140" transform="scale(.1)" fill="#fff" textLength="450">made in</text>
    </g>
</svg>
"""

def make_badge(code: str, path: str = None, *, text_width = 56, total_height = 20):
    img = crop_img(get_flag_img(code))
    b64 = to_base64(img)

    img_width, img_height = img.size

    factor = img_height / total_height

    img_width, img_height = (img_width / factor,  total_height)

    img = img.resize((int(round(img_width)), int(round(img_height))))

    total_width = text_width + img_width

    svg = BADGE_TEMPLATE.format(
        code         = code,
        image_data   = b64,
        total_width  = total_width,
        total_height = total_height,
        text_width   = text_width,
        img_width    = img_width,
        img_height   = img_height,
    )

    if path is None:
        path = f"{code}.svg"

    with open(path, "w") as fp:
        fp.write(svg)

    return path
  
