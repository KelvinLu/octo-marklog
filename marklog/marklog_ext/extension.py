import re

from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

import assets
import img_util



class MarklogAnnotationProcessor(Preprocessor):
    ANNOTATION_RE = re.compile(r'@([A-Za-z0-9_-]+)(\[(.*?)\])?\((.*?)\)')

    def __init__(self, *args, **kwargs):
        self.ext_instance = kwargs.pop('ext_instance')

        super(MarklogAnnotationProcessor, self).__init__(*args, **kwargs)

    def run(self, lines):
        for n, line in enumerate(lines):
            i = 0

            while True:
                match = self.ANNOTATION_RE.search(line, i)
                if match is None:
                    break

                annotation, _, argline, text = match.groups()
                l, r = match.span()
                i = l + 1

                asset_link, asset_path = assets.marklog_asset(text, file_hint = self.ext_instance.getConfig('marklog_file_hint', None))
                if asset_path is None:
                    continue

                replacement = None

                if annotation == 'marklog-asset':
                    replacement = asset_link
                elif annotation == 'marklog-img-thumbnail':
                    replacement = img_util.image_thumbnail(asset_path, argline)

                if replacement is not None:
                    lines[n] = line = line[:l] + replacement + line[r:]

        return lines

class MarklogExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {'marklog_file_hint': ['', 'Provide a hint for Marklog as to what Markdown file is being converted.']}

        super(MarklogExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('marklog_annotation',
            MarklogAnnotationProcessor(md, ext_instance = self),
            '<html_block')
