class Node {
  constructor(val) {
      this.val = val;
      this.left = null;
      this.right = null;
  }
}

class BinaryTree {
  constructor() {
      this.root = null;
  }
  
  insert(val) {
      if (!this.root) {
          this.root = new Node(val);
          return;
      }
      
      const q = [this.root];
      while (q.length) {
          const node = q.shift();
          if (!node.left) {
              node.left = new Node(val);
              return;
          }
          else if (!node.right) {
              node.right = new Node(val);
              return;
          }
          else {
              q.push(node.left);
              q.push(node.right);
          }
      }
  }
  
  printTree() {
      if (!this.root) {
          return;
      }
      
      const q = [this.root];
      while (q.length) {
          const node = q.shift();
          console.log(node.val);
          if (node.left) {
              q.push(node.left);
          }
          if (node.right) {
              q.push(node.right);
          }
      }
  }
}
