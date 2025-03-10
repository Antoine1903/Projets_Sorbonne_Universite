Antoine Lecomte & Yuxiang Zhang

TME 6-7


Question 1.1 :

nb_recepteurs est modifié simultanément par plusieurs récepteurs, ce qui pose un problème de concurrence. Pour garantir la cohérence de ce compteur, il faut introduire un mécanisme de verrouillage à l'aide de sémaphores, pour permettre de synchroniser correctement les accès en écriture sur un message. On crée alors un sémaphore MUTEX qui assure qu’un seul processus (récepteur) modifie nb_recepteurs à la fois. Chaque récepteur doit acquérir MUTEX avant d'incrémenter nb_recepteurs et le libérer ensuite.

EMET (initialisé à 1) : Bloque les émetteurs lorsque le tampon est plein (ils attendent qu’il soit lu par tous les récepteurs).
RECEP[NR] (tous initialisés à 0) : Bloque chaque récepteur tant qu’un message n’est pas disponible.
MUTEX (initialisé à 1) : Garantit l’accès exclusif à nb_recepteurs.


Question 1.2 :

En utilisant plutôt un seul sémaphore RECEP, initialisé à 0 et incrémenté de NR à chaque émission, alors tous les récepteurs pourraient décrémenter ce sémaphore en même temps. Rien ne nous garantit que tous les récepteurs lisent tous le même message avant que l'émetteur n'écrase la valeur du tampon, alors qu'avec un tableau RECEP[1..NR], chaque récepteur dispose de son propre sémaphore individuel donc :
- lorsqu’un message est émis, chaque sémaphore RECEP[i] est incrémenté individuellement.
- chaque récepteur ne peut décrémenter que son propre sémaphore, ce qui garantit qu’il accède bien au bon message.
- l’émetteur est ainsi assuré que tous les récepteurs ont lu le message avant d'en envoyer un autre.

C'est le dernier récepteur qui termine la lecture du message (celui qui fait nb_recepteurs == NR) et exécute V(EMET) qui débloque l’émetteur, car une fois qu’un récepteur a lu le message, il incrémente nb_recepteurs en faisant successivement P(MUTEX), nb_recepteurs++, V(MUTEX).


Question 2.1 :




Question 2.2 :

