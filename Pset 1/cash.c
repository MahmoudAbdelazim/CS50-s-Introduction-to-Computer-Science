#include <stdio.h>
#include <cs50.h>

int main(void) {
    float m = get_float("Change owed: ");
    if (m < 0) {
        printf("foo\n");
        return 1;
    }
    while (m < 0)
        m = get_float("Change owed: ");
    int coins = 0;
    int money = m * 100;
    while (money >= 25) {
        money -= 25;
        coins += 1;
    }
    while (money >= 10){
        money -= 10;
        coins += 1;
    }
    while (money >= 5) {
        money -= 5;
        coins += 1;
    }
    while (money >= 1){
        money -= 1;
        coins += 1;
    }
    printf("%i\n",coins);
}