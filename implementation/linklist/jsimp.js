class ListNode {
    constructor(val) {
          this.val = val;
        this.next = null;
        }
    }
  
    class LinkedList {
        constructor() {
        this.head = null;
        this.size = 0;
    }
  
    add(val) {
        let newNode = new ListNode(val);
        if (!this.head) {
            this.head = newNode;
        } else {
            let curr = this.head;
            while (curr.next) {
                curr = curr.next;
            }
            curr.next = newNode;
        }
        this.size++;
    }

    print() {
        let curr = this.head;
        while (curr) {
            console.log(curr.val);
            curr = curr.next;
        }
    }
}