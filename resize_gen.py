from PIL import Image
import os, sys
from tqdm import tqdm

path = "egnc/"
dirs = os.listdir( path )

def expand2square(pil_img, background_color):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result


def resize():
    for item in tqdm(dirs):
        if os.path.isfile(path+item):
            im = Image.open(path+item).convert("RGBA")
            f, e = os.path.splitext(path+item)
            im = expand2square(im, (0, 0, 0, 0))
            imResize = im.resize((512,512), Image.ANTIALIAS)
            imResize.save(f + '.png', 'PNG', quality=100)

resize()