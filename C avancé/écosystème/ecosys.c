#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include "ecosys.h"

/* PARTIE 1*/
/* Fourni: Part 1, exercice 4, question 2 */


Animal *creer_animal(int x, int y, float energie) {
  Animal *na = (Animal *)malloc(sizeof(Animal));
  assert(na);
  na->x = x;
  na->y = y;
  na->energie = energie;
  na->dir[0] = rand() % 3 - 1;
  na->dir[1] = rand() % 3 - 1;
  na->suivant = NULL;
  return na;
}


/* Fourni: Part 1, exercice 4, question 3 */
Animal *ajouter_en_tete_animal(Animal *liste, Animal *animal) {
  //test qu'il y a bien un seul animal à ajouter en tête
  assert(animal && !animal->suivant);
  animal->suivant = liste;
  return animal;
}

/* A faire. Part 1, exercice 6, question 2 */
void ajouter_animal(int x, int y, float energie, Animal **liste_animal) {
    /*A Completer*/
    assert(0 <= x && x < SIZE_X);
    assert(0 <= y && y < SIZE_Y);

    Animal *na = creer_animal(x, y, energie); // Créer un nouvel animal

    if (*liste_animal == NULL) {
        *liste_animal = na; // Si la liste est vide, la liste va avoir 1 animal
    }
    else {
      na->suivant = *liste_animal;
      *liste_animal = na; // On a ajouté en tête de liste le nouvel animal
    }
}


/* A Faire. Part 1, exercice 6, question 7 */
void enlever_animal(Animal **liste, Animal *animal) {
  /*A Completer*/
  //Vérification qu'il y a bien un animal à enlever et que la liste d'animaux n'est pas vide
  assert(liste && *liste && animal);

  // Cas particulier si l'animal à enlever est le premier de la liste
  if (*liste == animal) {
      *liste = (*liste)->suivant;
      free(animal);
  }

  else{
    //Recherche de l'animal précédent l'animal qui doit être enlevé dans la liste
    Animal *precedent = *liste;
    while (precedent->suivant && precedent->suivant != animal) {
      precedent = precedent->suivant;
    }

    // Vérification si l'animal à enlever a été trouvé dans la liste
    if (precedent->suivant == animal) {
      precedent->suivant = precedent->suivant->suivant;
      free(animal);
    }
  }
}

/* A Faire. Part 1, exercice 6, question 4 */
void liberer_liste_animaux(Animal *liste) {
  /*A Completer*/
  while (liste) {
    Animal *prochain = liste->suivant; // Sauvegarde du pointeur vers l'élément suivant
    free(liste); // Libération de la mémoire de l'élément en cours
    liste = prochain; // Passage à l'élément suivant
  }
}


/* Fourni: part 1, exercice 4, question 4 */
unsigned int compte_animal_rec(Animal *la) {
  if (!la) return 0;
  return 1 + compte_animal_rec(la->suivant);
}

/* Fourni: part 1, exercice 4, question 4 */
unsigned int compte_animal_it(Animal *la) {
  int cpt=0;
  while (la) {
    ++cpt;
    la=la->suivant;
  }
  return cpt;
}



/* Part 1. Exercice 5, question 1, ATTENTION, ce code est susceptible de contenir des erreurs... */
void afficher_ecosys(Animal *liste_proie, Animal *liste_predateur) {
  unsigned int i, j;
  char ecosys[SIZE_X][SIZE_Y];
  Animal *pa=NULL;

  /* on initialise le tableau */
  for (i = 0; i < SIZE_X; ++i) {
    for (j = 0; j < SIZE_Y; ++j) {
      ecosys[i][j]=' ';
    }
  }

  /* on ajoute les proies */
  pa = liste_proie;
  while (pa) {
    ecosys[pa->x][pa->y] = '*';
    pa = pa->suivant;
  }

  /* on ajoute les predateurs */
  pa = liste_predateur;
  while (pa) {
      if ((ecosys[pa->x][pa->y] == '@') || (ecosys[pa->x][pa->y] == '*')) { /* proies aussi present */
        ecosys[pa->x][pa->y] = '@';
      } else {
        ecosys[pa->x][pa->y] = 'O';
      }
    pa = pa->suivant;
  }

  /* on affiche le tableau */
  printf("+");
  for (i = 0; i < SIZE_X; ++i) {
    printf("-");
  }  
  printf("+\n");
  for (j = 0; j < SIZE_Y; ++j) {
    printf("|");
    for (i = 0; i < SIZE_X; ++i) {
      putchar(ecosys[i][j]);
    }
    printf("|\n");
  }
  printf("+");
  for (i = 0; i<SIZE_X; ++i) {
    printf("-");
  }
  printf("+\n");
  int nbproie = compte_animal_it(liste_proie);
  int nbpred = compte_animal_it(liste_predateur);
  
  printf("Nb proies : %5d\tNb predateurs : %5d\n", nbproie, nbpred);
}


void clear_screen() {
  printf("\x1b[2J\x1b[1;1H");  /* code ANSI X3.4 pour effacer l'ecran */
}

/* PARTIE 2*/

/* Part 2. Exercice 4, question 1 */
void bouger_animaux(Animal *la) {
    /*A Completer*/
    while (la) {
      // Définir une direction aléatoire de déplacement
      if (rand() / (float)RAND_MAX <= 0.8){ // p_ch_dir = 0.8
      	la->dir[0] = rand() % 3 - 1;
      	la->dir[1] = rand() % 3 - 1;
      }

      // Mettre à jour les coordonnées en fonction de la nouvelle direction
      la->x = (la->x + la->dir[0] + SIZE_X) % SIZE_X;
      la->y = (la->y + la->dir[1] + SIZE_Y) % SIZE_Y;

      la = la->suivant;
    }
}

/* Part 2. Exercice 4, question 3 */
void reproduce(Animal **liste_animal, double p_reproduce) { // p_reproduce était initialement un float 
   /*A Completer*/
  Animal *courant = *liste_animal;
  while (courant) {
    // Vérifier si l'animal doit se reproduire
    if (rand() / (float)RAND_MAX <= p_reproduce && courant->energie > 1) { // si son énergie est de 1 il ne pourra pas se reproduire car il va mourir avant
    	courant->energie /= 2;
      // Si oui, reproduire l'animal en ajoutant un nouvel animal avec les mêmes attributs (et donc avec la même énergie que l'animal après reproduction
      ajouter_animal(courant->x, courant->y, courant->energie, liste_animal);
    }
    courant = courant->suivant;
  }
}


/* Part 2. Exercice 6, question 1 */
void rafraichir_proies(Animal **liste_proie, int monde[SIZE_X][SIZE_Y]) {
  /*A Completer*/
  // Faire bouger les proies
  bouger_animaux(*liste_proie);

  // Parcourir la liste de proies
  Animal *courant = *liste_proie;
  Animal *precedent = NULL;

  while (courant) {
    // Baisser leur énergie de 1
    courant->energie--;

    // Vérifier si l'énergie est inférieure à 0
    if (courant->energie <= 0) {
      // Supprimer les proies dont l'énergie est inférieure à 0
      if (precedent) {
        precedent->suivant = courant->suivant;
        free(courant);
        courant = precedent->suivant;
      } 
      else {
        *liste_proie = courant->suivant;
        free(courant);
        courant = *liste_proie;
      }
    }
    else {
      // Sinon, passer à l'animal suivant
      precedent = courant;
      courant = courant->suivant;
    }
  }
  // Faire appel à la fonction de reproduction
  reproduce(liste_proie, 0.4); // p_reproduce_proie = 0.4
}

/* Part 2. Exercice 7, question 1 */
Animal *animal_en_XY(Animal *l, int x, int y) {
  /*A Completer*/
  while (l) {
    if (l->x == x && l->y == y) {
      // On a trouvé un animal aux coordonnées spécifiées
      return l;
    }
    l = l->suivant;
  }

  // Aucun animal trouvé aux coordonnées spécifiées
  return NULL;
} 

/* Part 2. Exercice 7, question 2 */
void rafraichir_predateurs(Animal **liste_predateur, Animal **liste_proie) {
  /*A Completer*/
  // Faire bouger les prédateurs
  bouger_animaux(*liste_predateur);

  Animal *courant = *liste_predateur;
  Animal *precedent = NULL;

  while (courant) {
    // Baisser leur énergie de 1
    courant->energie--;

    // Vérifier s'il y a une proie sur la même case que le prédateur
    Animal *proie = animal_en_XY(*liste_proie, courant->x, courant->y);

    if (proie) {
      // La proie est mangée, augmenter l'énergie du prédateur et supprimer la proie
      courant->energie += proie->energie;
      enlever_animal(liste_proie, proie);
    }

    // Vérifier si l'énergie est inférieure à 0
    if (courant->energie <= 0) {
      // Supprimer les prédateurs dont l'énergie est inférieure à 0
      if (precedent) {
        precedent->suivant = courant->suivant;
        free(courant);
        courant = precedent->suivant;
      } 
      else {
        *liste_predateur = courant->suivant;
        free(courant);
        courant = *liste_predateur;
      }
    }
    else {
      // Sinon, passer à l'animal suivant
      precedent = courant;
      courant = courant->suivant;
    }
  }
  // Faire appel à la fonction de reproduction
  reproduce(liste_predateur, 0.5); // p_reproduce_predateur = 0.5
}

/* Part 2. Exercice 5, question 2 */
void rafraichir_monde(int monde[SIZE_X][SIZE_Y]){
   /*A Completer*/
}

