import sys
from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://integrate.api.nvidia.com/v1"
)

try:
    response = client.chat.completions.create(
        model="moonshotai/kimi-k2.6",
        messages=[{"role": "user", "content": "Explain quantum physics in one sentence."}],
        max_tokens=1024,
        stream=True,
        extra_body={"chat_template_kwargs": {"thinking": True}}
    )
    for chunk in response:
        if chunk.choices and len(chunk.choices) > 0:
            # handle thinking content vs actual content
            # OpenAI python SDK maps unknown fields sometimes, or just puts it in content
            content = getattr(chunk.choices[0].delta, "content", None)
            if content:
                sys.stdout.write(content)
                sys.stdout.flush()
except Exception as e:
    print("TEXT ERROR:", e)
