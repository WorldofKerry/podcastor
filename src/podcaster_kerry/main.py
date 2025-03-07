import argparse
from pathlib import Path
import traceback
from podcaster_kerry import run, pdf_to_text, get_audio, upload

def run(input: Path, output: Path, key: str, working_dir: Path = None):
    if working_dir.exists():
        print(f"Woring dir {working_dir} already exists")
        return
    
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
    run(Path(args.input), Path(args.output), args.key, Path(args.working_dir))

if __name__ == "__main__":
    main()