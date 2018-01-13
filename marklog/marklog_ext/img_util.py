import os
import re

from PIL import Image



import assets



DEFAULT_THUMBNAIL_SIZE =    (512, 512)
DEFAULT_IMAGE_QUALITY =     95



def get_image(path):
    if not os.path.isabs(path):
        raise Exception("Path {} should be absolute.".format(path))

    dirpath = os.path.dirname(path)
    if not os.access(dirpath, os.W_OK):
        raise Exception("Directory containing {} is not writable.".format(path))

    filename, fileext = os.path.splitext(os.path.basename(path))

    return Image.open(path), filename, fileext, dirpath

def stale_ctime(orig_image, diff_image):
    return os.path.getctime(orig_image) > os.path.getctime(diff_image)

def thumbnail_args(img, argline = None):
    if argline is None:
        return DEFAULT_THUMBNAIL_SIZE, DEFAULT_IMAGE_QUALITY

    suffix = ""

    parsed_args = {}
    for arg in ['w', 'h', 'q']:
        match = re.search(arg + r'\s*=\s*(\d+)', argline)
        if not match:
            continue

        v = int(match.group(1))
        parsed_args[arg] = v
        suffix += '-' + arg + str(v)

    size = DEFAULT_THUMBNAIL_SIZE

    if parsed_args.get('w', None) or parsed_args.get('h', None):
        full_size = img.size
        size = (parsed_args.get('w', full_size[0]), parsed_args.get('h', full_size[1]))

    quality = parsed_args['q'] or DEFAULT_IMAGE_QUALITY

    return size, quality, suffix

def image_thumbnail(image_path, argline = None):
    img, filename, fileext, dirpath = get_image(image_path)
    size, quality, thumbnail_suffix = thumbnail_args(img, argline)

    thumbnail_filename = filename + ".thumbnail{}".format(thumbnail_suffix or '') + fileext
    thumbnail_path = os.path.join(dirpath, thumbnail_filename)

    if not os.path.isfile(thumbnail_path) or stale_ctime(image_path, thumbnail_path):
        img.thumbnail(size, Image.ANTIALIAS)
        img.save(thumbnail_path, img.format, optimize = True, quality = quality)

    return assets.mk_rel_path(thumbnail_path)
