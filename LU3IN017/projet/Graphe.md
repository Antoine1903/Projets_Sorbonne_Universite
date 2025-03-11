# Document de mi-projet : Organiz’asso

## 1. Graphe des dépendances réciproques des composants

Le graphe suivant montre les relations entre les composants React du projet, mettant en évidence les dépendances mutuelles et la hiérarchie des composants.

```
App (index.jsx)
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
├── api/serverConfig.jsx
└── context/UserContext.jsx
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

### 2.2 Gestion des utilisateurs

#### `Signup.jsx`
- **Fonction** : Permet à un nouvel utilisateur de s'inscrire.
- **Props** : Aucune.
- **State** : `name (String)`, `email (String)`, `password (String)`.

#### `UserProfile.jsx`
- **Fonction** : Affiche le profil d'un utilisateur avec ses messages publiés.
- **Props** : `user (Object)`.
- **State** : Aucun.
- **Composants enfants** : `UserInfo.jsx`, `UserMessageList.jsx`.

### 2.3 Fonctionnalités administratives

#### `AdminPanel.jsx`
- **Fonction** : Interface de gestion des administrateurs.
- **Props** : `adminActions (Object)`.
- **State** : `selectedAction (String)`.
- **Composants enfants** : `AdminMenu.jsx`, `UserValidation.jsx`.

#### `UserValidation.jsx`
- **Fonction** : Permet aux administrateurs d'approuver ou rejeter l'inscription des utilisateurs.
- **Props** : `pendingUsers (Array)`, `onValidate (Function)`, `onReject (Function)`.
- **State** : `selectedUser (Object)`, `loading (Boolean)`, `error (String)`.
- **Composants enfants** : `ValidateUser.jsx`.

### 2.4 Recherche et filtres avancés

#### `SearchBar.jsx`
- **Fonction** : Recherche avancée avec filtres.
- **Props** : `onSearch (Function)`, `filters (Object)`.
- **State** : `query (String)`, `selectedFilters (Object)`.

## 3. Architecture globale du projet

- **React Router** pour la gestion des routes.
- **`useContext`** pour gérer l'état global de l'utilisateur.
- **Requêtes API** gérées par `server_request.jsx` et `messages_request.jsx`.
- **Organisation en composants modulaires et réutilisables.**

## 4. Analyse des interactions et fonctionnalités

- **Connexion/inscription** : `Signup.jsx`, `Login.jsx`, `UserContext.jsx`.
- **Ajout/Suppression de messages** : `AddMessage.jsx`, `MessageList.jsx`, `UserProfile.jsx`.
- **Gestion administrateur** : `AdminPanel.jsx`, `UserValidation.jsx`.
- **Recherche avancée** : `SearchBar.jsx` avec filtres par mots-clés, auteur et date.
- **Contrôle des permissions** : `MainPage.jsx` gère l'accès des utilisateurs et administrateurs.

