"""Helper function for IO operations."""
import os
from typing import Iterable
from typing import List
from typing import Union


def lazy_read_headers(
    file_paths: Iterable[Union[str, os.PathLike]], *, lines_to_read: int = 10
) -> List[List[str]]:
    """Lazy read headerlines of files.

    Parameters
    ----------
    file_paths : Iterable[Union[str, os.PathLike]]
        Paths to the files which should be read.
    lines_to_read : int
        Number of lines to be read, by default 10

    Returns
    -------
    List[List[str]]
        Headerlines of the read files.
    """
    header_lines_list = []
    for file_path in file_paths:
        with open(file_path) as file:
            header_lines_list.append(
                [
                    file.readline().rstrip(
                        "\n",
                    )
                    for _ in range(lines_to_read)
                ]
            )
    return header_lines_list
