from openai import OpenAI

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
        "content": content + "\n Convert This Into A two party Podcast Conversation Without Losing Nuances, use the transcript format used in court hearings."
        }
    ],
    temperature=0.0,
    )

    return completion.choices[0].message.content