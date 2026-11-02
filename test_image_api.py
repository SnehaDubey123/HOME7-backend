from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    result = client.images.generate(
        model="gpt-image-2",
        prompt="A simple top-down 2D floor plan of a small 1BHK apartment, clearly labeled rooms, clean architectural drawing",
        size="1024x1024",
    )

    print("SUCCESS: Image generation worked.")
    print("Image data received:", bool(result.data[0].b64_json))

except Exception as e:
    print("FAILED:")
    print(type(e).__name__)
    print(e)