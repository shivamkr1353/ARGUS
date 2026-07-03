import base64
import io
from PIL import Image, ImageDraw
from openai import OpenAI

# Create an actual image (red circle) so it doesn't trigger blank image refusals
img = Image.new('RGB', (256, 256), color='white')
draw = ImageDraw.Draw(img)
draw.ellipse((50, 50, 200, 200), fill='red')

buffer = io.BytesIO()
img.save(buffer, format="JPEG")
b64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

client = OpenAI(
    api_key="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",
    base_url="https://integrate.api.nvidia.com/v1"
)

try:
    response = client.chat.completions.create(
        model="meta/llama-3.2-90b-vision-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What shape and color is in this image?"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64_image}"}}
                ]
            }
        ],
        max_tokens=300,
        temperature=0.1
    )
    print("REAL VISION TEST:", response.choices[0].message.content)
except Exception as e:
    print("REAL VISION ERROR:", e)
