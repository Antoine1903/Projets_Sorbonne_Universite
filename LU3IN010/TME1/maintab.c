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
    InitTab(tab, NMAX);
    PrintTab(tab, NMAX);

    // Initialisation et affichage du tableau sur le tas
    InitTab(heapTab, NMAX);
    PrintTab(heapTab, NMAX);

    // Tester les fonctions SumTab et MinSumTab
    int min;
    int sum = SumTab(tab, NMAX);
    printf("Sum of elements: %d\n", sum);

    int minSum = MinSumTab(&min, tab, NMAX);
    printf("Sum: %d, Min: %d\n", minSum, min);

    // Afficher la mémoire avant et après l'allocation
    PrintMem();

    free(heapTab); // Libérer la mémoire allouée
    return 0;
}
