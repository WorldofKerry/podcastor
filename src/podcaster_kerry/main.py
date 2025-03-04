import argparse
from podcaster_kerry.text_to_podcast import run
from podcaster_kerry.parse_text import pdf_to_text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key')
    parser.add_argument('-f', '--file')

    args = parser.parse_args()

    text = pdf_to_text(args.file)

    result = run(args.key, text)

    print(result)

if __name__ == "__main__":
    main()