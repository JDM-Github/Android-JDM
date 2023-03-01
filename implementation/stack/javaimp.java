import java.util.EmptyStackException;

class Stack {
  private int[] stack;
  private int top;

  public Stack(int size) {
    this.stack = new int[size];
    this.top = -1;
  }

  public void push(int val) {
    if (top == stack.length - 1) {
      System.out.println("Stack overflow");
      return;
    }
    top++;
    stack[top] = val;
  }

  public int pop() {
    if (top == -1) {
      throw new EmptyStackException();
    }
    int val = stack[top];
    top--;
    return val;
  }

  public int peek() {
    if (top == -1) {
        return 0;
    }
    return stack[top];
  }

  public int is_empty() {
    return stack.length == 0;
  }
}
     
