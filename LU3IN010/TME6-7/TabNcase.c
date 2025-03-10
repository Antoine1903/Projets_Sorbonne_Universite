/* Diffusion tampon N case */

#include <stdio.h> 
#include <unistd.h> 
#include <signal.h> 
#include <libipc.h>

/************************************************************/

/* definition des parametres */ 

#define NE 2     /*  Nombre d'emetteurs         */ 
#define NR 5     /*  Nombre de recepteurs       */ 
#define NMAX 3     /*  Taille du tampon           */ 

/************************************************************/

/* definition des semaphores */ 

int mutex;        // Protection de l'accès concurrent
int vide;         // Nombre de cases vides
int plein;        // Nombre de cases pleines


/************************************************************/

/* definition de la memoire partagee */ 

typedef struct {
	int buffer[NMAX];
	int index_ecriture;
	int index_lecture;
}shared_data;

shared_data *sp;

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

void emetteur(int id) {
	int message = 100 + id; // Exemple de message unique pour chaque émetteur
	while (1) {
		P(vide);       // Attente d'une case vide
		P(mutex);      // Accès exclusif au tampon
			
		sp->buffer[sp->index_ecriture] = message;
		printf("Emetteur %d a écrit %d dans la case %d\n", id, message, sp->index_ecriture);
		sp->index_ecriture = (sp->index_ecriture + 1) % NMAX;
			
		V(mutex);      // Libération de l'accès au tampon
		V(plein);      // Signal qu'une case est pleine

		sleep(1);      // Simulation de délai
	}
}

/************************************************************/

/* fonction RECEPTEUR */ 

void recepteur(int id) {
    while (1) {
        P(plein);      // Attente d'une case pleine
        P(mutex);      // Accès exclusif au tampon

        int message = sp->buffer[sp->index_lecture];
        printf("Recepteur %d a lu %d de la case %d\n", id, message, sp->index_lecture);
        sp->index_lecture = (sp->index_lecture + 1) % NMAX;

        V(mutex);      // Libération de l'accès au tampon
        V(vide);       // Signal qu'une case est vide

        sleep(1);      // Simulation de traitement
    }
}

/************************************************************/

int main() { 
    struct sigaction action;
	/* autres variables (a completer) */
    
    setbuf(stdout, NULL);

/* Creation du segment de memoire partagee */

	sp = (shared_data *)init_shm(sizeof(shared_data));
    sp->index_ecriture = 0;
    sp->index_lecture = 0;

/* creation des semaphores */ 

	mutex = creer_sem(1);       // Sémaphore pour l'exclusion mutuelle
    vide = creer_sem(NMAX);     // N cases vides au début
    plein = creer_sem(0);       // 0 cases pleines au début

/* initialisation des semaphores */ 

    init_un_sem(mutex, 1);  // Exclusion mutuelle : initialisé à 1
    init_un_sem(vide, NMAX); // NMAX cases vides
    init_un_sem(plein, 0);   // Aucune case pleine au début
    
/* creation des processus emetteurs */ 

	for (int i = 0; i < NE; i++) {
        if ((emet_pid[i] = fork()) == 0) {
            emetteur(i);
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

    pause();                     /* attente du Ctrl-C */
    return EXIT_SUCCESS;
}