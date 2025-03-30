import os
import openai
import asyncio

max_blocks = 50

source_language = os.getenv('SOURCE_LANGUAGE')
target_language = os.getenv('TARGET_LANGUAGE')
api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI(api_key=api_key)

def get_lines():
    with open("input.srt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    return lines

def get_prompt(source_language, target_language, text):
    with open("prompt.txt", "r", encoding="utf-8") as file:
        prompt = file.read()
    prompt = prompt.replace("{sourceLanguage}", source_language)
    prompt = prompt.replace("{targetLanguage}", target_language)
    prompt = prompt.replace("{text}", text)
    return prompt

async def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

async def translate(number, total, block):
    print(f"""Start #{number} of {total}...""")

    result = await get_completion(block)

    # Remove triple backticks from the result.
    result = result.replace("```\n", "")
    result = result.replace("```", "")

    # Make sure the result has the empty line at the end.
    result = result.rstrip().lstrip()
    result += "\n\n"

    print(f"""Finish #{number} of {total}...""")

    return result

async def main():
    blocks = []
    current_number_of_blocks = 0
    text = ""

    lines = get_lines()

    for line in lines:
        text += line
        if len(line.rstrip()) == 0 and len(text) > 0:
            current_number_of_blocks += 1
            if current_number_of_blocks >= max_blocks:
                blocks += [get_prompt(source_language, target_language, text)]
                current_number_of_blocks = 0
                text = ""
    if len(text) > 0:
        blocks += [get_prompt(source_language, target_language, text)]

    tasks = [translate(index + 1, len(blocks), block) for index, block in enumerate(blocks)]
    result = await asyncio.gather(*tasks)

    with open("output.srt", "w", encoding="utf-8") as file:
        for line in result:
            file.write(line)

asyncio.run(main())
