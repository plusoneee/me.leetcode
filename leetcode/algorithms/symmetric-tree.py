# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        if not root:
            return True

        return self.isSym(root.left, root.right)

    def isSym(self, l: TreeNode, r: TreeNode) -> bool:
        if not l and not r:
            return True
        if not l or not r:
            return False
        if l.val != r.val:
            return False

        return self.isSym(l.left, r.right) and self.isSym(l.right, r.left)
