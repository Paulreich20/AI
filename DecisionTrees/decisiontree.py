import argparse
import math

class Node(object):
    def __init__(self, entropy, data_yes, data_no, possible_splits):
        self.category = None #Need name to print later
        self.subcategory = None
        self.entropy = entropy
        self.dataY = data_yes
        self.dataN = data_no
        self.children = {}
        self.possible_splits = possible_splits

    def makeChildren(self, split_category, subcategories):
        children = {}
        newCategories = self.possible_splits.copy()
        newCategories.remove(split_category)
        for sub in subcategories[split_category]:
            new = Node(None, [], [], newCategories)
            new.subcategory = sub
            new.category = split_category
            children[sub] = new

        for row in self.dataY:
            children[row[split_category]].dataY.append(row)

        for row in self.dataN:
            children[row[split_category]].dataN.append(row)
        childrenList = []
        for child in children.values():
            childrenList.append(child)
            child.entropy = entropy(len(child.dataY), len(child.dataN))

        return childrenList

    def childrenEntropy(self, children):
        total_entropy = 0
        numerator = len(self.dataY) + len(self.dataN)
        for child in children:
            total_entropy += (len(child.dataY) + len(child.dataN)) / numerator * child.entropy
        return total_entropy


def getGain(parent, children):
    childEntropy = parent.childrenEntropy(children)
    return parent.entropy - childEntropy


def entropy(y, n):
    if y == 0 or n == 0:
        return 0
    t = y+n
    ent = (y/t)*math.log(t/y, 2) + (n/t)*math.log(t/n, 2)
    return ent


def split(node, subcategories):
    # Base cases are if either unanimous yes/no or if you've run out of categories to split
    if (not node.dataN) and (not node.dataY):
        node.children = 0
        return
    elif not node.dataN:
        node.children = 1
        return
    elif not node.dataY:
        node.children = 0
        return
    #If we've reached a leaf and we still are not unanimious we default to majority decision. So for the titanic example,
    # if there are two second class male children that survived and 1 second class male child that died the decision
    # tree gives an output of surviving.
    elif len(node.possible_splits) == 0:
        if len(node.dataY) > len(node.dataN):
            node.children = 1
        else:
            node.children = 0
        return

    # Otherwise iterate through categories and create children based on splitting by that category.
    # Save the children with the lowest current gain relative to the node.
    bestSplit = None
    for category in node.possible_splits:
        possChildren = node.makeChildren(category, subcategories)
        if node.entropy == node.childrenEntropy(possChildren):
            if len(node.dataY) > len(node.dataN):
                bestSplit = 1
            else:
                bestSplit = 0
            node.children = bestSplit
            return
        elif bestSplit is None or getGain(node, possChildren) > getGain(node, bestSplit):
            bestSplit = possChildren
    node.children = bestSplit

    # Split the node by best category, recursively split the children using DFS.
    for child in node.children:
        split(child, subcategories)


def makeTree(data, categories, subcategories):
    dataY = []
    dataN = []
    for row in data:
        if row["outcome"] == "yes":
            dataY.append(row)
        else:
            dataN.append(row)
    root = Node(entropy(len(dataY), len(dataN)), dataY, dataN, categories)
    split(root, subcategories)
    return root


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset')

    args= parser.parse_args()
    return args.dataset

def load_dataset(file):
    categories = []
    data = []
    with open(file) as f:
        for row in f:
            temp = row.split("\n")
            list = temp[0].split("\t")
            if not categories:
                categories = list
                subcategories = {}
                for cat in categories:
                    subcategories[cat] = []
            else:
                dict = {}
                for i in range(len(list)):
                    if i == len(list)-1:
                        dict['outcome'] = list[i]
                    else:
                        dict[categories[i]] = list[i]
                        if list[i] not in subcategories[categories[i]]:
                            subcategories[categories[i]].append(list[i])
                data.append(dict)
    categories = categories[:-1]
    return [data, categories, subcategories]


def display(node, level):
    #Note that if we reach a leaf whose specific combination of subcategories don't appear within the data we default to no
    # as it was not clear what we do with this edge case.
    if node.category is None:
        for child in node.children:
            display(child, level)
        return
    else:
        print("| \t"*level, end="")
        statement = node.category + " = " + node.subcategory
        if node.children == 1:
            statement += ": Yes"
            print(statement)
            return
        elif node.children == 0:
            statement += ": No"
            print(statement)
            return
        print(statement)
        for child in node.children:
            display(child, level +1)

if __name__ == '__main__':
    dataset = parse()
    data = load_dataset(dataset)
    root = makeTree(data[0], data[1], data[2])
    display(root, 0)
