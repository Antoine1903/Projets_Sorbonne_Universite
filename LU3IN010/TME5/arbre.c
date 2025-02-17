#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

void creer_arbre(int niveau) {
    if (niveau == 0) {
        sleep(30); // Chaque processus dort
        printf("Processus %d terminé (niveau %d)\n", getpid(), niveau);
        return;
    }

    pid_t gauche, droit;

    gauche = fork();
    if (gauche == 0) {
        printf("Processus %d créé par %d (gauche, niveau %d)\n", getpid(), getppid(), niveau);
        creer_arbre(niveau - 1);
        exit(0);
    }

    droit = fork();
    if (droit == 0) {
        printf("Processus %d créé par %d (droit, niveau %d)\n", getpid(), getppid(), niveau);
        creer_arbre(niveau - 1);
        exit(0);
    }

    wait(NULL);
    wait(NULL);

    sleep(30);
    printf("Processus %d terminé (niveau %d)\n", getpid(), niveau);
}


int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <niveau>\n", argv[0]);
        return 1;
    }

    int L = atoi(argv[1]);
    if (L < 0) {
        fprintf(stderr, "Le niveau doit être un entier positif.\n");
        return 1;
    }

    printf("Processus racine %d démarré (niveau %d)\n", getpid(), L);
    creer_arbre(L);

    return 0;
}
