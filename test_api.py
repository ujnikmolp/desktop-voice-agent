from openai import OpenAI

client = OpenAI(
    api_key="sk-03ae6efe161f45c69487e0a60b10b9b0",  # 替换成你自己的
    base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "你好，请回复'连接成功'"}
    ]
)

print(response.choices[0].message.content)