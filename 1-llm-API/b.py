import os
import json
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-small-latest"
client = Mistral(api_key=api_key)

def writeFile(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def launchPythonFile(path):
    import subprocess
    result = subprocess.run(['python3', path], capture_output=True, text=True)
    return result.stdout

def ask_llm_for_function_call():
    prompt = (
        "Tu as accès à deux fonctions :\n"
        "- writeFile(path, content) : écrit le contenu dans le fichier spécifié.\n"
        "- launchPythonFile(path) : exécute le fichier python spécifié.\n"
        "\n"
        "Je veux que tu répondes uniquement avec un JSON de la forme :\n"
        '{"function": "NOM_DE_LA_FONCTION", "args": {"arg1": "valeur1", ...}}' + "\n"
        "\n"
        "Écris un fichier python qui affiche 'hello world' à l'exécution."
    )
    chat_response = client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    return chat_response.choices[0].message.content

def main():

    llm_response = ask_llm_for_function_call()
    print("Réponse :", llm_response)

    try:
        call = json.loads(llm_response)
        func_name = call["function"]
        args = call["args"]
    except Exception as e:
        print("Erreur lors du parsing du JSON :", e)
        return

    if func_name == "writeFile":
        writeFile(**args)
        print(f"Fichier {args['path']} créé.")
        output = launchPythonFile(args['path'])
        print("Sortie :", output)
    elif func_name == "launchPythonFile":
        output = launchPythonFile(**args)
        print("Sortie :", output)
    else:
        print("Fonction non reconnue.")

if __name__ == "__main__":
    main()
