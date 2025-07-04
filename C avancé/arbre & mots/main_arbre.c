#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "arbre_lexicographique.h"


int main(int argc, char **argv){
  
  /* a completer. Exercice 4, question 4 */

  if (argc != 3) {
      fprintf(stderr, "Usage: %s <mot_a_rechercher> <nombre_de_repetitions>\n", argv[0]);
      return 1;
  }

  char *mot_a_rechercher = argv[1];
  int repetitions = atoi(argv[2]);


  PNoeud dico = lire_dico("french_za");
  if (dico == NULL){
      fprintf(stderr, "Erreur lors de la lecture du dictionnaire.\n");
      return 1;
  }

  // Mesurer le temps de recherche
  clock_t start_time = clock();

  for (int i=0; i<repetitions; i++){
      if (rechercher_mot(dico, mot_a_rechercher)){
          printf("Le mot '%s' est présent dans le dictionnaire.\n", mot_a_rechercher);
      }
      else{
          printf("Le mot '%s' n'est pas présent dans le dictionnaire.\n", mot_a_rechercher);
      }
  }

  clock_t end_time = clock();
  printf("Temps de recherche pour %d répétitions : %f secondes.\n", repetitions, ((double)(end_time - start_time)) / CLOCKS_PER_SEC);

  // Libérer la mémoire du dictionnaire
  detruire_dico(dico);

  return 0;
}

/*

Exercice 5 :

Arbre Lexicographique :

- Efficacité pour les recherches par préfixe : 
Les arbres lexicographiques sont bien adaptés aux recherches par préfixe.
Si le mot recherché est un préfixe, la recherche sera efficace.

- Recherche plus générale : 
Les arbres lexicographiques peuvent être utilisés pour des recherches plus générales.

*/