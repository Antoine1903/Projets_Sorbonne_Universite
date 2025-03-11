# Rapport de mi-projet : Organiz'Asso

## 1. Graphe des dépendances des composants React

Le graphe suivant montre les relations entre les composants React du projet, mettant en évidence les dépendances mutuelles et la hiérarchie des composants.

```
App (index.jsx)
├── MainPage.jsx
│   ├── NavigationPanel.jsx
│   │   ├── Login.jsx
│   │   ├── Logout.jsx
│   │   ├── Signup.jsx
│   ├── Feed.jsx
│   │   ├── SearchBar.jsx
│   │   ├── MessageList.jsx
│   │   │   ├── Message.jsx
│   │   │   │   ├── ReplyList.jsx
│   │   │   │   │   ├── Reply.jsx
│   │   │   │   ├── EditMessage.jsx
│   │   │   │   ├── DeleteMessage.jsx
│   │   ├── AddMessage.jsx
│   ├── UserProfile.jsx
│   │   ├── UserInfo.jsx
│   │   ├── UserSettings.jsx
│   │   ├── UserMessageList.jsx
│   │   │   ├── Message.jsx
│   │   │   │   ├── ReplyList.jsx
│   │   │   │   │   ├── Reply.jsx
│   │   │   │   ├── EditMessage.jsx
│   │   │   │   ├── DeleteMessage.jsx
│   ├── SearchResults.jsx
│   │   ├── MessageList.jsx
│   │   │   ├── Message.jsx
│   │   │   │   ├── ReplyList.jsx
│   │   │   │   │   ├── Reply.jsx
│   │   │   │   ├── EditMessage.jsx
│   │   │   │   ├── DeleteMessage.jsx
│   ├── AdminPanel.jsx
│   │   ├── AdminMenu.jsx
│   │   ├── UserValidation.jsx
│   │   │   ├── ValidateUser.jsx
│   │   ├── AdminFeed.jsx
│   │   │   ├── MessageList.jsx
│   │   │   │   ├── Message.jsx
│   │   │   │   │   ├── ReplyList.jsx
│   │   │   │   │   │   ├── Reply.jsx
│   │   │   │   │   ├── EditMessage.jsx
│   │   │   │   │   ├── DeleteMessage.jsx
│   │   │   ├── AddMessage.jsx
├── api/messagesAPI.jsx
├── api/userAPI.jsx
├── api/serverConfig.jsx
├── context/UserContext.jsx
```

## 2. Liste des composants et leur description

### **App**

- **Fonction** : Composant principal gérant la navigation et l'état global.
- **Props** : Aucune directe.
- **State** : Utilisateur connecté, statut administrateur.
- **Composants inclus** : MainPage.

### **MainPage**

- **Fonction** : Page principale affichant la navigation et le contenu central.
- **Props** : Aucune directe.
- **State** : Aucun.
- **Composants inclus** : NavigationPanel, Feed, UserProfile, SearchResults, AdminPanel.

### **NavigationPanel**

- **Fonction** : Gère l'authentification des utilisateurs.
- **Props** : Aucune.
- **State** : Aucun.
- **Composants inclus** : Login, Logout, Signup.

### **Feed**

- **Fonction** : Affiche les messages du forum.
- **Props** : Aucun.
- **State** : Liste des messages.
- **Composants inclus** : SearchBar, MessageList, AddMessage.

### **MessageList**

- **Fonction** : Liste des messages affichés sur le forum.
- **Props** : Liste des messages.
- **State** : Aucun.
- **Composants inclus** : Message.

### **Message**

- **Fonction** : Affichage d'un message avec ses réponses.
- **Props** : Contenu, auteur, date.
- **State** : Aucun.
- **Composants inclus** : ReplyList, EditMessage, DeleteMessage.

### **ReplyList**

- **Fonction** : Liste des réponses à un message.
- **Props** : Liste des réponses.
- **State** : Aucun.
- **Composants inclus** : Reply.

### **Reply**

- **Fonction** : Affichage d'une réponse.
- **Props** : Contenu, auteur, date.
- **State** : Aucun.
- **Composants inclus** : Aucun.

### **UserProfile**

- **Fonction** : Affichage du profil utilisateur.
- **Props** : Aucune.
- **State** : Aucun.
- **Composants inclus** : UserInfo, UserSettings, UserMessageList.

### **AdminPanel**

- **Fonction** : Gère les actions administratives.
- **Props** : Aucune.
- **State** : Aucun.
- **Composants inclus** : AdminMenu, UserValidation, AdminFeed.

### **UserValidation**

- **Fonction** : Gestion des inscriptions et validation des utilisateurs.
- **Props** : Liste des utilisateurs en attente.
- **State** : Aucun.
- **Composants inclus** : ValidateUser.

### **AdminFeed**

- **Fonction** : Affichage des discussions du forum privé.
- **Props** : Aucun.
- **State** : Aucun.
- **Composants inclus** : MessageList, AddMessage.

### **Hooks et API**

- **useAuth.jsx** : Gère l'authentification des utilisateurs.

- **useMessages.jsx** : Gère la récupération et l'envoi des messages.

- **messagesAPI.jsx** : Interface avec l'API pour la gestion des messages.

- **userAPI.jsx** : Interface avec l'API pour la gestion des utilisateurs

- **serverConfig.jsx** : Contient la configuration du serveur.

- **UserContext.jsx** : Gère le contexte global utilisateur.

