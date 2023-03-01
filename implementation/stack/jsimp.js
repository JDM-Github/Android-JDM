class Stack {
    constructor() {
      this.stack = [];
    }
  
    push(val) {
      this.stack.push(val);
    }
  
    pop() {
      if (this.is_empty()) {
        return null;
      }
      return this.stack.pop();
    }
  
    peek() {
      if (this.is_empty()) {
        return null;
      }
      return this.stack[this.stack.length - 1];
    }
  
    is_empty() {
      return this.stack.length == 0;
    }
  }
  