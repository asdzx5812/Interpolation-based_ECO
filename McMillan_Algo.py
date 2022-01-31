import re
class Node:
    def __init__(self, val="", left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def findLeaf(root, leaf):
    if root:
        if not root.left and not root.right:
            leaf.append(root)
        else:
            findLeaf(root.left, leaf)
            findLeaf(root.right, leaf)

def doOr(a, b):
    if a == "False":
        return b
    elif b == "False":
        return a
    else:
        return "(" + a + "|" + b + ")" 


def doAnd(a, b):
    if a == "False" or b == "False":
        return "False"
    elif a == "True":
        return b
    elif b == "True":
        return a
    else:
        return a + b

def itp(node, leaf, A, B):
    if node in leaf:
        if node.val in A:
            return extractGlobalLiteral(node, A, B)
        return "True"
    else:
        c1, c2 = node.left, node.right
        if c1.val in A:
            #print(itp(c1, leaf, A, B))
            return doOr(itp(c1, leaf, A, B), itp(c2, leaf, A, B))
        return doAnd(itp(c1, leaf, A, B), itp(c2, leaf, A, B))

def extractGlobalLiteral(node, A, B):
    s = set([i for i in re.split("!|\||\(|\)", node.val) if len(i) > 0])
    A = "".join(A)
    B = "".join(B)
    A = set([i for i in re.split("!|\||\(|\)", A) if len(i) > 0])
    B = set([i for i in re.split("!|\||\(|\)", B) if len(i) > 0])
    globalLiteral = A & B
    res = "False"
    for literal in s:
        if literal in globalLiteral:
            res = doOr(res, literal)
    
    return res
def initGraph():
    root = Node("()")
    cur = root
    cur.left = Node("(r)")
    cur.right = Node("(!r)")
    cur = cur.left
    cur.left = Node("(q)")
    cur.right = Node("(!q|r)")
    cur = cur.left
    cur.left = Node("(p)")
    cur.right = Node("(!p|q)")
    A = ["(p)", "(!p|q)"]
    B = ("(!q|r)","(!r)")
    return root, A, B

def preOrderTraverse(root):
    if root:
        print(root.val)
        preOrderTraverse(root.left)
        preOrderTraverse(root.right)

if __name__ == "__main__":

    root, A, B = initGraph()    
    
    leaf = []
    findLeaf(root, leaf)
    preOrderTraverse(root)
    
    print("A : " + "".join(A))
    print("B : " + "".join(B))
    print("interpolation : " + itp(root, leaf, A, B))