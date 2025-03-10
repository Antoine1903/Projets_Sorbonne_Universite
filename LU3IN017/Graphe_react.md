Rapport de mi-projet : Organiz'Asso

Graphe des dépendances des composants React


App 
|
|-- Auth 
|   |-- LoginForm 
|   |-- SignupForm 
|
|-- Forum 
|   |-- ThreadList 
|   |   |-- ThreadItem 
|   |       |-- MessageList 
|   |           |-- MessageItem 
|
|-- Profile 
|   |-- UserMessages 
|
|-- AdminPanel 
    |-- UserValidation 
    |-- RoleManagement 



Liste des composants et leur description


App

Fonction : Composant principal gérant la navigation et l'état global.

Props : Aucune directe.

State : Utilisateur connecté, statut administrateur.

Composants inclus : Auth, Forum, Profile, AdminPanel.


Auth

Fonction : Gestion de l'authentification.

Props : Aucune directe.

State : Formulaires de connexion/inscription.

Composants inclus : LoginForm, SignupForm.


LoginForm

Fonction : Formulaire de connexion.

Props : Aucune.

State : Email, mot de passe.

Composants inclus : Aucun.


SignupForm

Fonction : Formulaire d'inscription.

Props : Aucune.

State : Nom, email, mot de passe.

Composants inclus : Aucun.


Forum

Fonction : Affichage des fils de discussion.

Props : Aucune.

State : Liste des fils de discussion.

Composants inclus : ThreadList.


ThreadList

Fonction : Liste des fils de discussion.

Props : Liste des fils.

State : Aucun.

Composants inclus : ThreadItem.


ThreadItem

Fonction : Affichage d'un fil de discussion.

Props : Titre, auteur.

State : Aucun.

Composants inclus : MessageList.


MessageList

Fonction : Liste des messages d'un fil.

Props : Liste des messages.

State : Aucun.

Composants inclus : MessageItem.


MessageItem

Fonction : Affichage d'un message.

Props : Contenu, auteur, date.

State : Aucun.

Composants inclus : Aucun.


Profile

Fonction : Affichage du profil utilisateur.

Props : Aucune.

State : Liste des messages postés.

Composants inclus : UserMessages.


UserMessages

Fonction : Liste des messages postés par un utilisateur.

Props : Liste des messages.

State : Aucun.

Composants inclus : Aucun.


AdminPanel

Fonction : Gestion administrative du site.

Props : Aucune.

State : Liste des demandes d'inscription, gestion des rôles.

Composants inclus : UserValidation, RoleManagement.


UserValidation

Fonction : Validation des nouveaux inscrits.

Props : Liste des demandes.

State : Aucun.

Composants inclus : Aucun.


RoleManagement

Fonction : Gestion des rôles des utilisateurs.

Props : Liste des utilisateurs.

State : Aucun.

Composants inclus : Aucun.
