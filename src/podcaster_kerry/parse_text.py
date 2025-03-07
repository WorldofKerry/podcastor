
import os


def pdf_to_text(path: os.PathLike) -> str:
    import tika
    from tika import parser
    parsed = parser.from_file(str(path))
    return parsed["content"]