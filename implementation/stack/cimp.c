#include <stdio.h>
#define MAX_SIZE 100

typedef struct {
    int stack[MAX_SIZE];
    int top;
} Stack;

void init(Stack *s) {
    s->top = -1;
}

void push(Stack *s, int val) {
    if (s->top == MAX_SIZE - 1) {
        printf("Stack overflow\n");
        return;
    }
    s->top++;
    s->stack[s->top] = val;
}

int pop(Stack *s) {
    if (s->top == -1) {
        printf("Stack underflow\n");
        return -1;
    }
    int val = s->stack[s->top];
    s->top--;
    return val;
}

int peek(Stack *s) {
    if (s->top == -1) {
        printf("Stack underflow\n");
        return -1;
    }
    return s->stack[s->top];
}

int is_empty(Stack *s) {
    return s->top == -1;
}
