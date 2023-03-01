#include <iostream>
using namespace std;

const int MAX_SIZE = 10;

class Queue {
    private:
        int arr[MAX_SIZE];
        int front;
        int rear;

    public:
        Queue() {
            front = -1;
            rear = -1;
        }

        bool is_empty() {
            return (front == -1 && rear == -1);
        }

        bool is_full() {
            return (rear + 1) % MAX_SIZE == front;
        }

        void enqueue(int val) {
            if (is_full()) {
                cout << "Queue is full." << endl;
                return;
            }
            else if (is_empty()) {
                front = 0;
                rear = 0;
            }
            else {
                rear = (rear + 1) % MAX_SIZE;
            }
            arr[rear] = val;
        }

        void dequeue() {
            if (is_empty()) {
                cout << "Queue is empty." << endl;
                return;
            }
            else if (front == rear) {
                front = -1;
                rear = -1;
            }
            else {
                front = (front + 1) % MAX_SIZE;
            }
        }

        int get_front() {
            if (is_empty()) {
                cout << "Queue is empty." << endl;
                return -1;
            }
            return arr[front];
        }

        int get_rear() {
            if (is_empty()) {
                cout << "Queue is empty." << endl;
                return -1;
            }
            return arr[rear];
        }
};
