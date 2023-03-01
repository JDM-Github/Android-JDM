#include <iostream>
#include <queue>
using namespace std;

struct Node {
    int val;
    Node* left;
    Node* right;
};

Node* new_node(int val) {
    Node* node = new Node();
    node->val = val;
    node->left = NULL;
    node->right = NULL;
    return node;
}

void insert(Node* root, int val) {
    if (!root) {
        root = new_node(val);
        return;
    }
    
    queue<Node*> q;
    q.push(root);
    while (!q.empty()) {
        Node* node = q.front();
        q.pop();
        if (!node->left) {
            node->left = new_node(val);
            return;
        }
        else if (!node->right) {
            node->right = new_node(val);
            return;
        }
        else {
            q.push(node->left);
            q.push(node->right);
        }
    }
}

void print_tree(Node* root) {
    if (!root) {
        return;
    }
    
    queue<Node*> q;
    q.push(root);
    while (!q.empty()) {
        Node* node = q.front();
        q.pop();
        cout << node->val << endl;
        if (node->left) {
            q.push(node->left);
        }
        if (node->right) {
            q.push(node->right);
        }
    }
}
