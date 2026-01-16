# Calculatrice Scientifique

Une calculatrice graphique moderne avec interface style Apple, développée en Python avec CustomTkinter.

## Fonctionnalités

### Mode Standard
- Opérations de base : addition, soustraction, multiplication, division
- Pourcentage
- Nombres décimaux

### Mode Scientifique
- Fonctions trigonométriques : sin, cos, tan (en degrés)
- Racine carrée
- Puissances (x², xʸ)
- Constantes : π, e
- Parenthèses

### Interface
- Thème sombre style Apple
- Panneau d'historique des calculs (affichage/masquage)
- Basculement entre mode standard et scientifique

## Prérequis

- Python 3.10+
- CustomTkinter

## Installation

```bash
pip install customtkinter
```

## Utilisation

```bash
python main.py
```

## Structure du projet

```
├── main.py              # Point d'entrée de l'application
├── Calculator/
│   ├── __init__.py
│   └── calculator.py    # Logique de calcul (sans bibliothèque math)
└── GUI/
    ├── __init__.py
    └── builder_app.py   # Interface graphique CustomTkinter
```

## Auteurs

Tris-Rov-Ste-My
