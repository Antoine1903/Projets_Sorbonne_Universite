# Document de mi-projet : Organiz’asso

## 1. Graphe des dépendances réciproques des composants

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

## 2. Présentation détaillée des composants

### 2.1 Composants de Pages

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

### 2.2 Composants Fonctionnels

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

### 2.3 Composants Administrateur

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

## 3. Architecture Globale du Projet

- Utilisation de React Router pour la gestion de la navigation entre les pages
- Intégration de `server_request.jsx` pour toutes les requêtes API
- Gestion des états globaux avec `useState` et `useContext` pour une meilleure performance et organisation

## 4. Analyse des Interactions et Fonctionnalités

- **Connexion et inscription** : Gérés par `Login.jsx`, `Signin.jsx`
- **Gestion des messages et des réponses** : `AddMessage.jsx`, `Reply.jsx`
- **Contrôle des droits administratifs** : `AsideAdmin.jsx` avec accès limité aux fonctionnalités d’administration
- **Fonction de recherche avancée** : Utilisation de `SearchBar.jsx` pour affiner les résultats de recherche

