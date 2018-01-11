import os
import re

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.util import etree
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
        raise Exception("{} should be renamed safely (e.g.; {})".format(path, sanitized_path))
    path = sanitized_path

    if os.path.isabs(path):
        raise Exception("Path {} should be relative".format(path))

    base_paths = [MARKDOWN_DIR]
    if file_hint is not None:
        base_paths.insert(0, os.path.join(os.path.dirname(file_hint)))

    for base_path in base_paths:
        full_path = os.path.join(base_path, ASSETS_PATH, path)
        if os.path.isfile(full_path) and os.access(full_path, os.R_OK):
            return mk_rel_path(full_path)

    return None

class MarklogAnnotationProcessor(Preprocessor):
    ANNOTATION_RE = re.compile(r'@([A-Za-z0-9_-]+)\((.*?)\)')

    def __init__(self, *args, **kwargs):
        self.ext_instance = kwargs.pop('ext_instance')

        super(MarklogAnnotationProcessor, self).__init__(*args, **kwargs)

    def run(self, lines):
        for n, line in enumerate(lines):
            match = self.ANNOTATION_RE.search(line)
            if match is None:
                continue

            annotation, text = match.groups()

            if annotation == 'marklog-asset':
                link = marklog_asset(text, file_hint = self.ext_instance.getConfig('marklog_file_hint', None))
                if link is None:
                    continue

                l, r = match.span()
                lines[n] = line[:l] + link + line[r:]

        return lines

class MarklogExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {'marklog_file_hint': ['', 'Provide a hint for Marklog as to what Markdown file is being converted.']}

        super(MarklogExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('marklog_asset',
            MarklogAnnotationProcessor(md, ext_instance = self),
            '<html_block')
