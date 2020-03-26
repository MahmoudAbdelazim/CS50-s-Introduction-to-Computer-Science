#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <cs50.h>

int main(void) {
    string s = get_string("Text: ");
    int letters = 0;
    int words = 1;
    int sentences = 0;
    bool x = false;
    for (int i = 0, n = strlen(s); i < n; i++) {
        if (s[i] == ' ') {
            words++;
        }
        else if (s[i] == '.' || s[i] == '?' || s[i] == '!') {
            sentences++;
        }
        else if (isalpha(s[i])) {
            letters++;
        }
    }
    if (s[strlen(s) - 1] == ' ')
        words -= 1;
    double L = ((double)letters / words) * 100;
    double S = ((double)sentences / words) * 100;
    int index = round(0.0588 * L - 0.296 * S - 15.8);
    if (index > 16)
        printf("Grade 16+\n");
    else if (index == 0)
        printf("Before Grade 1\n");
    else
        printf("Grade %i\n", index);
}






