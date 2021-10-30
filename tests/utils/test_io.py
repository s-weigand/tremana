import pytest
from py.path import local as TmpDir

from tremana.utils.io import lazy_read_headers


@pytest.mark.parametrize("nr_of_lines", (5, 10, 20))
def test_lazy_read_headers(tmpdir: TmpDir, nr_of_lines: int):
    expected = []
    files_to_read = []
    for file_name in ("a.txt", "b.txt"):
        lines = [file_name[0] * i for i in range(1, nr_of_lines + 5)]
        file = tmpdir.join(file_name)
        file.write("\n".join(lines))
        files_to_read.append(file)
        expected.append(lines[:nr_of_lines])

    headers_from_paths = lazy_read_headers(files_to_read, lines_to_read=nr_of_lines)

    headers_from_string = lazy_read_headers(map(str, files_to_read), lines_to_read=nr_of_lines)

    assert headers_from_paths == expected
    assert headers_from_string == expected
