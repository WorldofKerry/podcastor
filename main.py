from openai import OpenAI
import argparse

def run(api_key):
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    )

    completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    model="openchat/openchat-7b:free",
    messages=[
        {
        "role": "user",
        "content": "What is the meaning of life?"
        }
    ]
    )

    print(completion.choices[0].message.content)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--key')

    args = parser.parse_args()

    run(args.key)

if __name__ == "__main__":
    main()