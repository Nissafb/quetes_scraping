from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import pandas as pd
url = "http://www.chucknorrisfacts.fr/facts/top/1"
navigator = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
html = requests.get(url, headers={'User-Agent': navigator})

soup = BeautifulSoup(html.text, 'html.parser')
bloc = soup.find_all('div', {"class" : "card"})
blague = soup.find_all('p', {"class" : "card-text"})

# Crée un dictionnaire vide pour stocker les blagues et les blocs correspondants
blagues_et_blocs_et_notes = {}

# Boucle pour enregistrer les blagues et les blocs dans le dictionnaire
for i in range(len(bloc)):
    blague_text = blague[i].get_text()
    bloc_text = bloc[i].get_text()
    blagues_et_blocs_et_notes[blague_text] = bloc_text
# Recherche de la note dans le bloc
    note = bloc[i].find('div', class_='row').get_text(strip=True) if bloc[i].find('div', class_='row') else None

    blagues_et_blocs_et_notes[blague_text] = {'bloc': bloc_text, 'note': note}

# Convertir le dictionnaire en DataFrame
df = pd.DataFrame(list(blagues_et_blocs_et_notes.items()), columns=['blague', 'details'])

# Séparer la colonne 'details' en deux colonnes 'bloc' et 'note'
df[['bloc', 'note']] = pd.DataFrame(df['details'].tolist(), index=df.index)

# Supprimer la colonne 'details' qui n'est plus nécessaire
df = df.drop(columns=['details'])

# Afficher le DataFrame
print(df)
