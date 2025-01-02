
# 🌦️ Weather Dashboard Project

## 📚 Description
Weather Dashboard est une application interactive permettant de visualiser les données météorologiques historiques et actuelles de plusieurs villes. Les données sont stockées dans MongoDB et accessibles via une API REST construite avec Flask. Le tableau de bord interactif est développé avec Dash.

---

## 📦 Prérequis
- **Docker** (v20+)
- **Docker Compose** (v2.0+)
- **Python 3.9+**
- **MongoDB Compass** *(optionnel pour visualiser la base MongoDB)*

---

## 🛠️ Installation

1. **Clonez le dépôt :**
   ```bash
   git clone https://github.com/Chaima-Mehrzi/Mini_project_weather.git
   cd Mini_project_weather
   ```

2. **Créez le fichier `.env` dans le dossier `app` :**
   ```
   MONGO_URI=mongodb://mongodb:27017/weather_data
   WEATHER_API_URL=http://weather_api:5000/cities
   ```

3. **Installez les dépendances Python (optionnel pour exécution locale) :**
   ```bash
   pip install -r app/requirements.txt
   ```

---

## 🚀 Lancement du Projet

### Lancer avec Docker Compose :
```bash
docker-compose up --build
```

### Lancer les services séparément :
- **API Flask :**
   ```bash
   docker-compose up weather_api
   ```
- **Tableau de Bord Flask Dash :**
   ```bash
   docker-compose up flask_dash_app
   ```

### Accès aux Services :
- **API :** [http://localhost:5000](http://localhost:5000)
- **Dashboard :** [http://localhost:8050](http://localhost:8050)

---

## 📊 Utilisation du Tableau de Bord

1. **Accédez au tableau de bord :** [http://localhost:8050](http://localhost:8050)
2. **Sélectionnez une ville.**
3. **Choisissez une plage de dates.**
4. **Cliquez sur `Load Data` pour afficher les graphiques.**

### Visualisations Disponibles :
- **Température (°C)** *(avec moyenne mobile)*
- **Humidité (%)**
- **Précipitations (mm)**

---

## 🌐 API Endpoints

- **Récupérer les villes disponibles :**
   ```http
   GET /cities
   ```
- **Récupérer les données d'une ville spécifique :**
   ```http
   GET /cities/<city_name>
   ```

**Exemple de Réponse :**
```json
{
    "name": "Paris",
    "temperature": 5.7,
    "humidity": 78,
    "weather": "Rain",
    "description": "light rain",
    "timestamp": "2024-12-03T13:00:00"
}
```

---

## 🛡️ Dépannage

- **API ne fonctionne pas :**
   ```bash
   docker-compose logs weather_api
   ```
- **Dashboard ne fonctionne pas :**
   ```bash
   docker-compose logs flask_dash_app
   ```
- **Accès MongoDB :**
   ```bash
   docker-compose exec mongodb mongosh
   ```


---

## 🗂️ Structure du Projet

```
/app
├── api.py          # API Flask
├── dashboard.py    # Tableau de bord Dash
├── db.py           # Connexion MongoDB
├── fetch_weather_data.py  # Récupération des données météo
├── generate_mock_data.py  # Génération de données fictives
├── Dockerfile.api  # Dockerfile pour l'API
├── Dockerfile.dashboard  # Dockerfile pour le Dashboard
├── requirements.txt  # Dépendances Python
└── __init__.py
docker-compose.yml  # Configuration Docker Compose
README.md           # Documentation du projet
```

---

## 🎯 **Merci d'utiliser Weather Dashboard ! 🌤️**
N'hésitez pas à ouvrir une **issue** sur GitHub en cas de problème ou pour proposer des améliorations.
