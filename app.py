from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Définition d'une métrique personnalisée : Compteur de requêtes
REQUEST_COUNT = Counter(
    'flask_app_requests_total', 
    'Nombre total de requêtes reçues par l'application Flask',
    ['method', 'endpoint', 'http_status']
)

@app.route('/')
def hello():
    # On incrémente le compteur à chaque visite
    REQUEST_COUNT.labels(method='GET', endpoint='/', http_status=200).inc()
    return "Hello INSAT! L'application est sous surveillance."

@app.route('/metrics')
def metrics():
    # Endpoint spécial que Prometheus va "scraper"
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)