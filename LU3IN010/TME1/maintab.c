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
    PrintMem(); // Memory usage: 1179648 kilobytes
    
    int tab[NMAX];
    PrintMem(); // Memory usage: 1196032 kilobytes
    
    int *heapTab = malloc(NMAX * sizeof(int));
    PrintMem(); // Memory usage: 1228800 kilobytes

    if (heapTab == NULL) {
        printf("Memory allocation failed!\n");
        return 1;
    }

    // Initialisation et affichage du tableau sur la pile

    // Afficher la mémoire avant et après l'allocation (tests effectués avec NMAX=1000000)
    PrintMem();     // Memory usage: 1228800 kilobytes
    InitTab(tab, NMAX);
    PrintMem();     // Memory usage: 5128192 kilobytes

    PrintTab(tab, NMAX);

    // Initialisation et affichage du tableau sur le tas

    // Afficher la mémoire avant et après l'allocation
    PrintMem();     // Memory usage: 5128192 kilobytes
    InitTab(heapTab, NMAX);
    PrintMem();     // Memory usage: 9142272 kilobytes

    PrintTab(heapTab, NMAX);

    /* Question 9
    La mémoire en cours d'utilisation n'est pas maximale juste avant l'appel à
    InitTab avec le tableau alloué sur la pile, ce qui signifie qu'elle est allouée
    lors de la déclaration de tab. Le reste de la mémoire utilisée est ajouté pendant
    l'appel à InitTab avec le tableau alloué dynamiquement, car effectivement, au 2ème
    et 3ème appel de PrintMem, l'utilisation de la mémoire est la même, donc il n'y a
    pas eu d'allocation à ce moment. 
    
    Ce qu'on peut constater :
        Mémoire allouée avant et après l'appel à InitTab :
        Pour le tableau tab (sur la pile), la mémoire est effectivement allouée lors de la déclaration du tableau, et ensuite, lorsque InitTab est appelé, la mémoire est utilisée pour remplir les données dans tab.
        Pour le tableau heapTab (sur le tas), la mémoire est allouée lors de l'appel à malloc, mais les données ne sont réellement allouées qu'une fois que InitTab est appelé. Cependant, le changement de l'utilisation de la mémoire n'est visible qu'après l'appel à InitTab.
    
    En résumé :
        Mémoire allouée sur la pile : Dès la déclaration du tableau (int tab[NMAX];), la mémoire est allouée.
        Mémoire allouée sur le tas : La mémoire est allouée uniquement lorsque malloc est appelé pour le tableau heapTab. Les données sont ensuite remplies lors de l'appel à InitTab.
    Ainsi, l'allocation de mémoire effective pour tab se produit dès sa déclaration (sur la pile), tandis que pour heapTab, elle se produit lors de l'appel à malloc (sur le tas).
    */


    // Tester les fonctions SumTab et MinSumTab
    int min;
    int sum = SumTab(tab, NMAX);
    printf("Sum of elements: %d\n", sum);

    int minSum = MinSumTab(&min, tab, NMAX);
    printf("Sum: %d, Min: %d\n", minSum, min);

    free(heapTab); // Libérer la mémoire allouée

    return 0;
}
