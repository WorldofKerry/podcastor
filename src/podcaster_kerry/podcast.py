from openai import OpenAI

PROMPT_TEXT = """
Convert this into a two-party podcast conversation, without losing nuances.
Be specific on equations used, new findings and methodologies, etc.
The result should formatted as:
H1: <things to say>
H2: <things to say>
where a newline delimits the contents.
"""

def to_podcast(api_key: str, content: str) -> str:
    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    )

    completion = client.chat.completions.create(
    model="deepseek/deepseek-chat:free",
    messages=[
        {
        "role": "user",
        "content": content + "\n" + PROMPT_TEXT
        }
    ],
    temperature=0.0,
    )
    return completion.choices[0].message.content, completion