#include <stdio.h>
#include <cs50.h>

int main(void) {
    int n = get_int("Height: ");
    int spaces = n - 1;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < spaces; j++) {
            printf(" ");
        }
        for (int j = spaces; j < n; j++) {
            printf("#");
        }
        spaces--;
        printf("\n");
    }
    return 0;
}