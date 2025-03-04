from openai import OpenAI
import argparse
import tika
from podcaster_kerry.text_to_podcast import run

def parse_text(path):
    import tika
    from tika import parser
    parsed = parser.from_file(path)
    return parsed["content"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key')
    parser.add_argument('-f', '--file')

    args = parser.parse_args()

    text = parse_text(args.file)

    result = run(args.key, text)

    print(result)

if __name__ == "__main__":
    main()