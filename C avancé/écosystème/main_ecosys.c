#include <assert.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <strings.h>
#include "ecosys.h"



#define NB_PROIES 20
#define NB_PREDATEURS 20
#define T_WAIT 300000


/* Parametres globaux de l'ecosysteme (externes dans le ecosys.h)*/
float p_ch_dir=0.8;
float p_reproduce_proie=0.4;
float p_reproduce_predateur=0.5;
int temps_repousse_herbe=-15;


int main(void) {
 
  /* A completer. Part 2:
   * exercice 4, questions 2 et 4 
   * exercice 6, question 2
   * exercice 7, question 3
   * exercice 8, question 1
   */

  // Créer une liste avec un seul animal à une position définie
  Animal *liste_animaux = NULL;
  ajouter_animal(5, 5, 10, &liste_animaux);

  // Afficher l'état initial de l'écosystème
  printf("État initial de l'écosystème :\n");
  afficher_ecosys(liste_animaux, NULL);
  
  // Initialisation du générateur de nombres aléatoires
  srand(time(NULL));

  // Faire déplacer l'animal dans une direction définie (=modification : enlever l'aléa et paramétrer directement les valeurs de dir[0] et dir[1] dans le corps de la fonction)
  bouger_animaux(liste_animaux);

  // Afficher l'état après le déplacement
  printf("\nÉtat après déplacement de l'animal :\n");
  afficher_ecosys(liste_animaux, NULL);

  // Reproduire les animaux avec un taux de reproduction de 1
  reproduce(&liste_animaux, 1.0);

  // Afficher l'état après la reproduction
  printf("\nÉtat après reproduction des animaux :\n");
  afficher_ecosys(liste_animaux, NULL);

  // Libérer la mémoire de la liste d'animaux
  liberer_liste_animaux(liste_animaux);



  // Créer une liste avec 20 proies à des positions aléatoires
  Animal *liste_proies = NULL;
  int energie_proie = 10;
  for (int i = 0; i < NB_PROIES; i++) {
    ajouter_animal(rand() % SIZE_X, rand() % SIZE_Y, energie_proie, &liste_proies);
  }

  // Créer une liste avec 20 prédateurs à des positions aléatoires
  Animal *liste_predateurs = NULL;
  int energie_predateur = 10;
  for (int i = 0; i < NB_PREDATEURS; i++) {
    ajouter_animal(rand() % SIZE_X, rand() % SIZE_Y, energie_predateur, &liste_predateurs);
  }

  // Afficher l'état initial de l'écosystème
  printf("État initial de l'écosystème :\n");
  afficher_ecosys(liste_proies, liste_predateurs);

  // Boucle de mise à jour jusqu'à ce qu'il n'y ait plus de proies ou 200 itérations
  int max_iterations = 200;
  for (int i = 1; i <= max_iterations && (liste_proies || liste_predateurs); i++) {
    printf("\nÉtat après %d itérations :\n", i);

    // Mise à jour des proies et prédateurs
    rafraichir_proies(&liste_proies, NULL);
    rafraichir_predateurs(&liste_predateurs, &liste_proies);

    // Afficher l'état actuel de l'écosystème
    afficher_ecosys(liste_proies, liste_predateurs);

    // Pause pour visualiser l'état
    usleep(T_WAIT);
  }

  // Libérer la mémoire des listes d'animaux
  liberer_liste_animaux(liste_proies);
  liberer_liste_animaux(liste_predateurs);

  return 0;
}

