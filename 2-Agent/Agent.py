import os
import json
from mistralai import Mistral
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

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

def stop():
    """Fonction appelée par l'agent pour signaler qu'il a terminé."""
    print("L'agent a décidé d'arrêter.")
    return "stop"

def listFiles(path):
    """Liste les fichiers et dossiers dans le chemin donné."""
    try:
        files = os.listdir(path)
        return files
    except Exception as e:
        return f"Erreur lors du listing : {e}"

def runTests(path):
    """Lance les tests unitaires sur le fichier ou dossier donné (pytest ou unittest)."""
    import subprocess
    try:
        result = subprocess.run(['python3', '-m', 'pytest', path], capture_output=True, text=True)
        return result.stdout + '\n' + result.stderr
    except Exception as e:
        return f"Erreur lors de l'exécution des tests : {e}"

def scrapeUrl(url, selector=None):
    """Fait du scraping sur l'URL donnée. Si selector est fourni, retourne le texte correspondant."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        if selector:
            elements = soup.select(selector)
            return [el.get_text(strip=True) for el in elements]
        else:
            return soup.get_text()
    except Exception as e:
        return f"Erreur scraping : {e}"


def run_agent(prompt: str, max_step: int):
    """
    Exécute une série d'actions en appelant le LLM dans une boucle, jusqu'à ce que l'agent appelle stop ou que max_step soit atteint.
    """
    context = ""
    for step in range(max_step):
        # On enrichit le prompt avec le contexte de la tâche précédente
        full_prompt = (
            "Tu es un agent Python autonome. Tu as accès aux fonctions suivantes :\n"
            "- writeFile(path, content) : écrit le contenu dans le fichier spécifié.\n"
            "- launchPythonFile(path) : exécute le fichier python spécifié.\n"
            "- runTests(path) : lance les tests unitaires (pytest) sur le fichier ou dossier spécifié.\n"
            "- listFiles(path) : liste les fichiers et dossiers dans le chemin donné.\n"
            "- scrapeUrl(url, selector=None) : fait du scraping sur l'URL (optionnellement avec un sélecteur CSS).\n"
            "- stop() : arrête la boucle si tu as terminé la tâche.\n"
            "\n"
            "À chaque étape, tu reçois le contexte de la tâche précédente :\n"
            f"{context}\n"
            "\n"
            f"Ta tâche : {prompt}\n"
            "\n"
            "Réponds uniquement avec un JSON de la forme :"
            '{"function": "NOM_DE_LA_FONCTION", "args": {"arg1": "valeur1", ...}}'
        )
        chat_response = client.chat.complete(
            model=model,
            messages=[{"role": "user", "content": full_prompt}],
            response_format={"type": "json_object"}
        )
        llm_response = chat_response.choices[0].message.content
        print(f"\nÉtape {step+1} - Réponse :", llm_response)
        try:
            call = json.loads(llm_response)
            func_name = call["function"]
            args = call["args"]
        except Exception as e:
            print("Erreur lors du parsing du JSON :", e)
            break
        if func_name == "writeFile":
            writeFile(**args)
            print(f"Fichier {args['path']} créé.")
            context = f"Fichier {args['path']} créé."
        elif func_name == "launchPythonFile":
            output = launchPythonFile(**args)
            print("Sortie :", output)
            context = f"Sortie : {output}"
        elif func_name == "runTests":
            output = runTests(**args)
            print("Résultat des tests :", output)
            context = f"Résultat des tests : {output}"
        elif func_name == "listFiles":
            files = listFiles(**args)
            print("Fichiers :", files)
            context = f"Fichiers : {files}"
        elif func_name == "scrapeUrl":
            result = scrapeUrl(**args)
            print("Résultat scraping :", result)
            context = f"Résultat scraping : {result}"
        elif func_name == "stop":
            stop()
            break
        else:
            print("Fonction non reconnue.")
            context = "Fonction non reconnue."


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
    prompt = input("Entrez votre prompt : ")
    run_agent(prompt, max_step=8)
