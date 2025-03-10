import os
import logging
from tika import parser

# Silence tika logs https://github.com/chrismattmann/tika-python/issues/341
tika_logger = logging.getLogger("tika.tika")
tika_logger.setLevel(logging.WARNING)

def extract_text(path: os.PathLike) -> str:
    while True:
        try:
            parsed = parser.from_file(str(path))
        except RuntimeError as e:
            print(f"Error with extract_text {e}, retrying ...")
    return parsed["content"]