public class Queue {
    private int[] arr;
    private int front;
    private int rear;

    public Queue(int size) {
        arr = new int[size];
        front = -1;
        rear = -1;
    }

    public boolean is_empty() {
        return front == -1 && rear == -1;
    }

    public boolean is_full() {
        return rear == arr.length - 1;
    }

    public void enqueue(int val) {
        if (is_full()) {
            System.out.println("Queue is full.");
            return;
        }
        else if (is_empty()) {
            front = 0;
            rear = 0;
        }
        else {
            rear++;
        }
        arr[rear] = val;
    }

    public void dequeue() {
        if (is_empty()) {
            System.out.println("Queue is empty.");
            return;
        }
        else if (front == rear) {
            front = -1;
            rear = -1;
        }
        else {
            front++;
        }
    }

    public int get_front() {
        if (is_empty()) {
            System.out.println("Queue is empty.");
            return -1;
        }
        return arr[front];
    }

    public int get_rear() {
        if (is_empty()) {
            System.out.println("Queue is empty.");
            return -1;
        }
        return arr[rear];
    }
}
