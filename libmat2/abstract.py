import abc
import os
import re
import shutil
import tempfile
from typing import Set, Dict, Union

assert Set  # make pyflakes happy


class AbstractParser(abc.ABC):
    """ This is the base class of every parser.
    It might yield `ValueError` on instantiation on invalid files,
    and `RuntimeError` when something went wrong in `remove_all`.
    """
    meta_list = set()  # type: Set[str]
    mimetypes = set()  # type: Set[str]

    def __init__(self, filename: str) -> None:
        """
        :raises ValueError: Raised upon an invalid file
        """
        if re.search('^[a-z0-9./]', filename) is None:
            # Some parsers are calling external binaries,
            # this prevents shell command injections
            filename = os.path.join('.', filename)

        self.filename = filename
        fname, extension = os.path.splitext(filename)
        self.output_filename = fname + '.cleaned' + extension
        self.lightweight_cleaning = False
        self.in_place = False

    def __del__(self) -> None:
        if self.in_place:
            try:
                shutil.move(self.output_filename, self.filename)
            except Exception as e:
                # If the move failed (for any reason), make sure the temporary
                # file is removed and inform the user.
                print("[-] %s was NOT cleaned: %s" % (self.filename, e))
                try:
                    os.remove(self.output_filename)
                except OSError as e:
                    print("[-] could not remove temporary file %s: %s",
                          (self.output_filename, e))

    def set_edit_in_place(self) -> None:
        # Make sure the temporary file has the same file extension name as the
        # original one, as external utilities may be based on that.
        _, ext = os.path.splitext(self.filename)
        fd, self.output_filename = tempfile.mkstemp(suffix=ext)
        self.in_place = True
        os.close(fd)

    @abc.abstractmethod
    def get_meta(self) -> Dict[str, Union[str, dict]]:
        pass  # pragma: no cover

    @abc.abstractmethod
    def remove_all(self) -> bool:
        """
        :raises RuntimeError: Raised if the cleaning process went wrong.
        """
        # pylint: disable=unnecessary-pass
        pass  # pragma: no cover
