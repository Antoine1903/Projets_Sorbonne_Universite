/* Diffusion tampon 1 case */

#include <stdio.h> 
#include <unistd.h> 
#include <stdlib.h> 
#include <signal.h> 
#include <libipc.h>

/************************************************************/

/* definition des parametres */ 

#define NE 2     /*  Nombre d'emetteurs         */ 
#define NR 5     /*  Nombre de recepteurs       */ 

/************************************************************/

/* definition des semaphores */ 

int EMET, MUTEX;
int RECEP[NR];
        
/************************************************************/

/* definition de la memoire partagee */ 

struct {
	int message;
	int nb_recepteurs;
}*sp;

/************************************************************/

/* variables globales */ 
int emet_pid[NE], recep_pid[NR]; 

/************************************************************/

/* traitement de Ctrl-C */ 

void handle_sigint(int sig) { 
	int i;
	for (i = 0; i < NE; i++) kill(emet_pid[i], SIGKILL); 
	for (i = 0; i < NR; i++) kill(recep_pid[i], SIGKILL); 
	det_sem(); 
	det_shm((char *)sp); 
} 

/************************************************************/

/* fonction EMETTEUR */ 

void emetteur() {
    while (1) {
        P(EMET);  // Attente d'une case libre
        sp->message = rand() % 100;  // Envoi d'un message aléatoire
        printf("Émetteur %d a envoyé %d\n", getpid(), sp->message);

        // Signale tous les récepteurs pour qu'ils puissent lire
        for (int i = 0; i < NR; i++) {
            V(RECEP[i]);
        }

        // Attente que tous les récepteurs aient lu le message
        P(MUTEX);
        while (sp->nb_recepteurs < NR) {
            V(MUTEX);
            sleep(1);  // Attendre avant de vérifier à nouveau
            P(MUTEX);
        }

        // Réinitialisation du nombre de récepteurs
        sp->nb_recepteurs = 0;
        V(MUTEX);
        V(EMET);  // Libère la case pour le prochain émetteur
    }
}

/************************************************************/

/* fonction RECEPTEUR */ 

void recepteur(int id) {
	while (1) {
		P(RECEP[id]);
		printf("Récepteur %d a reçu %d\n", getpid(), sp->message);

		P(MUTEX);
		sp->nb_recepteurs++;
		if (sp->nb_recepteurs == NR) {
			sp->nb_recepteurs = 0;
			V(EMET);
		}
		V(MUTEX);
	}
}

/************************************************************/

int main() { 
	struct sigaction action;
	/* autres variables (a completer) */

	setbuf(stdout, NULL);

	/* Creation du segment de memoire partagee */

	sp = (struct*)init_shm(sizeof(*sp));
	sp->nb_recepteurs = 0;

	/* creation des semaphores et initialisation des semaphores */ 

	EMET = creer_sem(1);
	MUTEX = creer_sem(1);
	init_un_sem(EMET, 1);
	init_un_sem(MUTEX, 1);

	for (int i = 0; i < NR; i++) {
		RECEP[i] = creer_sem(1);
		init_un_sem(RECEP[i], 0);
	}

	/* creation des processus emetteurs */ 

	for (int i = 0; i < NE; i++) {
		if ((emet_pid[i] = fork()) == 0) {
			emetteur();
			exit(0);
		}
	}

	/* creation des processus recepteurs */ 

	for (int i = 0; i < NR; i++) {
		if ((recep_pid[i] = fork()) == 0) {
			recepteur(i);
			exit(0);
		}
	}

	/* redefinition du traitement de Ctrl-C pour arreter le programme */ 

	sigemptyset(&action.sa_mask);
	action.sa_flags = 0;
	action.sa_handler = handle_sigint;
	sigaction(SIGINT, &action, 0); 

	pause();                    /* attente du Ctrl-C  */
	return EXIT_SUCCESS;
} 
