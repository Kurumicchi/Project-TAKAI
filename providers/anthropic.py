from providers.anthropic import Anthropic


MODEL = "claude-3-5-sonnet-20241022"

client = Anthropic()


def get_reply(user_input):
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    return response.content[0].text.strip()