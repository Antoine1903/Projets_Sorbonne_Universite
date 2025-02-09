#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <malloc.h>
#include <sched.h>

#define LONGTIME 8E8
void ProcLong(int *);
void ProcCourt(int *);

// Exemple de processus long (une simple bouble),
// Chaque processus long cr�e a son tour 4 processus courts
//
void ProcLong(int *pid) {
  long i;
  static int cpt = 0;

  for (i=0;i<LONGTIME;i++) {
    if (i%(long)(LONGTIME/4) == 0)  {
      int *tcpt = (int *) malloc(sizeof(int));
      *tcpt = cpt;
      CreateProc((function_t)ProcCourt,(void *)tcpt, 10);
      cpt++;
    }
    if (i%(long)(LONGTIME/100) == 0)
      printf("Proc. Long %d - %ld\n",*pid, i);
  }
  printf("############ FIN LONG %d\n\n", *pid );
}


// Processus court
void ProcCourt(int *pid) {
  long i;

  for (i=0;i<LONGTIME/10;i++)
    if (i%(long)(LONGTIME/100) == 0)
      printf("Proc. Court %d - %ld\n",*pid, i);
  printf("############ FIN COURT %d\n\n", *pid );
}




// Exemples de primitive d'election definie par l'utilisateur
// Remarques : les primitives d'election sont appel�es directement
//             depuis la librairie. Elles ne sont app�l�es que si au
//             moins un processus est � l'etat pret (RUN)
//             Ces primitives manipulent la table globale des processus
//             d�finie dans sched.h


// Election al�atoire
int RandomElect(void) {
  int i;

  printf("RANDOM Election !\n");

  do {
    i = (int) ((float)MAXPROC*rand()/(RAND_MAX+1.0));
  } while (Tproc[i].flag != RUN);

  return i;
}


int SJFElect(void) {
  int i, p = -1;

  // Trouver le premier processus en état RUN
  for (i = 0; i < MAXPROC; i++) {
      if (Tproc[i].flag == RUN) {
          p = i;
          break;
      }
  }

  // Si aucun processus n'est en état RUN, retourner -1 (aucune élection possible)
  if (p == -1) {
      return -1;
  }

  // Parcourir les processus restants pour trouver celui avec la plus courte durée
  for (; i < MAXPROC; i++) {
      if (Tproc[i].flag == RUN && Tproc[i].duration < Tproc[p].duration) {
          p = i;
      }
  }

  return p;
}


// Approximation SJF
int ApproxSJF(void) {
    int i, p = -1;
    float priority, temp_priority;

    // Initialiser la priorité la plus faible possible
    priority = __FLT_MAX__;

    // Parcourir tous les processus pour trouver celui avec la priorité la plus élevée
    for (i = 0; i < MAXPROC; i++) {
        if (Tproc[i].flag == RUN) {
            
            // Calcul de la priorité en tenant compte du vieillissement
            // Plus le processus attend longtemps, plus la priorité augmente
            temp_priority = Tproc[i].ncpu - (0.2 * Tproc[i].waiting_time);
            
            // Sélectionner le processus avec la plus petite priorité (durée CPU ajustée par vieillissement)
            if (temp_priority < priority) {
                priority = temp_priority;
                p = i;
            }
        }
    }

    // Retourner l'indice du processus élu ou -1 si aucun n'est en état RUN
    return p;
}


int main (int argc, char *argv[]) {
  int i;
  int *j;  

  // Cr�er les processus long
  for  (i = 0; i < 2; i++) {
    j = (int *) malloc(sizeof(int));
    *j= i;
    CreateProc((function_t)ProcLong,(void *)j, 80);
  }



  // Definir une nouvelle primitive d'election avec un quantum de 0.5 seconde
  SchedParam(NEW, 1, RandomElect);

  // Lancer l'ordonnanceur en mode non "verbeux"
  sched(0);     

  // Imprimer les statistiques
  PrintStat();

  return EXIT_SUCCESS;

}
