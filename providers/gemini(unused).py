from google import genai


MODEL = "gemini-3.6-flash"

client = genai.Client()


def get_reply(user_input):
    response = client.models.generate_content(
        model=MODEL,
        contents=user_input
    )

    return response.text.strip()