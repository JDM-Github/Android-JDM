import java.util.LinkedList;
import java.util.Queue;

class Node {
    int val;
    Node left;
    Node right;
    
    Node(int val) {
        this.val = val;
        left = null;
        right = null;
    }
}

class BinaryTree {
    Node root;
    
    BinaryTree() {
        root = null;
    }
    
    void insert(int val) {
        if (root == null) {
            root = new Node(val);
            return;
        }
        
        Queue<Node> q = new LinkedList<>();
        q.add(root);
        while (!q.isEmpty()) {
            Node node = q.poll();
            if (node.left == null) {
                node.left = new Node(val);
                return;
            }
            else if (node.right == null) {
                node.right = new Node(val);
                return;
            }
            else {
                q.add(node.left);
                q.add(node.right);
            }
        }
    }
    
    void printTree() {
        if (root == null) {
            return;
        }
        
        Queue<Node> q = new LinkedList<>();
        q.add(root);
        while (!q.isEmpty()) {
            Node node = q.poll();
            System.out.println(node.val);
            if (node.left != null) {
                q.add(node.left);
            }
            if (node.right != null) {
                q.add(node.right);
            }
        }
    }
}
