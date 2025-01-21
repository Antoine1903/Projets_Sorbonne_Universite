#include <stdio.h>
#include <stdlib.h>
#include "tab.h"
#include <sys/resource.h>

void PrintMem() {
    struct rusage usage;
    getrusage(RUSAGE_SELF, &usage);
    printf("Memory usage: %ld kilobytes\n", usage.ru_maxrss);
}

int main() {
    int tab[NMAX];
    int *heapTab = malloc(NMAX * sizeof(int));

    if (heapTab == NULL) {
        printf("Memory allocation failed!\n");
        return 1;
    }

    // Initialisation et affichage du tableau sur la pile

    // Afficher la mémoire avant et après l'allocation (tests effectués avec NMAX=100000)
    PrintMem();     // Memory usage: 1452 kilobytes
    InitTab(tab, NMAX);
    PrintMem();     // Memory usage: 1756 kilobytes

    PrintTab(tab, NMAX);

    // Initialisation et affichage du tableau sur le tas

    // Afficher la mémoire avant et après l'allocation
    PrintMem();     // Memory usage: 1756 kilobytes
    InitTab(heapTab, NMAX);
    PrintMem();     // Memory usage: 2284 kilobytes

    PrintTab(heapTab, NMAX);

    /* La mémoire en cours d'utilisation n'est pas maximale juste avant l'appel à
    InitTab avec le tableau alloué sur la pile, ce qui signifie qu'elle est allouée
    lors de la déclaration de tab. Le reste de la mémoire utilisée est ajouté pendant
    l'appel à InitTab avec le tableau alloué dynamiquement, car effectivement, au 2ème
    et 3ème appel de PrintMem, l'utilisation de la mémoire est la même, donc il n'y a
    pas eu d'allocation à ce moment. */


    // Tester les fonctions SumTab et MinSumTab
    int min;
    int sum = SumTab(tab, NMAX);
    printf("Sum of elements: %d\n", sum);

    int minSum = MinSumTab(&min, tab, NMAX);
    printf("Sum: %d, Min: %d\n", minSum, min);

    free(heapTab); // Libérer la mémoire allouée

    return 0;
}
