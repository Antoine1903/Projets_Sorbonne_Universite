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

### **Login**  
- **Fonction** : Permet à un utilisateur de se connecter.  
- **Props** : `onLoginSuccess(user)` – Fonction appelée après une connexion réussie.  
- **State** : `email` (string), `password` (string), `loading` (bool) – État du formulaire et de la requête.  
- **Composants inclus** : Aucun.  

### **Logout**  
- **Fonction** : Permet à un utilisateur de se déconnecter.  
- **Props** : `onLogout()` – Fonction déclenchée à la déconnexion.  
- **State** : Aucun.  
- **Composants inclus** : Aucun.  

### **Signup**  
- **Fonction** : Permet à un utilisateur de créer un compte.  
- **Props** : `onSignupSuccess(user)` – Fonction appelée après l'inscription.  
- **State** : `email` (string), `password` (string), `confirmPassword` (string), `loading` (bool) – État du formulaire et de la requête.  
- **Composants inclus** : Aucun.

### **Feed**

- **Fonction** : Affiche les messages du forum.
- **Props** : Aucun.
- **State** : Liste des messages.
- **Composants inclus** : SearchBar, MessageList, AddMessage.

### **SearchBar**  
- **Fonction** : Permet d’effectuer une recherche dans les messages.  
- **Props** : `onSearch(query)` – Fonction appelée lors d’une recherche.  
- **State** : `query` (string) – Terme recherché.  
- **Composants inclus** : Aucun.

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

### **UserInfo**  
- **Fonction** : Affiche les informations d’un utilisateur.  
- **Props** : `user` (objet) – Données de l’utilisateur.  
- **State** : Aucun.  
- **Composants inclus** : Aucun.  

### **UserSettings**  
- **Fonction** : Permet à un utilisateur de modifier ses paramètres (email, mot de passe, préférences).  
- **Props** : `user` (objet) – Informations de l’utilisateur actuel.  
- **State** : `email` (string), `password` (string), `notifications` (bool) – États modifiables.  
- **Composants inclus** : Aucun.  

### **UserMessageList**  
- **Fonction** : Affiche les messages publiés par un utilisateur.  
- **Props** : `userId` (string) – Identifiant de l’utilisateur.  
- **State** : `messages` (array) – Liste des messages.  
- **Composants inclus** : `Message`.  

### **SearchResults**  
- **Fonction** : Affiche les résultats d’une recherche de messages.  
- **Props** : `results` (array) – Liste des messages trouvés.  
- **State** : Aucun.  
- **Composants inclus** : `MessageList`.  

### **AdminMenu**  
- **Fonction** : Menu permettant d’accéder aux outils d’administration.  
- **Props** : Aucun.  
- **State** : `selectedSection` (string) – Section en cours d’affichage.  
- **Composants inclus** : Aucun.  

### **ValidateUser**  
- **Fonction** : Permet d’approuver ou rejeter les utilisateurs en attente.  
- **Props** : `user` (objet) – Informations de l’utilisateur à valider.  
- **State** : Aucun.  
- **Composants inclus** : Aucun.  

### **Hooks et API**

- **messagesAPI.jsx** : Interface avec l'API pour la gestion des messages.

- **userAPI.jsx** : Interface avec l'API pour la gestion des utilisateurs

- **serverConfig.jsx** : Contient la configuration du serveur.

- **UserContext.jsx** : Gère le contexte global utilisateur.

