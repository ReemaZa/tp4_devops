import unittest
from app import app

class BasicTests(unittest.TestCase):
    # Test de la route principale
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello INSAT!", response.data)

    # NOUVEAU : Test de la route metrics pour SonarQube
    def test_metrics(self):
        tester = app.test_client(self)
        response = tester.get('/metrics')
        self.assertEqual(response.status_code, 200)
        # On vérifie que les métriques Prometheus sont bien générées
        self.assertIn(b"flask_app_requests_total", response.data)

if __name__ == '__main__':
    unittest.main()