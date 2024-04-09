# Projet MyAniSongList

Ce dépôt contient le projet MyAniSongList comprenant à la fois le backend et le frontend, conçu pour offrir une application web complète et interactive. Le projet vise à démontrer la mise en œuvre d'une architecture moderne à deux niveaux, en utilisant des technologies populaires pour le développement web.

## Description

Ce projet met en place une application web qui permet aux utilisateurs de créer une compte, à l'aide de ce dernier noter leurs openings et endings de leurs animés préférés. L'utilisateur peut aussi ajouter des openings/endings à leur favoris.

L'architecture est divisée en deux parties principales :

- **Backend :** Le backend est construit à l'aide de Python avec la librairie FastAPI. Il expose des points d'API sécurisés pour gérer les opérations CRUD (Créer, Lire, Mettre à jour, Supprimer). Il communique avec une base de données MySQL et Redis pour stocker et récupérer les données.

- **Frontend :** Le frontend est construit en utilisant Angular 15. Il fournit une interface utilisateur réactive où les utilisateurs peuvent interagir. Les mises à jour en temps réel sont gérées grâce à des appels d'API au backend.

- **Base de données :**

<img src="./images/MLD_AniSong.png">


## Installation

### Prérequis

Avant de commencer, assurez-vous d'avoir installé Docker et créer un projet sur Firebase puis récupérer une clé privée.

### Instructions

1. **Backend :** Naviguez vers le dossier `backend`:<br/>
   1.1. Créez un fichier .env et remplissez le :
   ```
      DATABASE_URL=mysql+pymysql://ROOT_NAME:ROOT_PASSWORD@db/DATABASE_NAME
      SECRET_KEY=
      ALGORITHM=
      REDIS_HOST = redis
      REDIS_PORT = 6379
      MYSQL_ROOT_PASSWORD =
      USERNAME_ADMIN = Lors du lancement un compte administrateur est crée avec ce nom d'utilisateur
      PASSWORD_ADMIN = Lors du lancement un compte administrateur est crée avec ce mot de passe  
      ORIGINS = http://localhost:4200
      DOMAIN = localhost
      PROJECT_ID=
      PRIVATE_KEY_ID=
      PRIVATE_KEY=
      CLIENT_EMAIL=
      CLIENT_ID=
      CLIENT_CERT_URL=
      BUCKET_NAME= Nom du projet
   ```

2. A la racine du projet et exécutez les commandes suivantes :

   ```
   docker compose build
   docker compose start
   ```

3. Ouvrez votre navigateur et accédez à `http://localhost:4200` pour utiliser l'application.

## Technologies utilisées

- Backend : Python, FastAPI, SqlAlchemy
- Frontend : Angular 15, Tailwindcss
- Base de données : MySQL, Redis

## Fonctionnalités

FONCTIONNALITES GENERALES :
   
   - Création de compte
   - Connexion
   - Affichage des animes/détails
   - Affichage des musiques/détails
   - Affichage des avis
   - Affichage du classement des meilleurs musiques
   - Affichage des artistes/détails

COMPTE NORMAL :

   - Modification de profil
   - Notation d'un musique

ADMININISTRATEUR :

   - Gestion des langues
   - Gestion des animes
   - Gestion des types de musiques
   - Gestion des artistes
   - Gestion des musiques


## Remarques

- Ce projet a été créé dans le but d'apprendre de nouvelles compétences en développement fullstack.
