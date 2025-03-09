App (Composant principal gérant la navigation et l'état global. Props : Aucune directe.
State : Utilisateur connecté, statut administrateur.)
|
|-- Auth (Gestion de l'authentification. Props : Aucune directe.
    State : Formulaires de connexion/inscription.)
|   |-- LoginForm (Formulaire de connexion. Props : Aucune.
        State : Email, mot de passe.)
|   |-- SignupForm (Formulaire d'inscription. Props : Aucune.
        State : Email, mot de passe.)
|
|-- Forum (Affichage des fils de discussion. Props : Aucune.
    State : Liste des fils de discussion.)
|   |-- ThreadList (Liste des fils de discussion. Props : Liste des fils.
        State : Aucun.)
|   |   |-- ThreadItem (Affichage d'un fil de discussion. Props : Titre, auteur.
            State : Aucun.)
|   |       |-- MessageList (Liste des messages d'un fil. Props : Liste des fils.
                State : Aucun.)
|   |           |-- MessageItem (Affichage d'un message. Props : Contenu, auteur, date.
                    State : Aucun.)
|
|-- Profile (Affichage du profil utilisateur. Props : Aucune.
    State : Liste des messages postés.)
|   |-- UserMessages (Liste des messages postés par un utilisateur. Props : Liste des         messages.
        State : Aucun.)
|
|-- AdminPanel (Gestion administrative du site. Props : Aucune.
    State : Liste des demandes d'inscription, gestion des rôles.)
    |-- UserValidation (Validation des nouveaux inscrits. Props : Liste des demandes.
        State : Aucun.)
    |-- RoleManagement (Gestion des rôles des utilisateurs. Props : Liste des utilisateurs.
        State : Aucun.)