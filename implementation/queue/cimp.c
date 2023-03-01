#include <stdio.h>
#include <stdlib.h>

#define MAX_SIZE 10

struct queue {
    int arr[MAX_SIZE];
    int front;
    int rear;
};

void init(struct queue *q) {
    q->front = -1;
    q->rear = -1;
}

int is_empty(struct queue *q) {
    return (q->front == -1 && q->rear == -1);
}

int is_full(struct queue *q) {
    return (q->rear + 1) % MAX_SIZE == q->front;
}

void enqueue(struct queue *q, int val) {
    if (is_full(q)) {
        printf("Queue is full.\n");
        return;
    }
    else if (is_empty(q)) {
        q->front = 0;
        q->rear = 0;
    }
    else {
        q->rear = (q->rear + 1) % MAX_SIZE;
    }
    q->arr[q->rear] = val;
}

void dequeue(struct queue *q) {
    if (is_empty(q)) {
        printf("Queue is empty.\n");
        return;
    }
    else if (q->front == q->rear) {
        q->front = -1;
        q->rear = -1;
    }
    else {
        q->front = (q->front + 1) % MAX_SIZE;
    }
}

int front(struct queue *q) {
    if (is_empty(q)) {
        printf("Queue is empty.\n");
        return -1;
    }
    return q->arr[q->front];
}

int rear(struct queue *q) {
    if (is_empty(q)) {
        printf("Queue is empty.\n");
        return -1;
    }
    return q->arr[q->rear];
}
