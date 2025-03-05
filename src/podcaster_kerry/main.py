import argparse
from podcaster_kerry import run, pdf_to_text, to_audio, upload

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key', help="OPENROUTER_API_KEY")
    parser.add_argument('-i', '--input', help="path to input pdf file")
    parser.add_argument('-o', '--output', help="path to output mp3 file")
    parser.add_argument('-c', '--cache_dir', help="path to output mp3 file")

    args = parser.parse_args()

    text = pdf_to_text(args.input)

    result = run(args.key, text)

    print(result)

    to_audio(result, args.output)

    upload(args.output)

if __name__ == "__main__":
    main()