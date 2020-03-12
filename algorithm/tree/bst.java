class Node {
    public int val;
    public Node left, right, prev;
    public Node(int val) {
        this.val = val;
        left = null;
        right = null;
        prev = null;
    }
}

class BST {
    private Node root;

    public BST() {
        root = null;
    }

    public Node find(int val) {
        Node current = root;
        while (current != null) {
            if (current.val == val)
                return current;
            else if (current.val < val) {
                current = current.right;
            }
            else {
                current = current.left;
            }
        }
        return null;
    }

    public void insert (int val) {
        if (root == null) {
            root = new Node(val);
            return;
        }

        Node current = root, parent = root;
        while (current != null) {
            parent = current;
            if (current.val < val) {
                current = current.right;
            }
            else {
                current = current.left;
            }
        }

        Node node = new Node(val);
        if (parent.val < val) {
            parent.right = node;
        }
        else {
            parent.left = node;
        }
        node.prev = parent;
    }

    /**
     * 用一棵以v为根的子树来替换一棵以u为根的子树
     * 该方法不更新 v.left和v.right
     */
    private void transplant(Node u, Node v) {
        if (u.prev == null)
            root = v;
        else if (u == u.prev.left)
            u.prev.left = v;
        else
            u.prev.right = v;

        if (v != null)
            v.prev = u.prev;
    }

    /**
     * 删除节点，分以下几种情况
     * 1. 若z没有左孩子，则使用z的右孩子替换z，右孩子可以为null，也可以不是
     * 2. 若z仅有右孩子，那么用左孩子节点替换z
     * 3. z既有左孩子又有右孩子，则查找z的后继y（y一定在右子树，且没有左孩子）
     *   3.1 如果y是z的右孩子，则使用y替换z
     *   3.2 如果y不是z的右孩子，则使用y的右孩子替换y，然后用y替换z
     */
    public void delete(int val) {
        Node node = find(val);
        if (node == null)
            return;

        if (node.left == null)
            transplant(node, node.right);
        else if (node.right == null)
            transplant(node, node.left);
        else {
            Node y = minimum(node.right);
            if (y.prev != node) {
                transplant(y, y.right);
                y.right = node.right;
                y.right.prev = y;
            }
            transplant(node, y);
            y.left = node.left;
            y.left.prev = y;
        }
    }

    public Node minimum(Node current) {
        if (current == null)
            current = root;

        while (current.left != null)
            current = current.left;

        return current;
    }

    public Node minimum() {
        return minimum(null);
    }

    public Node maximum(Node current) {
        if (current == null)
            current = root;

        while (current.right != null)
            current = current.right;

        return current;
    }

    public Node maximum() {
        return maximum(null);
    }

    /**
     * 后继节点是大于该节点的最小关键字节点
     */
    public Node successor(Node node) {
        if (node.right != null)
            return minimum(node.right);

        Node prev = node.prev;
        // 若当前节点是父节点的右孩子，则需要往上找
        while (prev != null && node == prev.right) {
            node = prev;
            prev = prev.prev;
        }
        // 直到当前节点是父节点的左孩子，那么父节点就是后继节点
        return prev;
    }

    /**
     * 前驱节点
     *   1. 如果左孩子不为空，则前驱节点为左子树中最大节点
     *   2. 如果当前节点是左孩子节点，则一直遍历到当前子树是父节点的右子树
     *   3. 如果当前节点是右孩子节点，则父节点就是其前驱节点
     */
    public Node predecessor(Node node) {
        if (node.left != null)
            return maximum(node);

        Node prev = node.prev;
        while (prev != null && node == prev.left) {
            node = prev;
            prev = prev.prev;
        }
        return prev;
    }
}

public class Solution {
    public static void main(String[] args) {
        BST bst = new BST();
        int[] arr = {5, 4, 2, 3, 9, 7, 6, 8, 10};
        for (int i: arr) {
            bst.insert(i);
        }
        Node node = bst.find(8);
        System.out.println(bst.predecessor(node).val);
        System.out.println(bst.maximum().val);
        System.out.println(bst.minimum().val);

        node = bst.find(5);
        System.out.println(bst.successor(node).val);

        bst.delete(7);

    }
}