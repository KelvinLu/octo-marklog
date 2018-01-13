import os
from werkzeug.utils import secure_filename

from marklog import app


BASE_DIR = app.config['BASE_DIR']
MARKDOWN_DIR = app.config['MARKDOWN_DIR']
ASSETS_PATH = app.config['ASSETS_PATH']



def mk_rel_path(path):
    assert os.path.isabs(path)
    assert os.path.dirname(os.path.commonprefix([p + os.path.sep for p in [BASE_DIR, path]])).startswith(BASE_DIR)

    path = os.path.normpath(path).replace(os.path.normpath(BASE_DIR), '', 1)

    return path

def marklog_asset(path, file_hint = None):
    sanitized_path = secure_filename(path)

    if not sanitized_path == path:
        raise Exception("{} should be renamed safely (e.g.; {}).".format(path, sanitized_path))
    path = sanitized_path

    if os.path.isabs(path):
        raise Exception("Path {} should be relative.".format(path))

    base_paths = [MARKDOWN_DIR]
    if file_hint is not None:
        base_paths.insert(0, os.path.join(os.path.dirname(file_hint)))

    for base_path in base_paths:
        full_path = os.path.join(base_path, ASSETS_PATH, path)

        if os.path.isfile(full_path) and os.access(full_path, os.R_OK):
            return mk_rel_path(full_path), full_path

    raise Exception("Could not find a readable file for asset {}.".format(path if file_hint is None else path + " in " + file_hint))
