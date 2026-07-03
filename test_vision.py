import base64
from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://integrate.api.nvidia.com/v1"
)

# create a dummy 1x1 png image
dummy_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
b64_image = base64.b64encode(dummy_image).decode('utf-8')

try:
    response = client.chat.completions.create(
        model="meta/llama-3.2-90b-vision-instruct",
        messages=[
            {
                "role": "user",
                "content": f"What color is this image? <img src=\"data:image/png;base64,{b64_image}\" />"
            }
        ],
        max_tokens=300
    )
    print("VISION TEST:", response.choices[0].message.content)
except Exception as e:
    print("VISION ERROR:", e)
