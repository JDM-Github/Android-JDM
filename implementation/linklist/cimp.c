#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int data;
    struct Node *next;
} Node;

void insert(Node **head, int data) {
    Node *new_node = malloc(sizeof(Node));
    new_node->data = data;
    new_node->next = *head;
    *head = new_node;
}

void print_list(Node *head) {
    while (head != NULL) {
        printf("%d\n", head->data);
        head = head->next;
    }
}
