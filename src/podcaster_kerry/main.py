import argparse
from pathlib import Path
import tempfile
import traceback
from podcaster_kerry import run, pdf_to_text, get_audio, upload

def everything(input: Path, output: Path, key: str, working_dir: Path = None):
    try:
        text = pdf_to_text(input)
        print(f"{text=}")
        result = run(key, text)
        print(f"{result=}")
        get_audio(result, working_dir, output)
        upload(output)
    except Exception:
        print(traceback.format_exc())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key', help="OPENROUTER_API_KEY", required=True)
    parser.add_argument('-i', '--input', help="path to input pdf file", required=True)
    parser.add_argument('-o', '--output', help="path to output mp3 file", required=True)
    parser.add_argument('-c', '--working_dir', help="working dir", default="./outputs/")
    args = parser.parse_args()

    everything(Path(args.input), Path(args.output), args.key, Path(args.working_dir))

if __name__ == "__main__":
    main()