Zhang Yuxiang & Lecomte Antoine

TME 2

Question 1.1 :
exécution de time sleep 5 :
sleep 5 0.00s user 0.00s system 0% cpu 5.016 total
On constate que le temps CPU passé en mode kernel et en mode user sont approximativement de 0.00s ce qui s'explique car sleep ne fait aucun calcul, donc aucune charge pour le CPU user. Pour le CPU en mode kernel, sleep suspend le processus donc le noyau n'a de même presque rien à faire. 0% cpu indique que le processus sleep n'occupe pas le processeur, il ne fait qu'attendre passivement. Il y a 16 millisecondes de latence sur la machine utilisée au moment du lancement de la commande.


Question 1.2 :
volatile est utilisé pour éviter l'optimisation par le compilateur, qui supprime la boucle si elle ne fait rien d'utile. Avec Unsigned Long Long, la valeur de max_iter est bien interprétée comme un entier de 64 bits.
Au lancement du programme, on a : ./loopcpu 6.91s user 0.01s system 96% cpu 7.152 total.
Donc le cpu est bien en mode user pour l'exécution du programme. La gestion du processus effectuée par l'OS en arrière-plan peut expliquer le temps très faible d'environ 0.01s du temps CPU passé en mode kernel. Le programme sollicite énormément le cpu durant l'exécution du programme car il a utilisé 96% des ressources du CPU. Donc le programme a utilisé 6.91 secondes de CPU pour 96% de l'usage du processeur mais l'OS a pris légèrement plus de temps pour gérer le processus correspondant aux 0.242 secondes supplémentaires et gérer d'autres tâches du système simultanément.


Question 1.3 :
On ne fait rien avec pid pour que l'appel système soit la tâche principale.
Au lancement du programme, on a : ./loopsys 0.14s user 0.01s system 38% cpu 0.398 total.
Cela indique que 0.14 secondes de temps CPU ont été utilisées pour exécuter getpid() à chaque intération. Le CPU passe alors en mode kernel mais n'a pas de tâche à effectuer donc revient immédiatement en mode user pour continuer les itérations de la boucle. Le temps total prend en compte d'autres tâches de l'OS, c'est pourquoi il est plus élevé que le temps CPU (kernel + user) lié à l'exécution du programme.


