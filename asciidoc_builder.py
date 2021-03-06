# -*- coding: utf-8 -*-
"""
    sphinx.builders.asciidoc
    ~~~~~~~~~~~~~~~~~~~~

    AsciiDoc Sphinx builder.

    :copyright: Copyright 2007-2016 by the Sphinx team, see AUTHORS.
    :copyright: Copyright 2017 by Lukas Ruzicka (based on the Sphinx TextBuilder by the Sphinx team (see above))
    :license: BSD, see LICENSE for details.
"""

import codecs
from os import path

from docutils.io import StringOutput

from sphinx.builders import Builder
from sphinx.util.osutil import ensuredir, os_path
from sphinx.writers.asciidoc import AsciiDocWriter


class AsciiDocBuilder(Builder):
    name = 'asciidoc'
    format = 'asciidoc'
    out_suffix = '.adoc'
    allow_parallel = True

    def init(self):
        pass

    def get_outdated_docs(self):
        for docname in self.env.found_docs:
            if docname not in self.env.all_docs:
                yield docname
                continue
            targetname = self.env.doc2path(docname, self.outdir,
                                           self.out_suffix)
            try:
                targetmtime = path.getmtime(targetname)
            except Exception:
                targetmtime = 0
            try:
                srcmtime = path.getmtime(self.env.doc2path(docname))
                if srcmtime > targetmtime:
                    yield docname
            except EnvironmentError:
                # source doesn't exist anymore
                pass

    def get_target_uri(self, docname, typ=None):
        return ''

    def prepare_writing(self, docnames):
        self.writer = AsciiDocWriter()

    def write_doc(self, docname, doctree):
        self.current_docname = docname
        destination = StringOutput(encoding='utf-8')
        self.writer.write(doctree, destination)
        outfilename = path.join(self.outdir, os_path(docname) + self.out_suffix)
        ensuredir(path.dirname(outfilename))
        try:
            with codecs.open(outfilename, 'w', 'utf-8') as f:
                f.write(self.writer.output)
        except (IOError, OSError) as err:
            self.warn("error writing file %s: %s" % (outfilename, err))

    def finish(self):
        pass


def setup(app):
    app.add_builder(AsciiDocBuilder)

    #app.add_config_value('text_sectionchars', '*=-~"+`', 'env')
    #app.add_config_value('text_newlines', 'unix', 'env')

    return {
        'version': 'builtin',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
