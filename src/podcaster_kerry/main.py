import argparse
from podcaster_kerry import run
from podcaster_kerry import pdf_to_text
from podcaster_kerry import to_audio

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key')
    parser.add_argument('-f', '--file')

    args = parser.parse_args()

    text = pdf_to_text(args.file)

    result = run(args.key, text)

    print(result)

    to_audio()

if __name__ == "__main__":
    main()