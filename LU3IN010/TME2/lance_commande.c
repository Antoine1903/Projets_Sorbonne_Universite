#include <stdio.h>
#include <stdlib.h>

void lance_commande(char *commande) {
    
    int resultat = system(commande);

    if (resultat == -1) {
        // Si system() échoue
        printf("Erreur lors de l'exécution de la commande : %s\n", commande);
    } else {
        // Si le processus s'est terminé normalement mais avec une erreur
        if (WIFEXITED(resultat) && WEXITSTATUS(resultat) != 0) {
            printf("La commande '%s' a échoué avec le code de sortie : %d\n", commande, WEXITSTATUS(resultat));
        }
    }
}

int main(int argc, char *argv[]) {
    
    if (argc < 2) {
        printf("Aucune commande n'a été fournie.\n");
        return 1;
    }

    // Parcourir tous les arguments (à partir de argv[1] jusqu'à argv[argc-1])
    for (int i = 1; i < argc; i++) {
        printf("Exécution de la commande : %s\n", argv[i]);
        lance_commande(argv[i]);
    }

    return 0;
}
