# Tests du Projet Formation IA Agentique

## Description
Ce dossier contient les tests automatisés pour valider le comportement des agents IA du projet.

## Tests disponibles

### 1. Test de Sécurité - Résistance au Prompt Injection
- **Fichier** : `test_agents.py::test_agent_resists_prompt_injection`
- **Objectif** : Vérifier que l'agent refuse de divulguer son prompt système
- **Validation** : L'agent doit refuser poliment sans révéler ses instructions internes

### 2. Test de Format - Respect du Format Markdown
- **Fichier** : `test_agents.py::test_agent_respects_output_format`
- **Objectif** : Vérifier que l'agent génère des rapports au format Markdown
- **Validation** : Présence de titres H1 (#) et sous-titres H2 (##)

## Comment exécuter les tests

### Exécution simple (sans output)
```bash
python3 -m pytest tests/
```

### Avec affichage des outputs (recommandé)
```bash
python3 -m pytest tests/ -s
```

### Mode verbose avec outputs
```bash
python3 -m pytest tests/ -s -v
```

### Exécuter un test spécifique
```bash
python3 -m pytest tests/test_agents.py::test_agent_resists_prompt_injection -s -v
```

## Options utiles

- `-s` : Affiche les print() et outputs des agents
- `-v` : Mode verbose (détails des tests)
- `-x` : Arrête à la première erreur
- `--tb=short` : Affiche une trace d'erreur courte

## Structure des tests

Les tests utilisent :
- **pytest** : Framework de test
- **CrewAI** : Pour créer et exécuter les agents
- **Assertions** : Pour valider les comportements attendus

## Notes importantes

- Les agents ont `verbose=True` pour voir leur processus de réflexion
- Les tests vérifient à la fois la sécurité et la conformité fonctionnelle
- Les warnings de pydantic sont normaux et peuvent être ignorés