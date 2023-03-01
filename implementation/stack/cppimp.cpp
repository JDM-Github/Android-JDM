#include <iostream>

using namespace std;

#define MAX_SIZE 100

class Stack {
private:
    int stack[MAX_SIZE];
    int top;

public:
    Stack() {
        top = -1;
    }

    void push(int val) {
        if (top == MAX_SIZE - 1) {
            cout << "Stack overflow" << endl;
            return;
        }
        top++;
        stack[top] = val;
    }

    int pop() {
        if (top == -1) {
            cout << "Stack underflow" << endl;
            return -1;
        }
        int val = stack[top];
        top--;
        return val;
    }

    int peek() {
        if (top == -1) {
            cout << "Stack underflow" << endl;
            return -1;
        }
        return stack[top];
    }

    bool is_empty() {
        return top == -1;
    }
};
