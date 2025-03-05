import argparse
from podcaster_kerry import run
from podcaster_kerry import pdf_to_text
from podcaster_kerry import to_audio

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key', help="OPENROUTER_API_KEY")
    parser.add_argument('-f', '--file', help="path to input pdf file")
    parser.add_argument('-o', '--output', help="path to output audio file")

    args = parser.parse_args()

    text = pdf_to_text(args.file)

    result = run(args.key, text)

    print(result)

    to_audio(args.output)

if __name__ == "__main__":
    main()