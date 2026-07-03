import base64
from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://integrate.api.nvidia.com/v1"
)

try:
    response = client.chat.completions.create(
        model="moonshotai/kimi-k2.6",
        messages=[{"role": "user", "content": "hello"}],
        max_tokens=100
    )
    print("TEXT TEST:", response.choices[0].message.content)
except Exception as e:
    print("TEXT ERROR:", e)
