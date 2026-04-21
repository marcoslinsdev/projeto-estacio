#include <stdio.h>
struct Territorio {
    char nome[30];
    int tropas;


};
int main() {
    struct Territorio t1;
    printf("Nome do territorio: ");
    scanf("%s",  t1.nome);

    
    printf("Numero de tropas: ");
    scanf("%d", &t1.tropas);

    printf("\nTerritorio: %s\n",  t1.nome);
    printf("Tropas: %d n", t1.tropas);

    return 0;
}