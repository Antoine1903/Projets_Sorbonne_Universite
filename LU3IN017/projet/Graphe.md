# Document de mi-projet : Organiz’asso

## 1. Graphe des dépendances réciproques des composants

Le graphe suivant montre les relations entre les composants React du projet, mettant en évidence les dépendances mutuelles et la hiérarchie des composants.

```
App (index.jsx)
├── UserContext.jsx
├── MainPage.jsx
│   ├── NavigationPanel.jsx
│   │   ├── Login.jsx
│   │   ├── Logout.jsx
│   │   └── Signup.jsx
│   ├── Feed.jsx
│   │   ├── SearchBar.jsx
│   │   ├── MessageList.jsx
│   │   │   ├── Message.jsx
│   │   │   │   ├── ReplyList.jsx
│   │   │   │   │   └── Reply.jsx
│   │   │   │   ├── EditMessage.jsx
│   │   │   │   └── DeleteMessage.jsx
│   │   └── AddMessage.jsx
│   ├── UserProfile.jsx
│   │   ├── UserInfo.jsx
│   │   ├── UserMessageList.jsx
│   │   │   ├── Message.jsx
│   │   │   │   ├── ReplyList.jsx
│   │   │   │   │   └── Reply.jsx
│   │   │   │   ├── EditMessage.jsx
│   │   │   │   └── DeleteMessage.jsx
│   ├── SearchResults.jsx
│   │   ├── MessageList.jsx
│   │   │   ├── Message.jsx
│   │   │   │   ├── ReplyList.jsx
│   │   │   │   │   └── Reply.jsx
│   │   │   │   ├── EditMessage.jsx
│   │   │   │   └── DeleteMessage.jsx
│   ├── AdminPanel.jsx
│   │   ├── AdminMenu.jsx
│   │   ├── UserValidation.jsx
│   │   │   └── ValidateUser.jsx
│   │   ├── AdminFeed.jsx
│   │   │   ├── MessageList.jsx
│   │   │   │   ├── Message.jsx
│   │   │   │   │   ├── ReplyList.jsx
│   │   │   │   │   │   └── Reply.jsx
│   │   │   │   │   ├── EditMessage.jsx
│   │   │   │   │   └── DeleteMessage.jsx
│   │   │   └── AddMessage.jsx
├── api/messagesAPI.jsx
├── api/userAPI.jsx
└── api/serverConfig.jsx
```

## 2. Présentation des composants et leur fonctionnement

### 2.1 Gestion du contexte global
Nous utilisons `useContext` pour gérer l'état global des utilisateurs.

#### `UserContext.jsx`
- **Fonction** : Gère l'état de l'utilisateur connecté.
- **Props** : Aucune.
- **State** : `user (Object)`, `setUser (Function)`.
- **Utilisation** : Importé dans `index.jsx` et fourni à toute l'application.

```jsx
import { createContext, useState } from "react";

export const UserContext = createContext();

export const UserProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    return (
        <UserContext.Provider value={{ user, setUser }}>
            {children}
        </UserContext.Provider>
    );
};
```

### 2.2 Composants principaux

#### `App.jsx`
- **Fonction** : Point d'entrée de l'application.
- **Props** : Aucune.
- **State** : Aucun.
- **Composants enfants** : `MainPage.jsx`.

#### `MainPage.jsx`
- **Fonction** : Gère la navigation et l'affichage principal.
- **Props** : Aucune.
- **State** : `currentPage (String)`, `user (Object)`.
- **Composants enfants** : `NavigationPanel.jsx`, `Feed.jsx`, `User.jsx`, `Result.jsx`, `AsideAdmin.jsx`.

### 2.3 Gestion des utilisateurs

#### `NavigationPanel.jsx`
- **Fonction** : Barre de navigation permettant connexion/déconnexion.
- **Props** : Aucune.
- **State** : Aucun.
- **Composants enfants** : `Login.jsx`, `Logout.jsx`.

#### `Login.jsx`
- **Fonction** : Gère la connexion utilisateur.
- **Props** : Aucune.
- **State** : `email (String)`, `password (String)`.

#### `Logout.jsx`
- **Fonction** : Gère la déconnexion.
- **Props** : Aucune.
- **State** : Aucun.

### 2.4 Gestion des messages

#### `Feed.jsx`
- **Fonction** : Affiche les messages du forum ouvert.
- **Props** : `messages (Array)`, `user (Object)`.
- **State** : `searchTerm (String)`, `filteredMessages (Array)`.
- **Composants enfants** : `SearchBar.jsx`, `MessageList.jsx`, `AddMessage.jsx`.

#### `MessageList.jsx`
- **Fonction** : Affiche une liste de messages.
- **Props** : `messages (Array)`, `onDelete (Function)`.
- **State** : Aucun.
- **Composants enfants** : `Message.jsx`.

#### `Message.jsx`
- **Fonction** : Affiche un message.
- **Props** : `author (String)`, `content (String)`, `timestamp (Date)`.
- **State** : `isEditing (Boolean)`.
- **Composants enfants** : `ReplyList.jsx`.

#### `ReplyList.jsx`
- **Fonction** : Liste des réponses d'un message.
- **Props** : `replies (Array)`.
- **State** : Aucun.
- **Composants enfants** : `Reply.jsx`.

#### `Reply.jsx`
- **Fonction** : Affiche une réponse.
- **Props** : `reply (Object)`.
- **State** : Aucun.

### 2.5 Fonctionnalités administratives

#### `AsideAdmin.jsx`
- **Fonction** : Interface administrateur.
- **Props** : `adminActions (Object)`.
- **State** : `selectedAction (String)`.
- **Composants enfants** : `AsideMenu.jsx`, `AsideValidation.jsx`.

#### `AsideValidation.jsx`
- **Fonction** : Validation des inscriptions.
- **Props** : `pendingUsers (Array)`, `onValidate (Function)`, `onReject (Function)`.
- **State** : `selectedUser (Object)`, `loading (Boolean)`, `error (String)`.
- **Composants enfants** : `AsideValidationUser.jsx`.

### 2.6 Recherche

#### `SearchBar.jsx`
- **Fonction** : Recherche de messages.
- **Props** : `onSearch (Function)`, `placeholder (String, optionnel)`.
- **State** : `query (String)`.

## 3. Architecture globale du projet

- **React Router** pour la gestion des routes.
- **`useContext`** pour gérer l'état global de l'utilisateur.
- **Requêtes API** gérées par `server_request.jsx` et `messages_request.jsx`.
- **Organisation en composants modulaires et réutilisables.**

## 4. Analyse des interactions et fonctionnalités

- **Connexion/inscription** : `Login.jsx`, `UserContext.jsx`.
- **Ajout/Suppression de messages** : `AddMessage.jsx`, `MessageList.jsx`.
- **Gestion administrateur** : `AsideAdmin.jsx`, `AsideValidation.jsx`.
- **Recherche avancée** : `SearchBar.jsx`.

