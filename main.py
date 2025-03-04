from openai import OpenAI
import argparse
import tika

def run(api_key, content):
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    )

    completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    model="deepseek/deepseek-chat:free",
    messages=[
        {
        "role": "user",
        "content": content + "\n Give Me An In Depth Summary"
        }
    ]
    )

    print(completion.choices[0].message.content)

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

    run(args.key, text)

if __name__ == "__main__":
    main()