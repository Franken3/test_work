import asyncio

import aiohttp


class ChatGPT:
    def __init__(self, gpt_api_key: str) -> dict:
        self.api_key = gpt_api_key

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def async_openai_request(self, messages: list) -> str:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}",
                   "Content-Type": "application/json"}
        data = {
            "model": "gpt-3.5-turbo",
            "messages": messages
        }

        async with self.session.post(url, json=data, headers=headers, ssl=False) as response:
            info = await response.json()
            return info


async def chat_response(api_key: str, user_input: str) -> str:
    async with ChatGPT(api_key) as gpt:
        mood_detect = [
            {"role": "system", "content": "Определите настроение этого сообщения (позитивное или негативное)."},
            {"role": "user", "content": user_input}
        ]
        get_mood = await gpt.async_openai_request(mood_detect)
        mood = "позитивное" if "позитивное" in get_mood["choices"][0]["message"]["content"].lower() else "негативное"
        print(f"Настроение вашего сообщения - {mood}, ожидайте ответ")
        await asyncio.sleep(30)
        if mood == "позитивное":
            style_prompt = f"Ответьте на него как Бэтмен. Обязательно сделай приписку кто отвечает и характерную фразу для персонажа"
        else:
            style_prompt = f"Ответьте на него как Джокер. Обязательно сделай приписку кто отвечает и характерную фразу для персонажа"
        final_messages = [
            {"role": "system", "content": style_prompt},
            {"role": "user", "content": user_input}
        ]
        final_response = await gpt.async_openai_request(final_messages)
        return final_response["choices"][0]["message"]["content"]


api_key = "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"

# test part
positive_questions = [
    "Покормить котенка на улице?",
    "Купить маме цветов?",
    "Помочь другу с переездом?",
    "Сделать тренировку",
    "Выпить воды вместо газировки?"
]

negative_questions = [
    "Забрать конфету у ребенка?",
    "Лопнуть все шарики в цирке?",
    "Поменять сахар и соль местами?",
    "Закрыть брата в темной комнате?",
    "Забрать еду у котенка?"
]

print("Тесты: ")
k = 0
for q in positive_questions:
    k += 1
    user_input = q
    print(f"№{k} - {q}")
    try:
        response = asyncio.run(chat_response(api_key, user_input))
        print(f"Ответ: {response}")
    except:
        print('Задержка очереди, подождите 20 секунд')
        asyncio.run(asyncio.sleep(20))
        response = asyncio.run(chat_response(api_key, user_input))
        print(f"Ответ: {response}\n\n")

for q in negative_questions:
    k += 1
    user_input = q
    print(f"№{k} - {q}")
    try:
        response = asyncio.run(chat_response(api_key, user_input))
        print(f"Ответ: {response}\n\n")
    except:
        print('Задержка очереди, подождите 20 секунд')
        asyncio.run(asyncio.sleep(20))
        response = asyncio.run(chat_response(api_key, user_input))
        print(f"Ответ: {response}\n\n")

while True:
    user_input = input("Введите ваш вопрос: ")
    try:
        response = asyncio.run(chat_response(api_key, user_input))
        print(f"Ответ: {response}")
    except:
        print('Задержка очереди, подождите 20 секунд')
        asyncio.run(asyncio.sleep(20))
        response = asyncio.run(chat_response(api_key, user_input))
        print(f"Ответ: {response}")
