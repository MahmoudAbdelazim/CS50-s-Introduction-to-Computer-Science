// Implements a dictionary's functionality

#include <stdbool.h>
#include <string.h>
#include <strings.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 1e5 + 1;

// Hash table
node *table[N];

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    char wordd[LENGTH + 1];
    strcpy(wordd, word);
    for (int i = 0; wordd[i] != '\0'; i++) {
        if (isalpha(wordd[i])) {
            wordd[i] = tolower(wordd[i]);
        }
    }
    unsigned int code = hash(wordd);
    bool found = false;
    node *cur = table[code];
    while (cur != NULL)  {
        if (strcasecmp(cur->word, wordd) == 0) {
            found = true;
            break;
        }
        cur = cur->next;
    }
    return found;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    unsigned int hash = 5381;
    int c;

    while ((c = (*word++)))
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */

    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // TODO
    FILE *file = fopen(dictionary, "r");
    if (!file) {
        return false;
    }
    for (int i = 0; i < N; i++) {
        table[i] = NULL;
    }
    char word[LENGTH + 1];
    while (fscanf(file, "%s", word) != EOF) {
        unsigned int code = hash(word);
        if (table[code] == NULL) {
            table[code] = malloc(sizeof(node));
            strcpy(table[code]->word, word);
            table[code]->next = NULL;
        } else {
            node *nw = malloc(sizeof(node));
            strcpy(nw->word, word);
            nw->next = table[code]->next;
            table[code]->next = nw;
        }
    }
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    int num = 0;
    node *cur;
    for (int i = 0; i < N; i++) {
        cur = table[i];
        while (cur != NULL) {
            num++;
            cur = cur->next;
        }
    }
    return num;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    node *cur;
    node *tmp;
    for (int i = 0; i < N; i++) {
        cur = table[i];
        while (cur != NULL) {
            tmp = cur->next;
            free(cur);
            cur = tmp;
        }
    }
    return true;
}
