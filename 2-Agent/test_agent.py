import pytest

def test_writeFile():
    # Test si le fichier est créé
    assert writeFile('test.txt', 'Contenu de test') is None
    # Test si le contenu est correct
    with open('test.txt', 'r') as f:
        assert f.read() == 'Contenu de test'

# Ajoute d'autres tests si nécessaire