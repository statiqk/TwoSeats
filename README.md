# Deux Places · Two Seats

Appli de tri de films et séries à deux — un seul fichier statique (`index.html`) + un service worker minimal (`sw.js`).

## Hébergement : GitHub Pages
Réglages → Pages → Source : *Deploy from a branch* → `main` / `(root)`.

## Pages utiles
- `/` : l'application
- `/?admin` : panneau d'administration (code admin demandé)
- `/?share=…` : pages de recommandation publiques

## Données
JSONBin (index + un bin par espace), synchro temps réel Ably (facultatif), métadonnées TMDB / iTunes / TVMaze.
