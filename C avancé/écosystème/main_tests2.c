#include <assert.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "ecosys.h"



int main(void) {
  Animal *liste_proie = NULL;
  Animal *liste_predateur = NULL;
  int energie=10;

  // Initialisation du générateur de nombres aléatoires
  srand(time(NULL));

  // Créer 20 proies et 20 prédateurs à des positions aléatoires
  for (int i = 0; i < 20; i++) {
    ajouter_animal(rand() % SIZE_X, rand() % SIZE_Y, energie, &liste_proie);
    ajouter_animal(rand() % SIZE_X, rand() % SIZE_Y, energie, &liste_predateur);
  }

  // Vérifier le nombre d'animaux
  int nb_proies = compte_animal_it(liste_proie);
  int nb_predateurs = compte_animal_rec(liste_predateur);

  assert(nb_proies == 20);
  assert(nb_predateurs == 20);

  // Afficher l'état de l'écosystème
  printf("État initial de l'écosystème :\n");
  afficher_ecosys(liste_proie,liste_predateur);

  printf("Nombre de proies : %d\n", nb_proies);
  printf("Nombre de prédateurs : %d\n", nb_predateurs);



  // Copier l'écosystème actuel dans de nouvelles listes
  Animal *nouvelle_liste_proie = NULL;
  Animal *nouvelle_liste_predateur = NULL;

  // Copier la liste de proies
  Animal *courant = liste_proie;
  while (courant) {
    ajouter_animal(courant->x, courant->y, courant->energie, &nouvelle_liste_proie);
    courant = courant->suivant;
  }

  // Copier la liste de prédateurs
  courant = liste_predateur;
  while (courant) {
    ajouter_animal(courant->x, courant->y, courant->energie, &nouvelle_liste_predateur);
    courant = courant->suivant;
  }

  // Vérifier le nombre d'animaux
  nb_proies = compte_animal_it(nouvelle_liste_proie);
  nb_predateurs = compte_animal_rec(nouvelle_liste_predateur);

  assert(nb_proies == 20);
  assert(nb_predateurs == 20);

  // Afficher l'état des nouvelles listes
  printf("\nÉtat des nouvelles listes :\n");
  afficher_ecosys(nouvelle_liste_proie, nouvelle_liste_predateur);

  printf("Nombre de proies : %d\n", nb_proies);
  printf("Nombre de prédateurs : %d\n", nb_predateurs);



  // Supprimer quelques proies et prédateurs
  enlever_animal(&liste_proie, liste_proie);  // Supprime le premier élément
  enlever_animal(&liste_proie, liste_proie);  // Supprime le deuxième élément
  enlever_animal(&liste_predateur, liste_predateur);  // Supprime le premier élément
  enlever_animal(&liste_predateur, liste_predateur);  // Supprime le deuxième élément

  // Afficher l'état après suppression
  printf("\nÉtat après suppression de quelques proies et prédateurs :\n");
  afficher_ecosys(liste_proie, liste_predateur);

  // Vérifier le nombre d'animaux après suppression
  nb_proies = compte_animal_it(liste_proie);
  nb_predateurs = compte_animal_rec(liste_predateur);

  assert(nb_proies == 18);
  assert(nb_predateurs == 18);

  printf("\nNombre de proies après suppression : %d\n", nb_proies);
  printf("Nombre de prédateurs après suppression : %d\n", nb_predateurs);


  // Libérer la mémoire de toutes les listes et des animaux
  liberer_liste_animaux(liste_proie);
  liberer_liste_animaux(liste_predateur);
  liberer_liste_animaux(nouvelle_liste_proie);
  liberer_liste_animaux(nouvelle_liste_predateur);

  //vérification de la suppression de tous les animaux
  nb_proies = compte_animal_it(liste_proie);
  nb_predateurs = compte_animal_rec(liste_predateur);

  assert(nb_proies == 0);
  assert(nb_predateurs == 0);

  printf("\nNombre de proies après suppression : %d\n", nb_proies);
  printf("Nombre de prédateurs après suppression : %d\n", nb_predateurs);
  
  return 0;
}
