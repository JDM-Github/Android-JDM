class ListNode {
    int val;
    ListNode next;

    ListNode(int val) {
        this.val = val;
        this.next = null;
    }
}

class LinkedList {
    ListNode head;
    int size;

    LinkedList() {
        this.head = null;
        this.size = 0;
    }

    void add(int val) {
        ListNode newNode = new ListNode(val);
        if (this.head == null) {
            this.head = newNode;
        } else {
            ListNode curr = this.head;
            while (curr.next != null) {
                curr = curr.next;
            }
            curr.next = newNode;
        }
        this.size++;
    }

    void print() {
        ListNode curr = this.head;
        while (curr != null) {
            System.out.println(curr.val);
            curr = curr.next;
        }
    }
}