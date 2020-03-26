#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cs50.h>

int main(int argc, char *argv[])
{
    if (argc != 2) {
        printf("Only one argument allowed\n");
        return 1;
    }
    FILE* file = fopen(argv[1], "r");
    if (file == NULL) {
        printf("Couldn't open file\n");
        return 1;
    }

    int cnt = 0;
    FILE* output = NULL;

    unsigned char *block = malloc(512);
    bool jpeg = false;

    while (fread(block, 1, 512, file)) {
        jpeg = false;
        if (block[0] == 0xff && block[1] == 0xd8 && block[2] == 0xff) {
            if (block[3] >= 0xe0 && block[3] <= 0xef) {
                if (output != NULL) {
                    fclose(output);
                }
                char outname[8];
                sprintf(outname, "%03d.jpg", cnt);
                output = fopen(outname, "a");
                cnt++;
                jpeg = true;
            }
        }
        if (output != NULL) {
            fwrite(block, 1, 512, output);
        }

    }
    if (output != NULL)
        fclose(output);
    if (file != NULL)
        fclose(file);
    free(block);
    return 0;
}
