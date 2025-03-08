import argparse
from pathlib import Path
from podcaster_kerry import to_podcast, extract_text, dialogue_to_mp3, upload

def write_to_file(text: str, path: Path):
    with open(path, "w") as f:
        f.write(text)

def run(input: Path, output: Path, key: str, working_dir: Path):
    if working_dir.exists():
        print(f"Working dir {working_dir} already exists")
        return
    working_dir.mkdir(parents=True, exist_ok=True)
    raw_text = extract_text(input)
    write_to_file(raw_text, working_dir / "raw.txt")
    podcast_text, response = to_podcast(key, raw_text)
    write_to_file(podcast_text, working_dir / "podcast.txt")
    write_to_file(str(response), working_dir / "response.txt")
    dialogue_to_mp3(podcast_text, working_dir, output)
    upload(output)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key', help="OPENROUTER_API_KEY", required=True)
    parser.add_argument('-i', '--input', help="path to input pdf file", required=True)
    parser.add_argument('-o', '--output', help="path to output mp3 file", required=True)
    parser.add_argument('-d', '--working_dir', help="working dir that holds all intermediary data", default="./output/")
    args = parser.parse_args()
    run(Path(args.input), Path(args.output), args.key, Path(args.working_dir))

if __name__ == "__main__":
    main()