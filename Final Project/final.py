import argparse
import math

class Node(object):
    def __init__(self, entropy, dataPerOutcome, possible_splits):
        self.category = None
        self.subcategory = None
        self.entropy = entropy
        self.dataPerOutcome = dataPerOutcome
        self.children = {}
        self.possible_splits = possible_splits

    def makeChildren(self, split_category, subcategories):
        children = {}
        newCategories = self.possible_splits.copy()
        newCategories.remove(split_category)
        for sub in subcategories[split_category]:
            new = Node(None, {}, newCategories)
            new.subcategory = sub
            new.category = split_category
            children[sub] = new

        for key in self.dataPerOutcome.keys():
            for row in self.dataPerOutcome[key]:
                child =
                children[row[split_category]].dataPerOutcome[key].append(row)

        childrenList = []
        for child in children.values():
            childrenList.append(child)
            child.entropy = entropy(child.dataPerOutcome)

        return childrenList

    def childrenEntropy(self, children):
        total_entropy = 0
        denominator = 0
        for outcome in self.dataPerOutcome.values(): denominator += len(outcome)
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

    for outcome in outcomes:
        total += len(outcome)

    for outcome in outcomes:
        current = len(outcome)
        entropy += (current/total)*math.log(total/current, 2)

    return entropy

def split(node, subcategories):
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


    bestSplit = None
    for category in node.possible_splits:
        possChildren = node.makeChildren(category, subcategories)
        if bestSplit is None or getGain(node, possChildren) > getGain(node, bestSplit):
            bestSplit = possChildren
    node.children = bestSplit

    for child in node.children:
        split(child, subcategories)


def makeTree(data, categories, subcategories):
    rowPerOutcome = {}
    for val in subcategories["outcome"]:
        rowPerOutcome[val] = []
    for row in data:
        outcome = row["outcome"]
        rowPerOutcome[outcome].append(row)
    root = Node(entropy(rowPerOutcome), rowPerOutcome, categories)
    split(root, subcategories)
    return root
    #split(root,categories)

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

def display(node, level, outcomes):
    if node.category is None:
        for child in node.children:
            display(child, level)
        return
    else:
        print("| \t"*level, end="")
        statement = node.category + " = " + node.subcategory
        if type(node.children) != type([]):
            print(statement, ": ", node.children)
            return
        print(statement)
        for child in node.children:
            display(child, level +1)


if __name__ == '__main__':
    dataset = parse()
    data = load_dataset(dataset)
    root = makeTree(data[0], data[1], data[2])
    display(root, 0, data[2]["outcome"])
    #root = makeTree(data[0], data[1], data[2])
    #display(root, 0)
