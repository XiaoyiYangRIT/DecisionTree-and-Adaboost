from Models import features as fe
import math
   
def learn(leaf, attrs = fe.features, root = "root"):
    """
    The Decision Tree Learning function
    :param leaf: The data of the current leaf on the tree
    :param attrs: The features will be used in leaning
    :param root: The parent of the leaf
    :return: The partial or whole decision tree represented by dictionary
    """
    if sameClassification(leaf):
        # if all items belong to the same class
        subtree = {}
        subtree[root] = leaf[0][-1]
        return subtree
    elif not attrs:
        # if no attribute left, means the learning on this branch is ending
        # the result may be mixed
        pos = countPositive(leaf)
        neg = len(leaf) - pos
        if(pos > neg):
            re = pos
        else:
            re = neg
        subtree = {}
        subtree[root] = re
        return subtree
    else:
        # Otherwise, continue the learning process
        tree = {}
        
        # get the decision and entropy by fomular
        decision, entropy = importance(attrs, leaf)
        tree[root] = str(decision)
        
        # Expand according to the optimal decision
        branches = classifier(leaf, decision)
        
        # Prepare leaves for expansion
        newAttrs = attrs.copy()
        newAttrs.remove(decision)
        
        # Save into the tree
        tree[root + ";" + str(decision)] = []
        
        # Move toward the next round learning
        for key in branches:
            tree[root + ";" + str(decision)].append(str(decision) + key)
            tree.update(learn(branches[key], newAttrs, root + ";" + str(decision) + key))
        
        return tree

def predict(example, hypo, root = "root"):
    """
    The recursive Decision Tree predict function, 
    print out the outcome
    :param example: One text data to be predicted
    :param hypo: The features used to predict
    :param root: The parent of the leaf
    """
    val = hypo[root]
    if(val == fe.positive):
        print(fe.positive)
    elif(val == fe.negative):
        print(fe.negative)
    else:
        decision = int(hypo[root])
        if example[decision]:
            predict(example, hypo, root + ";" + val + "True")
        else:
            predict(example, hypo, root + ";" + val + "False")
            
def classifier(examples, index):
    """
    To classify text datas with decision stump
    :param examples: The text datas from the leaf on decision tree
    :param index: indicate which decision stump to use
    :return: a dictionary with the classified data
    """
    A = []
    B = []
    for example in examples:
        if example[index] == True:
            A.append(example)
        else:
            B.append(example)
    result = {}
    if A:
        result["True"] = A
    if B:
        result["False"] = B
    return result
   
def sameClassification(data):
    """
    Check if all datas from the leaf positive or negative
    :param data: The text datas from the leaf on decision tree
    :return: a boolean value 
    """
    # Unsure about which class it is, get the first one and compare with all the rest
    marker = data[0][-1]
    for d in data:
        if d[-1] != marker:
            return False
    return True
        
def importance(attrs, datas):
    """
    Function to find the feature with highest entropy
    :param attrs: All available features
    :param datas: All datas
    :return: the feature with highest entropy
    """
    # List of all entropies
    gains = {}
    
    for x in attrs:
        dic = classifier(datas, x)
        gains[x] = gain(dic, len(datas))
        
    return myMax(gains)

def gain(dic, totalSize):
    """
    Part of formula to calculate entropy
    :param dic: The classified data by desicion stump
    :param totalSize: The size of all datas
    :return: a required value in formula
    """
    sum = 0
    for key in dic:
        val = dic[key]
        size = len(val)
        sum = sum + size / totalSize * getEntropy(countPositive(val) / size)
    return 1 - sum
           
def getEntropy(q):
    """
    Part of formula to calculate entropy
    :param q: part of the formula
    :return: the entropy
    """
    if (q == 0 or q == 1):
        return 0
    else:
        return (-1) * (q * math.log2(q) + (1 - q) * math.log2(1 - q))

def countPositive(leaf):
    """
    Function to count the number of positive data
    :param leaf: All datas
    :return: the number of positive data
    """
    count = 0;
    for item in leaf:
        if item[-1] == fe.positive:
            count = count + 1
    return count

def myMax(dic):
    """
    Function to found the maximum emtropy and corresponding decision stump
    :param dic: All datas
    :return: the maximum emtropy and corresponding decision stump
    """
    maxi = list(dic.values())[0]
    maxk = list(dic.keys())[0]
    for key in dic:
        if dic[key] >= maxi:
            maxi = dic[key]
            maxk = key
    return maxk, maxi