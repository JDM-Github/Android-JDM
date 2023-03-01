#include <iostream>

using namespace std;

class Node {
public:
    int data;
    Node *next;

    Node(int data) {
        this->data = data;
        this->next = nullptr;
    }
};

class LinkedList {
public:
    Node *head;

    LinkedList() {
        this->head = nullptr;
    }

    void insert(int data) {
        Node *new_node = new Node(data);
        new_node->next = head;
        head = new_node;
    }

    void print_list() {
        Node *curr = head;
        while (curr != nullptr) {
            cout << curr->data << endl;
            curr = curr->next;
        }
    }
};
