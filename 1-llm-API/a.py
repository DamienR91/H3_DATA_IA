import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = Mistral(api_key=api_key)

def generateText(prompt: str) -> str:
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ]
    )
    return chat_response.choices[0].message.content

def writeFile(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def launchPythonFile(path):
    import subprocess
    result = subprocess.run(['python3', path], capture_output=True, text=True)
    return result.stdout

if __name__ == "__main__":
    prompt = input("Entrez votre prompt : ")
    print(generateText(prompt))