#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/times.h>  // Pour times()

void lance_commande(char *commande) {
    struct tms start_time, end_time;
    clock_t start_clock, end_clock;

    // Récupérer l'heure avant l'exécution de la commande
    start_clock = times(&start_time);

    // Exécution de la commande avec system()
    int resultat = system(commande);

    // Récupérer l'heure après l'exécution de la commande
    end_clock = times(&end_time);

    if (resultat == -1) {
        // Si system() échoue
        printf("Erreur lors de l'exécution de la commande : %s\n", commande);
    } else {
        // Si le processus s'est terminé normalement mais avec une erreur
        if (WIFEXITED(resultat) && WEXITSTATUS(resultat) != 0) {
            printf("La commande '%s' a échoué avec le code de sortie : %d\n", commande, WEXITSTATUS(resultat));
        }

        // Calcul du temps d'exécution en mode utilisateur et système
        long user_time = end_time.tms_utime - start_time.tms_utime;
        long system_time = end_time.tms_stime - start_time.tms_stime;

        // Conversion du temps en secondes et microsecondes
        double user_time_sec = user_time / (double)sysconf(_SC_CLK_TCK);
        double system_time_sec = system_time / (double)sysconf(_SC_CLK_TCK);

        // Affichage du temps d'exécution
        printf("Temps d'exécution de la commande '%s':\n", commande);
        printf("  Mode utilisateur: %.6f secondes\n", user_time_sec);
        printf("  Mode système: %.6f secondes\n", system_time_sec);
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
