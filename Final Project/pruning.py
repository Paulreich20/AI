import argparse
import math
import random
import copy

class Node(object):
    def __init__(self, entropy, dataPerOutcome, possible_splits):
        self.category = None
        self.subcategory = None
        self.entropy = entropy
        self.dataPerOutcome = dataPerOutcome.copy()
        self.children = {}
        self.possible_splits = possible_splits
        self.parent = None


    def makeChildren(self, split_category, subcategories, emptyDataPerOutcome):
        children = {}
        newCategories = self.possible_splits.copy()
        newCategories.remove(split_category)
        for sub in subcategories[split_category]:
            new = Node(None, makeEmpty(subcategories), newCategories)
            new.subcategory = sub
            new.category = split_category
            new.parent = self
            children[sub] = new

        for lst in self.dataPerOutcome.values():
            for row in lst:
                if row != {}:
                    children[row[split_category]].dataPerOutcome[row['outcome']] += [row]


        childrenList = []
        for child in children.values():
            childrenList.append(child)
            child.entropy = entropy(child.dataPerOutcome)

        return childrenList

    def childrenEntropy(self, children):
        total_entropy = 0
        denominator = 0
        for outcome in self.dataPerOutcome.values():
            denominator += len(outcome)
        if denominator == 0:
            return 0

        for child in children:
            numerator = 0
            for outcome in child.dataPerOutcome.values(): numerator += len(outcome)
            total_entropy += numerator / denominator * child.entropy
        return total_entropy


def getGain(parent, children):
    childEntropy = parent.childrenEntropy(children)
    return parent.entropy - childEntropy


def entropy(outcomes):
    total = 0
    entropy = 0
    for outcome in outcomes.values():
        total += len(outcome)


    if total == 0:
        return 0
    for outcome in outcomes.values():
        current = len(outcome)
        if current == 0:
            entropy += 0
        else:
            entropy += (current/total)*math.log(total/current, 2)

    return entropy


def getMajority(dic):
    maxK = None
    for k,v in dic.items():
        if maxK is None or len(v) > len(dic[maxK]):
            maxK = k

    return maxK


def split(node, subcategories, emptyDataPerOutcome):
    outcome = None
    counter = 0
    for key in node.dataPerOutcome.keys():
        if not node.dataPerOutcome[key]:
            continue
        elif counter > 0:
            counter += 1
            break
        else:
            outcome = key
            counter += 1
    if counter == 1:
        node.children = outcome
        return
    if counter == 0:
        node.children = getMajority(node.parent.dataPerOutcome)
        return
    elif not node.possible_splits:
        node.children = getMajority(node.dataPerOutcome)
        return

    bestSplit = None
    for category in node.possible_splits:
        possChildren = node.makeChildren(category, subcategories, emptyDataPerOutcome)
        if bestSplit is None or getGain(node, possChildren) > getGain(node, bestSplit):
            bestSplit = possChildren
    node.children = bestSplit

    if node.entropy == node.childrenEntropy(bestSplit):
        majorityOutcome = None
        temp = None
        for k, v in node.dataPerOutcome.items():
            if majorityOutcome is None or len(v) > len(majorityOutcome):
                temp = k
                majorityOutcome = v
        node.children = temp
        return

    for child in node.children:
        split(child, subcategories, emptyDataPerOutcome)


def makeEmpty(subcategories):
    emptyDataPerOutcome = {}
    for val in subcategories["outcome"]:
        emptyDataPerOutcome[val] = []
    return emptyDataPerOutcome

def error(root, testSet):
    numcorrect = 0
    for value in testSet:
        if testTree(root, value):
            numcorrect += 1

    return 1 - numcorrect/len(testSet)

def removalError(originalRoot, prunedRoot, testSet):
    err = (error(prunedRoot, testSet)-error(originalRoot, testSet))/(getLeaves(originalRoot)-getLeaves(prunedRoot))
    return err

#AVOID PRUNING BEFORE DECIDING ON THE OPTIMAL PRUNED TREE
def prune(node):
    node.children = getMajority(node.dataPerOutcome)
    while node.parent is not None:
        node = node.parent
    return node

def getLeaves(root):
    leaves = 0
    for node in getNodes(root):
        if type(node.children) is not list:
            leaves += 1
    return leaves

def getNodes(root):
    if type(root.children) is list:
        lst = []
        for child in root.children:
            lst += getNodes(child)
        lst.append(root)
        return lst
    else:
        return [root]

def pruneTree(root, testSet):
    T = root
    T_i = root
    while type(T_i.children) is list:
        best = None
        for s in getNodes(copy.deepcopy(T_i)):
            if type(s.children) is list:
                if best is None or removalError(T_i, prune(s), testSet) < removalError(T_i, best, testSet):
                    best = prune(copy.deepcopy(s))

        if error(best, testSet) < error(T, testSet):
            T = copy.deepcopy(best)
        T_i = best
    return T


def makeTree(data, categories, subcategories, testSet):
    random.shuffle(data)
    trainSet = data
    rowPerOutcome = {}
    emptyDataPerOutcome = {}
    for val in subcategories["outcome"]:
        rowPerOutcome[val] = []
        emptyDataPerOutcome[val] = []
    for row in trainSet:
        outcome = row["outcome"]
        rowPerOutcome[outcome].append(row)
    root = Node(entropy(rowPerOutcome), rowPerOutcome, categories)
    split(root, subcategories, emptyDataPerOutcome)
    print("Tree size:", len(getNodes(root)))
    return pruneTree(root, testSet)


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset')
    args = parser.parse_args()
    return args.dataset


def load_dataset(file):
    categories = []
    data = []
    with open(file) as f:
        for row in f:
            temp = row.split("\n")
            list = temp[0].split(",")
            if not categories:
                categories = list
                subcategories = {"outcome": []}
                for cat in categories:
                    subcategories[cat] = []
            else:
                dict = {}
                for i in range(len(list)):
                    if i == len(list)-1:
                        dict['outcome'] = list[i]
                        if list[i] not in subcategories["outcome"]:
                            subcategories["outcome"].append(list[i])
                    else:
                        dict[categories[i]] = list[i]
                        if list[i] not in subcategories[categories[i]]:
                            subcategories[categories[i]].append(list[i])
                data.append(dict)
    categories = categories[:-1]
    return [data, categories, subcategories]


def rlen(dic):
    l = 0
    for lst in dic.values():
        l += len(lst)
    return l

def display(node, level, outcomes):
    if node.category is None:
        for child in node.children:
            display(child, level, outcomes)
        return
    else:
        print("| \t"*level, end="")
        statement = node.category + " = " + node.subcategory
        if type(node.children) != type([]):
            print(statement, ": ", node.children)
            return
        print(statement)
        for child in node.children:
            display(child, level +1, outcomes)

def testTree(root, input):
    if type(root.children) is not list:
        return False

    if root.category is None:
        cat = root.children[0].category
        subcat = input[cat]
        for child in root.children:
            if child.subcategory == subcat:
                temp = child

    while type(temp.children) == type([]):
        cat = temp.children[0].category
        for child in temp.children:
            #if still in tree and still correct then we "recurse"
            if child.subcategory == input[cat]:
                temp = child
    if temp.children != input['outcome']:
        return False
    return True

def tenFoldCrossValidation(data):
    accuracyList = []
    print("\n++++++++++++++++++++++++++++++++++++")
    print("Ten-Fold Cross Validation Results")
    print("++++++++++++++++++++++++++++++++++++")
    for j in range(10):
        numCorrect = 0
        trainingSet = []
        testSet = []
        for i in range(len(data[0])):
            if i % 10 == j:
                testSet.append(data[0][i])
            else:
                trainingSet.append(data[0][i])
        print("----- Fold", j+1, "-----")
        root = makeTree(trainingSet, data[1], data[2], testSet)
        print("Pruned tree size:", len(getNodes(root)))
        for valid in testSet:
            if testTree(root, valid) == True:
                numCorrect += 1

        accuracyList.append(numCorrect / len(testSet))
        print("Accuracy:", str(round(100*numCorrect/len(testSet),2)) + "%", "\n")
    print("Average accuracy for ten-fold validation test:", str(round(10*sum(accuracyList))) + "%")

if __name__ == '__main__':
    dataset = parse()
    data = load_dataset(dataset)
    random.shuffle(data[0])
    root = makeTree(data[0][:int(.9*len(data[0]))], data[1], data[2], data[0][int(.9*len(data[0])):])
    print("Pruned tree size:", len(getNodes(root)))
    display(root, 0, data[2]["outcome"])
    tenFoldCrossValidation(data)
