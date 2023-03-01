class Queue {
  constructor() {
      this.items = [];
  }

  enqueue(item) {
      this.items.push(item);
  }

  dequeue() {
      if (!this.is_empty()) {
          return this.items.shift();
      }
  }

  is_empty() {
      return this.items.length === 0;
  }

  size() {
      return this.items.length;
  }

  front() {
      if (!this.is_empty()) {
          return this.items[0];
      }
  }

  rear() {
      if (!this.is_empty()) {
          return this.items[this.items.length - 1];
      }
  }
}
