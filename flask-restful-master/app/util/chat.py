import json
from app.models.mission import MissionModel
import requests

api_key = "sk-proj-h0nF6h87OEsBnZuUkgbjT3BlbkFJWUUxdoaYjc6cqzJQyxh8"

def requete_openai(texte):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": texte}],
        "temperature": 0.7
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print("Erreur lors de la requête :", response.status_code)
        return None

def getMission(texte):
    format = "{'titre':'', 'description':'', 'datedebut':'', 'datefin':'', 'niveaudurgence':'', 'lieu',''}"
    requete = f"""
    Vous êtes un assistant d'une agence secrète qui emploie les agents 00.
    On vous donne la description de la mission et vous devez, à partir de cela, me donner le nom approprie a la mission.
    La description de la mission est la suivante : {texte}.
    Vous allez me donner la reponse sous forme de donnee json comme tel:
    {format}
    Completer moi ces informations selon l'sos ou la demande venant du client
    Met en double cote pas un seul cote comme je l'ai fait parce que je vais le transformer en json en python
    Met la date au format date comme par exemple 2024-05-10 a vous de determiner la date de debut et fin selon son niveau d'urgence.
    le niveau d'urgence varie entre 1 et 10
    """
    response = requete_openai(requete)
    response_json = json.loads(response)
    return MissionModel(response_json['titre'], response_json['description'], response_json['datedebut'],
                            response_json['datefin'], response_json['niveaudurgence'], response_json['lieu'])
    
def getAgents(textes,agents):
    liste_agent = ""
    i = 0
    for agent in agents:
        specialites = ""
        for sp in agent.specialites:
            specialites+= f"{sp.libelle},"
        liste_agent += f"[id:{i}, nom:{agent.nom}, grade:{agent.rang}, specialite:{specialites}]\n"
        i = i + 1
    print(liste_agent)
    format = "{\"id_agents_dispo\":[1,2]}"
    requete = f"""
        Vous êtes un assistant IA qui organisera un mission et tu vas choisir les agents 00 qui est capable de la mission. ca peut 1,2 ou 3 ou plusieurs, a toi de choisir.
        On vous donne la description de la mission et vous devez, à partir de cela, me donner les agents qui doivent la réaliser selon leur spécialité et grade.
        La description de la mission est la suivante : {textes}
        Voici les Agents disponibles :
        {liste_agent}
        Vous n'allez me renvoyer que les id des agents que vous trouver etre capable pour cette mission selon leur capacite et grade.
        vous allez me le donner en cette format: {format}
    """
    response = requete_openai(requete)
    response_json = json.loads(response)
    ids = response_json['id_agents_dispo']
    return [agents[id] for id in ids]


def getGadgets(textes,gadgets):
    liste_gadgets = ""
    i = 0
    for gadget in gadgets:
        liste_gadgets += f"[id:{i}, libelle:{gadget.name}]\n"
        i = i + 1
    format = "{\"id_gadgets\":[1,2]}"
    requete = f"""
        Vous êtes un assistant d'une agence secrète qui emploie les agents 00.
        On vous donne la description de la mission et vous devez, à partir de cela, me donner les gadgets adequats a la mission.
        La description de la mission est la suivante  {textes}
        Voici les Gadgets disponibles :
        {liste_gadgets}
        Vous n'allez me renvoyer que les id des gadgets que vous trouver etre adequat a la mission.
        vous allez me le donner en cette format: {format}
    """
    response = requete_openai(requete)
    response_json = json.loads(response)
    ids = response_json['id_gadgets']
    return [gadgets[id] for id in ids]

def sosText(texte, agents, gadgets):
    mission = getMission(texte)
    agents = getAgents(texte,agents)
    gadgets = getGadgets(texte, gadgets)
    return mission, agents, gadgets