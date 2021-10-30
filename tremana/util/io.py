"""Helper function for IO operations."""
from __future__ import annotations

import os
from typing import Iterable


def lazy_read_headers(
    file_paths: Iterable[str | os.PathLike[str]], *, lines_to_read: int = 10
) -> list[list[str]]:
    """Lazy read headerlines of files.

    Parameters
    ----------
    file_paths : Iterable[str | os.PathLike[str]]
        Paths to the files which should be read.
    lines_to_read : int
        Number of lines to be read, by default 10

    Returns
    -------
    list[list[str]]
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
