import argparse
import math

class Node(object):
    def __init__(self, entropy, data_yes, data_no, possible_splits):
        self.entropy = entropy
        self.data = data
        self.dataY = data_yes
        self.dataN = data_no
        self.children = {}
        self.possible_splits = possible_splits

    def makeChildren(self, split_category):
            #MAKES EVERYTHING ELSE WORK
    
    def ChildrenEntropy(self, category):
        total_entropy = 0
        children  = self.makeChildren(category)
        for child in children:
            total_entropy += child.entropy
        return total_entropy
    def getGain(self, category):
        self.entropy - self.ChildrenEntropy()

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
            if categories == []:
                categories = list
            else:
                dict = {}
                for i in range(len(list)):
                    if i == len(list)-1:
                        dict['outcome'] = list[i]
                    else:
                        dict[categories[i]] = list[i]
                data.append(dict)
    cagegories = categories[:-1]
    return [data,categories]

def entropy(y, n):
    t = y+n
    ent = (y/t)*math.log(t/y, 2)  + (n/t)*math.log(t/n,2)
    return ent

def split(node):
    best = None
    for category in node.possible_splits:
        if best is None or gain(node) > gain(best)

def makeTree(data, categories):
    dataY = []
    dataN = []
    for row in data:
        if row["outcome"] == "yes":
            dataY.append(row)
        else:
            dataN.append(row)
    root = Node(entropy(len(dataY), len(dataN)), dataY, dataN, categories)
    split(root)









if __name__ == '__main__':
    dataset = parse()
    data = load_dataset(dataset)
