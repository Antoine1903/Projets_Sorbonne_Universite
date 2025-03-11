# Document de mi-projet : Organiz’asso

## Graphe des dépendances réciproques des composants

Ce graphe montre les relations entre les composants React du projet, mettant en évidence les dépendances mutuelles et la hiérarchie des composants.

### Schéma des dépendances

```
App (index.jsx)
├── MainPage.jsx
│   ├── NavigationPanel.jsx
│   │   ├── Login.jsx
│   │   └── Logout.jsx
│   ├── Feed.jsx
│   │   ├── SearchBar.jsx
│   │   ├── MessageList.jsx
│   │   │   ├── Message.jsx
│   │   │   │   └── ReplyList.jsx
│   │   │   │       └── Reply.jsx
│   │   └── AddMessage.jsx
│   ├── User.jsx
│   │   ├── MessageList.jsx
│   │   │   └── Message.jsx
│   │   │       └── ReplyList.jsx
│   │   │           └── Reply.jsx
│   ├── Result.jsx
│   │   ├── MessageList.jsx
│   │   │   └── Message.jsx
│   │   │       └── ReplyList.jsx
│   │   │           └── Reply.jsx
│   ├── AsideAdmin.jsx
│   │   ├── AsideMenu.jsx
│   │   └── AsideValidation.jsx
│   │       └── AsideValidationUser.jsx
│   ├── FeedAdmin.jsx
│   │   ├── MessageList.jsx
│   │   │   ├── Message.jsx
│   │   │   │   └── ReplyList.jsx
│   │   │   │       └── Reply.jsx
│   │   └── AddMessage.jsx
├── messages_request.jsx
└── server_request.jsx
```

## Présentation détaillée des composants

### Composants de Pages

#### `Feed.jsx`
- **Fonction** : Affiche tous les messages du forum ouvert
- **Props** : `user (Object)`, `messages (Array)`
- **State** : `searchTerm`, `filteredMessages`
- **Composants enfants** : `SearchBar.jsx`, `MessageList.jsx`, `AddMessage.jsx`

#### `User.jsx`
- **Fonction** : Affiche les informations utilisateur et les messages publiés
- **Props** : `user (Object)`
- **State** : `userMessages (Array)`
- **Composants enfants** : `MessageList.jsx`

#### `Result.jsx`
- **Fonction** : Affiche les résultats de recherche basés sur des mots-clés, des dates ou des auteurs
- **Props** : `searchResults (Array)`
- **State** : `filteredMessages`
- **Composants enfants** : `MessageList.jsx`

### Composants Fonctionnels

#### `MessageList.jsx`
- **Fonction** : Affiche une liste de messages
- **Props** : `messages (Array)`, `onDelete (Function)`
- **State** : Aucun
- **Composants enfants** : `Message.jsx`

#### `Message.jsx`
- **Fonction** : Affiche un message individuel
- **Props** : `author (String)`, `content (String)`, `timestamp (Date)`
- **State** : `isEditing (Boolean)`
- **Composants enfants** : `ReplyList.jsx`

#### `messages_request.jsx`
- **Fonction** : Gère les requêtes API pour récupérer, ajouter ou supprimer des messages
- **Dépendances** : `axios`, `server_request.jsx`

### Composants Administrateur

#### `AsideAdmin.jsx`
- **Fonction** : Affiche le menu latéral pour les administrateurs
- **Props** : `adminActions (Object)`
- **State** : `selectedAction (String)`
- **Composants enfants** : `AsideMenu.jsx`, `AsideValidation.jsx`

#### `AsideValidation.jsx`
- **Fonction** : Gère la validation des nouvelles inscriptions
- **Props** : `pendingUsers (Array)`, `onValidate (Function)`
- **State** : `selectedUser (Object)`
- **Composants enfants** : `AsideValidationUser.jsx`

----------------------------------------------------

### index.jsx
- **Fonction** : Point d'entrée de l'application, rend le composant `MainPage`.
- **Props** : Aucune.
- **États** : Aucun.
- **Composants enfants** : `MainPage`.

### MainPage.jsx
- **Fonction** : Gère la navigation principale et l'affichage dynamique des différentes pages (`Feed`, `User`, `Result`, `FeedAdmin`).
- **Props** : Aucune.
- **États** : Utilise `useState` et `useEffect` pour charger les données utilisateur et gérer la navigation.
- **Composants enfants** : `NavigationPanel`, `Signin`, `Feed`, `Result`, `User`, `SearchBar`, `AsideAdmin`, `FeedAdmin`.

### NavigationPanel.jsx
- **Fonction** : Barre de navigation permettant la connexion/déconnexion.
- **Props** : Aucune.
- **États** : Aucun.
- **Composants enfants** : `Login`, `Logout`.

### Login.jsx
- **Fonction** : Gère la connexion utilisateur.
- **Props** : Aucune.
- **États** : Utilise `useState` pour stocker les informations de connexion.
- **Composants enfants** : Aucun.

### Logout.jsx
- **Fonction** : Gère la déconnexion utilisateur.
- **Props** : Aucune.
- **États** : Aucun.
- **Composants enfants** : Aucun.

### Feed.jsx
- **Fonction** : Affiche les messages du forum ouvert.
- **Props** : Aucune.
- **États** : Utilise `useState` et `useEffect` pour récupérer les messages via `messages_request.jsx`.
- **Composants enfants** : `SearchBar`, `MessageList`, `AddMessage`.

### MessageList.jsx
- **Fonction** : Liste tous les messages sous forme de composants `Message`.
- **Props** : `messages` (tableau de messages).
- **États** : Aucun.
- **Composants enfants** : `Message`.

### Message.jsx
- **Fonction** : Affiche un message spécifique avec ses réponses.
- **Props** : `message` (objet message).
- **États** : Utilise `useState` et `useEffect` pour charger les réponses.
- **Composants enfants** : `ReplyList`.

### ReplyList.jsx
- **Fonction** : Affiche la liste des réponses associées à un message.
- **Props** : `replies` (tableau de réponses).
- **États** : Aucun.
- **Composants enfants** : `Reply`.

### Reply.jsx
- **Fonction** : Affiche une réponse unique.
- **Props** : `reply` (objet réponse).
- **États** : Aucun.
- **Composants enfants** : Aucun.

### User.jsx
- **Fonction** : Affiche le profil utilisateur avec ses messages publiés.
- **Props** : Aucune.
- **États** : Utilise `useState` et `useEffect` pour récupérer les messages utilisateur.
- **Composants enfants** : `MessageList`.

### Result.jsx
- **Fonction** : Affiche les résultats de recherche sous forme de messages filtrés.
- **Props** : `results` (tableau de messages filtrés).
- **États** : Utilise `useState` pour stocker les résultats de recherche.
- **Composants enfants** : `MessageList`.

### AsideAdmin.jsx
- **Fonction** : Menu latéral réservé aux administrateurs pour la gestion du site.
- **Props** : Aucune.
- **États** : Utilise `useState` et `useEffect` pour la validation des utilisateurs.
- **Composants enfants** : `AsideMenu`, `AsideValidation`.

### AsideValidationUser.jsx
- **Fonction** : Gère la validation des utilisateurs en attente.
- **Props** : `user` (objet utilisateur).
- **États** : Utilise `useState` pour le statut de validation.
- **Composants enfants** : Aucun.

### FeedAdmin.jsx
- **Fonction** : Affiche le forum réservé aux administrateurs avec la possibilité d'ajouter des messages.
- **Props** : Aucune.
- **États** : Utilise `useState` et `useEffect` pour récupérer et afficher les messages.
- **Composants enfants** : `MessageList`, `AddMessage`.

### messages_request.jsx
- **Fonction** : Contient les fonctions de requêtes API pour manipuler les messages (GET, POST, DELETE).
- **Props** : Non applicable.
- **États** : Non applicable.
- **Composants enfants** : Aucun.

### server_request.jsx
- **Fonction** : Définit la configuration par défaut pour les requêtes serveur avec Axios.
- **Props** : Non applicable.
- **États** : Non applicable.
- **Composants enfants** : Aucun.

### SearchBar.jsx
**Fonction :**
SearchBar permet aux utilisateurs de rechercher des messages en fonction de mots-clés, d'une période de temps ou d'un auteur spécifique.

**Props :**
- `onSearch`: (fonction) Callback pour exécuter la recherche.
- `placeholder`: (string, optionnel) Texte affiché dans la barre de recherche.

**États :**
- `query`: (string) Stocke le texte de la recherche en cours.

**Composants inclus :**
- Aucun.

### AddMessage.jsx
**Fonction :**
Permet aux utilisateurs de publier de nouveaux messages sur le forum.

**Props :**
- `onMessageAdded`: (fonction) Callback pour rafraîchir la liste des messages après l’ajout.

**États :**
- `messageContent`: (string) Contenu du message saisi par l'utilisateur.
- `error`: (string) Stocke les erreurs éventuelles.

**Composants inclus :**
- Aucun.

### AsideMenu.jsx
**Fonction :**
Affiche un menu latéral permettant aux utilisateurs de naviguer dans différentes sections du site.

**Props :**
- `userRole`: (string) Définit si l'utilisateur est un administrateur ou un membre standard.

**États :**
- `activeSection`: (string) Définit la section actuellement sélectionnée.

**Composants inclus :**
- Aucun.

### AsideValidation.jsx
**Fonction :**
Affiche une liste des nouvelles inscriptions en attente de validation par un administrateur.

**Props :**
- `pendingUsers`: (array) Liste des utilisateurs en attente d’approbation.
- `onValidate`: (fonction) Callback pour valider un utilisateur.
- `onReject`: (fonction) Callback pour rejeter une inscription.

**États :**
- `loading`: (booléen) Indique si les données sont en cours de récupération.
- `error`: (string) Stocke un message d’erreur potentiel.

**Composants inclus :**
- `AsideValidationUser.jsx`

-------------------------------------------------------

## Architecture Globale du Projet

- Utilisation de React Router pour la gestion de la navigation entre les pages
- Intégration de `server_request.jsx` pour toutes les requêtes API
- Gestion des états globaux avec `useState` et `useContext` pour une meilleure performance et organisation

## Analyse des Interactions et Fonctionnalités

- **Connexion et inscription** : Gérés par `Login.jsx`, `Signin.jsx`
- **Gestion des messages et des réponses** : `AddMessage.jsx`, `Reply.jsx`
- **Contrôle des droits administratifs** : `AsideAdmin.jsx` avec accès limité aux fonctionnalités d’administration
- **Fonction de recherche avancée** : Utilisation de `SearchBar.jsx` pour affiner les résultats de recherche

