from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pathlib import Path, PurePosixPath

from six import text_type


class Importer(object):
    pass
# DONE find_relative(uri, base, options)
# DONE find(uri, options)
#mtime(uri, options)
#key(uri, options)
#public_uri(uri, sourcemap_directory)
# DONE to_s
#directories_to_watch
#watched_file?(filename)


class FilesystemImporter(Importer):
    # TODO these should point to syntax objects or something
    # TODO ok bear with me here: instead of rewriting sass code to scss, make
    # an intermediate form (since we don't have blockast yet) that will just
    # run locate_blocks a bunch /ahead of time/ to produce a nested tree of
    # not-yet-parsed things.  that is, normalize to an actual intermediate
    # representation.  this is a Good Idea yes
    extensions = dict(sass='sass', scss='scss')

    def __init__(self, root):
        self.root = Path(root)

    def __repr__(self):
        return "<{0}({1!r})>".format(
            type(self).__name__, text_type(self.root))

    def find(self, path, relative_to='.', **kwargs):
        # TODO allow backslashes on windows?  what about drive letters?
        path = PurePosixPath(path)
        relative_to = PurePosixPath(relative_to)

        if path.name in ('.', '..'):
            # These cannot possibly be names of files
            return

        path = self.lexical_resolve(path, relative_to)

        # Don't allow ascending to a parent directory.
        # TODO/DEVIATION: ruby sass allows this, but it seems bonkers to me.
        # compiler switch to turn it off?  does ruby intend to disallow it?
        if path.parts[0] == '..':
            raise TypeError

        exists = []
        for candpath, syntax in self.candidate_filenames(path):
            fullpath = self.root / candpath
            if fullpath.exists():
                exists.append((candpath, syntax))

        if len(exists) == 0:
            return
        elif len(exists) == 1:
            candpath, syntax = exists[0]
            return Module.from_filename(self.root / candpath, syntax=syntax, importer=self)

        raise SassImportError(
            "Found multiple candidate files while trying to import {0!r} "
            "(you should rename or delete all but one of these):\n  {1}"
            .format(
                text_type(path),
                "\n  ".join(
                    text_type(self.root / candpath)
                    for candpath, syntax in exists)))

    @staticmethod
    def lexical_resolve(path, relative_to):
        """Given a path (which may be relative) and a base path, return a
        single combined path, without consulting the filesystem.
        """
        if path.parts[0] == '/':
            # Absolute path, relative to the import root
            parts = path.parts[1:]
        else:
            # Relative path, relative to relative_to.  Evaluate relative parts
            # textually
            parts = []
            for part in relative_to.parts + path.parts:
                if part == '.':
                    continue
                elif part == '..' and parts:
                    parts.pop()
                else:
                    parts.append(part)

        return PurePosixPath(*parts)

    def candidate_filenames(self, path):
        """Given a path, produce a sequence of ``(path, syntax)`` pairs that
        the path might be referring to.  This is what multiplexes "foo" into
        "foo.scss", "_foo.scss", etc.
        """
        # Now deal with extensions
        if path.suffix in self.extensions:
            candidate_extensions = [path.suffix]
            base = path.stem
        else:
            candidate_extensions = sorted(self.extensions)
            base = path.name

        for ext in candidate_extensions:
            syntax = self.extensions[ext]
            yield path.parent / base + "." + ext, syntax
            yield path.parent / "_" + base + "." + ext, syntax
