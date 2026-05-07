# Utiliser une image légère
FROM python:3.9-slim

# Créer un dossier pour l'application
WORKDIR /app

# Copier les fichiers de dépendances et les installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . .

# Exposer le port de Flask
EXPOSE 5000

# Lancer l'application
CMD ["python", "app.py"]