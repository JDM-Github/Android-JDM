#include <stdio.h>
#include <stdlib.h>

struct Node {
    int val;
    struct Node* left;
    struct Node* right;
};

struct Node* new_node(int val) {
    struct Node* node = (struct Node*)malloc(sizeof(struct Node));
    node->val = val;
    node->left = NULL;
    node->right = NULL;
    return node;
}

void insert(struct Node* root, int val) {
    if (!root) {
        root = new_node(val);
        return;
    }
    
    struct Node* temp = root;
    while (temp->left && temp->right) {
        temp = temp->left;
    }
    if (!temp->left) {
        temp->left = new_node(val);
    }
    else {
        temp->right = new_node(val);
    }
}

void print_tree(struct Node* root) {
    if (!root) {
        return;
    }
    
    struct Node* q[100];
    int front = 0;
    int rear = 0;
    
    q[rear++] = root;
    while (front != rear) {
        struct Node* node = q[front++];
        printf("%d\n", node->val);
        if (node->left) {
            q[rear++] = node->left;
        }
        if (node->right) {
            q[rear++] = node->right;
        }
    }
}
