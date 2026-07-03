import base64
import requests

invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"

# Create a small valid JPEG
dummy_image = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00\xff\xdb\x00C\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xc0\x00\x0b\x08\x00\x01\x00\x01\x01\x01\x11\x00\xff\xc4\x00\x1f\x00\x00\x01\x05\x01\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\xff\xda\x00\x08\x01\x01\x00\x00?\x00\x00\xff\xd9'
b64_image = base64.b64encode(dummy_image).decode('utf-8')

headers = {
    "Authorization": "Bearer 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",
    "Accept": "application/json"
}

payload = {
    "model": "meta/llama-3.2-90b-vision-instruct",
    "messages": [
        {
            "role": "user",
            "content": f"Describe this image <img src=\"data:image/jpeg;base64,{b64_image}\" />"
        }
    ],
    "max_tokens": 512,
    "temperature": 0.4,
    "stream": False
}

try:
    response = requests.post(invoke_url, headers=headers, json=payload)
    print(response.status_code)
    print(response.text)
except Exception as e:
    print("ERROR:", e)
