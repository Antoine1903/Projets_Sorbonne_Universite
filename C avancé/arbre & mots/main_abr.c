#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "liste.h"
#include "abr.h"

int main(int argc, char **argv){

  /* a completer. Exercice 3, question 1 */

  if (argc != 3) {
      fprintf(stderr, "Usage: %s <mot_a_rechercher> <nombre_de_repetitions>\n", argv[0]);
      return 1;
  }

  const char *mot_a_rechercher = argv[1];
  int repetitions = atoi(argv[2]);

  // Lire le dictionnaire depuis le fichier
  Lm_mot *liste_mots = lire_dico_Lmot("french_za");
  if (liste_mots == NULL){
      fprintf(stderr, "Erreur lors de la lecture du dictionnaire.\n");
      return 1;
  }

  // Construire l'ABR à partir de la liste de mots
  Nd_mot *abr = Lm2abr(liste_mots);

  // Mesurer le temps de recherche
  clock_t start_time = clock();

  for (int i=0; i<repetitions; i++){
      if (chercher_Nd_mot(abr, mot_a_rechercher)){
          printf("Le mot '%s' a été trouvé.\n", mot_a_rechercher);
      }
      else{
          printf("Le mot '%s' n'a pas été trouvé.\n", mot_a_rechercher);
      }
  }
  clock_t end_time = clock();

  printf("Temps de recherche pour %d répétitions : %f secondes.\n", repetitions, ((double)(end_time - start_time)) / CLOCKS_PER_SEC);

  // Libérer la mémoire
  detruire_abr_mot(abr);
  detruire_Lmot(liste_mots);
  
  return 0;
}

/*

Exercice 5 :

Arbre binaire de recherche (ABR) :

- Efficacité pour la recherche exacte : 
Les ABR sont efficaces pour les opérations de recherche exacte.
Si le mot recherché existe dans le dictionnaire, la recherche sera relativement rapide.

*/