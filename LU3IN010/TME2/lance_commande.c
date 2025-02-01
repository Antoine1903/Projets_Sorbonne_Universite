#include <stdio.h>
#include <stdlib.h>

void lance_commande(char *commande) {

    int resultat = system(commande);

    if (resultat == -1) {
        // Si system() échoue
        printf("Erreur lors de l'exécution de la commande");
    } else {

        if (WIFEXITED(resultat) && WEXITSTATUS(resultat) != 0) {
            // Si le processus s'est terminé normalement avec une erreur
            printf("La commande a échoué avec le code de sortie : %d\n", WEXITSTATUS(resultat));
        }
    }
}

int main() {
    // Exemple d'appel à la fonction avec une commande
    lance_commande("ls");
    lance_commande("nonexistent_command");  // Exemple d'échec

    return 0;
}
