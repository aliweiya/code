import java.util.*;

class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;
    TreeNode() {}
    TreeNode(int val) { this.val = val; }
    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }
}
class Solution {
    public static TreeNode build(List<Integer> nodes) {
        if (nodes.size() == 0)
            return null;

        TreeNode root = new TreeNode(nodes.get(0));
        Queue<TreeNode> queue = new LinkedList<>();
        queue.add(root);

        for (int i=1; i<nodes.size(); i+=2) {
            int size = queue.size();
            TreeNode node = queue.poll();
            if (nodes.get(i) != null) {
                node.left = new TreeNode(nodes.get(i));
                queue.add(node.left);
            }

            if (i+1 < nodes.size() && nodes.get(i+1) != null) {
                node.right = new TreeNode(nodes.get(i+1));
                queue.add(node.right);
            }
        }
        return root;
    }

    public static void levelOrder(TreeNode root) {
        Queue<TreeNode> queue = new LinkedList<>();
        queue.add(root);

        while (queue.size() > 0) {
            int size = queue.size();

            for (int i=0; i < size; i++) {
                TreeNode node = queue.poll();

                if (node != null) {
                    System.out.println(node.val);

                    queue.add(node.left);
                    queue.add(node.right);
                }
                else {
                    System.out.println("null");
                }
            }
        }
    }

    public static void main(String[] args) {
        List<Integer> list = new ArrayList<>(Arrays.asList(3,1,4,null,null,2));
        TreeNode root = Solution.build(list);

        Solution.levelOrder(root);
    }
}