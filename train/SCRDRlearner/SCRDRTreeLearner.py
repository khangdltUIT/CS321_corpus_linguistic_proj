# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

class Node:
    """
    A class to represent the nodes in SCRDR tree
    """

    def __init__(self, condition, conclusion, father=None, exceptChild=None, elseChild=None, cornerstoneCases=[], depth=0):
        self.condition = condition
        self.conclusion = conclusion
        self.father = father
        self.exceptChild = exceptChild
        self.elseChild = elseChild
        self.cornerstoneCases = cornerstoneCases
        self.depth = depth

    def satisfied(self, object):
        return eval(self.condition)

    def executeConclusion(self, object):
        exec(self.conclusion)

    def appendCornerstoneCase(self, object):
        self.cornerstoneCases.append(object)

    def check(self, object):
        if self.satisfied(object):
            self.executeConclusion(object)
            if self.exceptChild != None:
                self.exceptChild.check(object)
        else:
            if self.elseChild != None:
                self.elseChild.check(object)

    def checkDepth(self, object, length):
        if self.depth <= length:
            if self.satisfied(object):
                self.executeConclusion(object)
                if self.exceptChild != None:
                    self.exceptChild.checkDepth(object, length)
            else:
                if self.elseChild != None:
                    self.elseChild.checkDepth(object, length)

    def findRealFather(self):
        node = self
        fatherNode = node.father
        while True and fatherNode != None:
            if fatherNode.exceptChild == node:
                break
            node = fatherNode
            fatherNode = node.father
        return fatherNode

    def addElseChild(self, node):
        fatherNode = self.findRealFather()
        for object in fatherNode.cornerstoneCases:
            if node.satisfied(object):
                print("The new rule fires the cornerstone cases of its father node!!!")
                self.findRealFather().cornerstoneCases.remove(object)
        self.elseChild = node
        return True

    def addExceptChild(self, node):
        for object in self.cornerstoneCases:
            if node.satisfied(object):
                print("The new rule fires the cornerstone cases of its father node!!!")
                self.cornerstoneCases.remove(object)
        self.exceptChild = node
        return True

    def writeToFileWithSeenCases(self, out, depth):
        space = tabStr(depth)
        out.write(space + self.condition + " : " + self.conclusion + "\n")
        for case in self.cornerstoneCases:
            out.write(" " + space + "cc: " + case.toStr() + "\n")
        if self.exceptChild != None:
            self.exceptChild.writeToFile(out, depth + 1)
        if self.elseChild != None:
            self.elseChild.writeToFile(out, depth)

    def writeToFile(self, out, depth):
        space = tabStr(depth)
        out.write(space + self.condition + " : " + self.conclusion + "\n")
        if self.exceptChild != None:
            self.exceptChild.writeToFile(out, depth + 1)
        if self.elseChild != None:
            self.elseChild.writeToFile(out, depth)


def tabStr(length):
    return "".join(["\t"] * length)


class Object:
    attributes = ["word",
                  "tag",
                  "prevWord2",
                  "prevWord1",
                  "nextWord1",
                  "nextWord2",
                  "prevTag2",
                  "prevTag1",
                  "nextTag1",
                  "nextTag2",
                  "suffixL2",
                  "suffixL3",
                  "suffixL4"]
    code = "def __init__(self"
    for att in attributes:
        code = code + ", " + att + " = None"
    code = code + "):\n"
    for att in attributes:
        code = code + "    self." + att + "=" + att + "\n"

    exec(code)

    def toStr(self):
        res = "("
        for att in Object.attributes:
            boo = eval("isinstance(self. " + att + ", str)")
            if not boo:
                res = res + str(eval("self." + att))
            else:
                res = res + "\"" + str(eval("self." + att)) + "\""

            if att != Object.attributes[len(Object.attributes) - 1]:
                res = res + ","
        res += ")"
        return res


def getWordTag(wordTag):
    if wordTag == "///":
        return "/", "/"
    index = wordTag.rfind("/")
    word = wordTag[:index].strip()
    tag = wordTag[index + 1:].strip()
    return word, tag


def getObject(wordTags, index):  # Sequence of "Word/Tag"
    word, tag = getWordTag(wordTags[index])
    #print(word)
    #word = word.decode("utf-8").lower().encode("utf-8")
    word = word.lower()

    preWord1 = preTag1 = preWord2 = preTag2 = ""
    nextWord1 = nextTag1 = nextWord2 = nextTag2 = ""
    suffixL2 = suffixL3 = suffixL4 = ""

    decodedW = word  # .decode("utf-8")
    if len(decodedW) >= 4:
        suffixL3 = decodedW[-3:].encode("utf-8")
        suffixL2 = decodedW[-2:].encode("utf-8")
    if len(decodedW) >= 5:
        suffixL4 = decodedW[-4:].encode("utf-8")

    if index > 0:
        preWord1, preTag1 = getWordTag(wordTags[index - 1])
        preWord1 = preWord1.lower()  # .decode("utf-8").lower().encode("utf-8")
    if index > 1:
        preWord2, preTag2 = getWordTag(wordTags[index - 2])
        preWord2 = preWord2.lower()  # .decode("utf-8").lower().encode("utf-8")
    if index < len(wordTags) - 1:
        nextWord1, nextTag1 = getWordTag(wordTags[index + 1])
        nextWord1 = nextWord1.lower()  # .decode("utf-8").lower().encode("utf-8")
    if index < len(wordTags) - 2:
        nextWord2, nextTag2 = getWordTag(wordTags[index + 2])
        nextWord2 = nextWord2.lower()  # .decode("utf-8").lower().encode("utf-8")

    return Object(word, tag, preWord2, preWord1, nextWord1, nextWord2, preTag2, preTag1, nextTag1, nextTag2, suffixL2, suffixL3, suffixL4)


def getObjectDictionary(initializedCorpus, goldStandardCorpus):
    goldStandardSens = open(goldStandardCorpus, "r",
                            encoding='utf8').readlines()
    initializedSens = open(initializedCorpus, "r", encoding='utf8').readlines()

    objects = {}
    j = 0
    for i in xrange(len(initializedSens)):
        init = initializedSens[i].strip()
        if len(init) == 0:
            continue

        while j < len(goldStandardSens) and goldStandardSens[j].strip() == "":
            j += 1

        if j >= len(goldStandardSens):
            continue

        gold = goldStandardSens[j].strip()
        j += 1

        initWordTags = init.replace("“", "''").replace(
            "”", "''").replace("\"", "''").split()
        goldWordTags = gold.replace("“", "''").replace(
            "”", "''").replace("\"", "''").split()
        
        for k in xrange(len(initWordTags)):
            initWord, initTag = getWordTag(initWordTags[k])
            goldWord, correctTag = getWordTag(goldWordTags[k])
            #print("initWord: {} goldWord: {}".format(initWord, goldWord))
            if initWord != goldWord:
                print(
                    "\ERROR - 1 ==> Raw texts extracted from the gold standard corpus and the initialized corpus are not the same!")
                return None

            if initTag not in objects.keys():
                objects[initTag] = {}
                objects[initTag][initTag] = []

            if correctTag not in objects[initTag].keys():
                objects[initTag][correctTag] = []

            objects[initTag][correctTag].append(getObject(initWordTags, k))

    return objects


class FWObject:
    """
    RDRPOSTaggerV1.1: new implementation scheme
    RDRPOSTaggerV1.2: add suffixes
    """

    def __init__(self, check=False):
        self.context = [None, None, None, None, None,
                        None, None, None, None, None, None, None, None]
        if(check == True):
            i = 0
            while (i < 10):
                self.context[i] = "<W>"
                self.context[i + 1] = "<T>"
                i = i + 2
            self.context[10] = "<SFX>"  # suffix
            self.context[11] = "<SFX>"
            self.context[12] = "<SFX>"
        self.notNoneIds = []

    @staticmethod
    def getFWObject(startWordTags, index):
        object = FWObject(True)
        word, tag = getWordTag(startWordTags[index])
        object.context[4] = word.decode("utf-8").lower().encode("utf-8")
        object.context[5] = tag

        decodedW = word.decode("utf-8")
        if len(decodedW) >= 4:
            object.context[10] = decodedW[-2:].encode("utf-8")
            object.context[11] = decodedW[-3:].encode("utf-8")
        if len(decodedW) >= 5:
            object.context[12] = decodedW[-4:].encode("utf-8")

        if index > 0:
            preWord1, preTag1 = getWordTag(startWordTags[index - 1])
            object.context[2] = preWord1.decode(
                "utf-8").lower().encode("utf-8")
            object.context[3] = preTag1

        if index > 1:
            preWord2, preTag2 = getWordTag(startWordTags[index - 2])
            object.context[0] = preWord2.decode(
                "utf-8").lower().encode("utf-8")
            object.context[1] = preTag2

        if index < len(startWordTags) - 1:
            nextWord1, nextTag1 = getWordTag(startWordTags[index + 1])
            object.context[6] = nextWord1.decode(
                "utf-8").lower().encode("utf-8")
            object.context[7] = nextTag1

        if index < len(startWordTags) - 2:
            nextWord2, nextTag2 = getWordTag(startWordTags[index + 2])
            object.context[8] = nextWord2.decode(
                "utf-8").lower().encode("utf-8")
            object.context[9] = nextTag2

        return object

# add



#from Object import getObjectDictionary

# -*- coding: utf-8 -*-


#from Object import FWObject


class SCRDRTree:
    """
    Single Classification Ripple Down Rules tree for Part-of-Speech and morphological tagging
    """

    def __init__(self, root=None):
        self.root = root

    def findDepthNode(self, node, depth):
        while node.depth != depth:
            node = node.father
        return node

    def classify(self, object):
        self.root.check(object)

    def writeToFileWithSeenCases(self, outFile):
        out = open(outFile, "w")
        self.root.writeToFileWithSeenCases(out, 0)
        out.close()

    def writeToFile(self, outFile):
        out = open(outFile, "w", encoding='utf8')
        self.root.writeToFile(out, 0)
        out.close()

    # Build tree from file containing rules using FWObject
    def constructSCRDRtreeFromRDRfile(self, rulesFilePath):

        self.root = Node(FWObject(False), "NN", None, None, None, [], 0)
        currentNode = self.root
        currentDepth = 0

        rulesFile = open(rulesFilePath, "r")
        lines = rulesFile.readlines()

        for i in xrange(1, len(lines)):
            line = lines[i]
            depth = 0
            for c in line:
                if c == '\t':
                    depth = depth + 1
                else:
                    break

            line = line.strip()
            if len(line) == 0:
                continue

            temp = line.find("cc")
            if temp == 0:
                continue

            condition = getCondition(line.split(" : ", 1)[0].strip())
            conclusion = getConcreteValue(line.split(" : ", 1)[1].strip())

            node = Node(condition, conclusion, None, None, None, [], depth)

            if depth > currentDepth:
                currentNode.exceptChild = node
            elif depth == currentDepth:
                currentNode.elseChild = node
            else:
                while currentNode.depth != depth:
                    currentNode = currentNode.father
                currentNode.elseChild = node

            node.father = currentNode
            currentNode = node
            currentDepth = depth

    def findFiredNode(self, fwObject):
        currentNode = self.root
        firedNode = None
        obContext = fwObject.context
        while True:
            # Check whether object satisfying the current node's condition
            cnContext = currentNode.condition.context
            notNoneIds = currentNode.condition.notNoneIds
            satisfied = True
            for i in notNoneIds:
                if cnContext[i] != obContext[i]:
                    satisfied = False
                    break

            if(satisfied):
                firedNode = currentNode
                exChild = currentNode.exceptChild
                if exChild is None:
                    break
                else:
                    currentNode = exChild
            else:
                elChild = currentNode.elseChild
                if elChild is None:
                    break
                else:
                    currentNode = elChild
        return firedNode

#    def findFiredNodeInDepth(self, fwObject, depth):
#        currentNode = self.root
#        firedNode = None
#        while True:
#            if(currentNode.condition.isSatisfied(fwObject)):
#                firedNode = currentNode
#                if currentNode.exceptChild is None:
#                    break
#                else:
#                    currentNode = currentNode.exceptChild
#            else:
#                if currentNode.elseChild is None:
#                    break
#                else:
#                    currentNode = currentNode.elseChild
#            if currentNode.depth > depth:
#                break
#        return firedNode
#
#    #Count number of nodes in exception-structure levels
#    def countNodes(self, inDepth):
#        currentNode = self.root
#        nodeQueue = []
#        nodeQueue.append(currentNode)
#        count = 0
#        while len(nodeQueue) > 0:
#            currentNode = nodeQueue[0]
#            #Current node's depth is smaller than a given threshold
#            if currentNode.depth <= inDepth:
#                count += 1
#            if currentNode.exceptChild is not None:
#                nodeQueue.append(currentNode.exceptChild)
#            if currentNode.elseChild is not None:
#                nodeQueue.append(currentNode.elseChild)
#            nodeQueue = nodeQueue[1:]
#        return count

def getObjectDictionary(initializedCorpus, goldStandardCorpus):
    goldStandardSens = open(goldStandardCorpus, "r",
                            encoding='utf8').readlines()
    initializedSens = open(initializedCorpus, "r", encoding='utf8').readlines()

    objects = {}

    j = 0
    for i in range(len(initializedSens)):
        init = initializedSens[i].strip()
        if len(init) == 0:
            continue

        while j < len(goldStandardSens) and goldStandardSens[j].strip() == "":
            j += 1

        if j >= len(goldStandardSens):
            continue

        gold = goldStandardSens[j].strip()
        j += 1

        initWordTags = init.replace("“", "''").replace(
            "”", "''").replace("\"", "''").split()
        goldWordTags = gold.replace("“", "''").replace(
            "”", "''").replace("\"", "''").split()

        for k in range(len(initWordTags)):
            initWord, initTag = getWordTag(initWordTags[k])
            goldWord, correctTag = getWordTag(goldWordTags[k])

            print("initword: {}  goldword: {}".format(initWord, goldWord))
            #break
            if initWord == goldWord:
                print("same\n")
            if initWord != goldWord:
                print(
                    "\nERROR - 2 ==> Raw texts extracted from the gold standard corpus and the initialized corpus are not the same!")
                return None

            if initTag not in objects.keys():
                objects[initTag] = {}
                objects[initTag][initTag] = []

            if correctTag not in objects[initTag].keys():
                objects[initTag][correctTag] = []

            objects[initTag][correctTag].append(getObject(initWordTags, k))

    return objects

def getConcreteValue(str):
    if str.find('""') > 0:
        if str.find("Word") > 0:
            return "<W>"
        elif str.find("suffixL") > 0:
            return "<SFX>"
        else:
            return "<T>"
    return str[str.find("\"") + 1: len(str) - 1]


def getCondition(strCondition):
    condition = FWObject(False)
    for rule in strCondition.split(" and "):
        rule = rule.strip()
        key = rule[rule.find(".") + 1: rule.find(" ")]
        value = getConcreteValue(rule)

        if key == "prevWord2":
            condition.context[0] = value
        elif key == "prevTag2":
            condition.context[1] = value
        elif key == "prevWord1":
            condition.context[2] = value
        elif key == "prevTag1":
            condition.context[3] = value
        elif key == "word":
            condition.context[4] = value
        elif key == "tag":
            condition.context[5] = value
        elif key == "nextWord1":
            condition.context[6] = value
        elif key == "nextTag1":
            condition.context[7] = value
        elif key == "nextWord2":
            condition.context[8] = value
        elif key == "nextTag2":
            condition.context[9] = value
        elif key == "suffixL2":
            condition.context[10] = value
        elif key == "suffixL3":
            condition.context[11] = value
        elif key == "suffixL4":
            condition.context[12] = value
    for i in xrange(13):
        if condition.context[i] is not None:
            condition.notNoneIds.append(i)
    return condition


if __name__ == "__main__":
    pass


#from SCRDRTree import SCRDRTree

# Generate concrete rules based on input object of 5-word window context object
def generateRules(object):
    # 1. Current word
    rule1 = "object.word == \"" + object.word + "\""
    # 2. Next 1st word
    rule2 = "object.nextWord1 == \"" + object.nextWord1 + "\""
    # 3. Next 2nd word
    rule3 = "object.nextWord2 == \"" + object.nextWord2 + "\""
    # 4. Previous 1st word
    rule4 = "object.prevWord1 == \"" + object.prevWord1 + "\""
    # 5. Previous 2nd word
    rule5 = "object.prevWord2 == \"" + object.prevWord2 + "\""

    # 6. Current word and next 1st word
    rule6 = rule1 + " and " + rule2
    # 7. Previous 1st word and current word
    rule7 = rule4 + " and " + rule1
    # 11. Previous 1st word and next 1st word
    rule11 = rule4 + " and " + rule2
    # 29. Next 1st word and next 2nd word
    #rule29 = rule2 + " and " + rule3
    # 30. Previous 2nd word and previous 1st word
    #rule30 = rule5 + " and " + rule4
    # 19. Current word and next 2nd word
    rule19 = rule1 + " and " + rule3
    # 20. Previous 2nd word and current word
    rule20 = rule5 + " and " + rule1

    # 8. Current word, next 1st word and next 2nd word
    rule8 = rule6 + " and " + rule3
    # 9. Previous 2nd word, previous 1st word and current word
    rule9 = rule5 + " and " + rule7
    # 10. Previous 1st word, current word and next 1st word
    rule10 = rule4 + " and " + rule6

    # 12. Next 1st tag
    rule12 = "object.nextTag1 == \"" + object.nextTag1 + "\""
    # 13. Next 2nd tag
    rule13 = "object.nextTag2 == \"" + object.nextTag2 + "\""
    # 14. Previous 1st tag
    rule14 = "object.prevTag1 == \"" + object.prevTag1 + "\""
    # 15. Previous 2nd tag
    rule15 = "object.prevTag2 == \"" + object.prevTag2 + "\""
    # 16. Next 1st tag and next 2nd tag
    rule16 = rule12 + " and " + rule13
    # 17. Previous 2nd tag and previous 1st tag
    rule17 = rule15 + " and " + rule14
    # 18. Previous 1st tag and next 1st tag
    rule18 = rule14 + " and " + rule12

    # 21. Current word and next 1st tag
    rule21 = rule1 + " and " + rule12
    # 22. Current word and previous 1st tag
    rule22 = rule14 + " and " + rule1
    # 23. Previous 1st tag, current word and next 1st tag
    rule23 = rule14 + " and " + rule21
    # 24. Current word and 2 next tags.
    rule24 = rule1 + " and " + rule16
    # 25. 2 previous tags and current word
    rule25 = rule17 + " and " + rule1
    # 26. 2-character suffix
    #rule26 = "object.suffixL2 == \"" + object.suffixL2 + "\""
    # 27. 3-character suffix
    #rule27 = "object.suffixL3 == \"" + object.suffixL3 + "\""
    # 28. 4-character suffix
    #rule28 = "object.suffixL4 == \"" + object.suffixL4 + "\""

    rules = []
    rules.append(rule1)
    rules.append(rule2)
    rules.append(rule3)
    rules.append(rule4)
    rules.append(rule5)
    rules.append(rule6)
    rules.append(rule7)
    rules.append(rule8)
    rules.append(rule9)
    rules.append(rule10)
    rules.append(rule11)
    rules.append(rule12)
    rules.append(rule13)
    rules.append(rule14)
    rules.append(rule15)
    rules.append(rule16)
    rules.append(rule17)
    rules.append(rule18)
    rules.append(rule19)
    rules.append(rule20)
    rules.append(rule21)
    rules.append(rule22)
    rules.append(rule23)
    rules.append(rule24)
    rules.append(rule25)
    # rules.append(rule26)
    # rules.append(rule27)
    # rules.append(rule28)
    # rules.append(rule29)
    # rules.append(rule30)

    rules = set(rules)
    return rules


def countMatching(objects, ruleNotIn):
    counts = {}
    matchedObjects = {}
    for object in objects:
        rules = generateRules(object)
        for rule in rules:
            if rule in ruleNotIn:
                continue
            counts[rule] = counts.setdefault(rule, 0) + 1
            matchedObjects.setdefault(rule, []).append(object)
    return counts, matchedObjects


def satisfy(object, rule):
    return eval(rule)


def fire(rule, cornerstoneCases):
    for object in cornerstoneCases:
        if satisfy(object, rule):
            return True
    return False


def generateRulesFromObjectSet(objects):
    res = []
    for object in objects:
        rules = generateRules(object)
        res += rules
    return res


class SCRDRTreeLearner(SCRDRTree):
    def __init__(self, iThreshold=2, mThreshold=2):
        self.improvedThreshold = iThreshold
        self.matchedThreshold = mThreshold

    # For layer-2 exception structure
    def findMostImprovingRuleForTag(self, startTag, correctTag, correctCounts, wrongObjects):
        impCounts, affectedObjects = countMatching(wrongObjects, [])

        maxImp = -1000000
        bestRule = ""
        for rule in impCounts:
            temp = impCounts[rule]
            if rule in correctCounts:
                temp -= correctCounts[rule]

            if temp > maxImp:
                maxImp = temp
                bestRule = rule

        if maxImp == -1000000:
            affectedObjects[bestRule] = []

        return bestRule, maxImp, affectedObjects[bestRule]

    def findMostEfficientRule(self, startTag, objects, correctCounts):
        maxImp = -1000000
        rule = ""
        correctTag = ""
        cornerstoneCases = []

        for tag in objects:
            if tag == startTag:
                continue
            if len(objects[tag]) <= maxImp or len(objects[tag]) < self.improvedThreshold:
                continue

            ruleTemp, imp, affectedObjects = self.findMostImprovingRuleForTag(
                startTag, correctTag, correctCounts, objects[tag])
            if imp >= self.improvedThreshold and imp > maxImp:
                maxImp = imp
                rule = ruleTemp
                correctTag = tag
                cornerstoneCases = affectedObjects

        needToCorrectObjects = {}
        errorRaisingObjects = []
        if maxImp > -1000000:
            for tag in objects:
                if tag != correctTag:
                    for object in objects[tag]:
                        if satisfy(object, rule):
                            needToCorrectObjects.setdefault(
                                tag, []).append(object)
                            if tag == startTag:
                                errorRaisingObjects.append(object)

        return rule, correctTag, maxImp, cornerstoneCases, needToCorrectObjects, errorRaisingObjects

    def findMostMatchingRule(self, matchingCounts):
        correctTag = ""
        bestRule = ""
        maxCount = -1000000

        for tag in matchingCounts:
            for rule in matchingCounts[tag]:
                if matchingCounts[tag][rule] >= self.matchedThreshold and matchingCounts[tag][rule] > maxCount:
                    maxCount = matchingCounts[tag][rule]
                    bestRule = rule
                    correctTag = tag

        return bestRule, correctTag

    def buildNodeForObjectSet(self, objects, root):
        cornerstoneCaseRules = generateRulesFromObjectSet(
            root.cornerstoneCases)

        matchingCounts = {}
        matchingObjects = {}
        for tag in objects:
            matchingCounts[tag], matchingObjects[tag] = countMatching(
                objects[tag], cornerstoneCaseRules)

        total = 0
        for tag in objects:
            total += len(objects[tag])

        currentNode = root
        elseChild = False
        while True:
            rule, correctTag = self.findMostMatchingRule(matchingCounts)

            if rule == "":
                break

            cornerstoneCases = matchingObjects[correctTag][rule]

            needToCorrectObjects = {}
            for tag in objects:
                if rule in matchingObjects[tag]:
                    if tag != correctTag:
                        needToCorrectObjects[tag] = matchingObjects[tag][rule]
                    for object in matchingObjects[tag][rule]:
                        rules = generateRules(object)
                        for rule1 in rules:
                            if rule1 not in matchingCounts[tag]:
                                continue
                            matchingCounts[tag][rule1] -= 1

            node = Node(rule, "object.conclusion = \"" + correctTag +
                        "\"", currentNode, None, None, cornerstoneCases)

            if not elseChild:
                currentNode.exceptChild = node
                elseChild = True
            else:
                currentNode.elseChild = node

            currentNode = node
            self.buildNodeForObjectSet(needToCorrectObjects, currentNode)

    def learnRDRTree(self, initializedCorpus, goldStandardCorpus):
        self.root = Node("True", 'object.conclusion = "NN"',
                         None, None, None, 0)

        objects = getObjectDictionary(initializedCorpus, goldStandardCorpus)
        # print(objects)
        currentNode = self.root

        for initializedTag in objects:
            print("\n===> Building exception rules for tag %s" % initializedTag)
            correctCounts = {}
            for object in objects[initializedTag][initializedTag]:
                rules = generateRules(object)
                for rule in rules:
                    correctCounts[rule] = correctCounts.setdefault(rule, 0) + 1

            node = Node("object.tag == \"" + initializedTag + "\"",
                        "object.conclusion = \"" + initializedTag + "\"", self.root, None, None, [], 1)

            if self.root.exceptChild == None:
                self.root.exceptChild = node
            else:
                currentNode.elseChild = node

            currentNode = node
            objectSet = objects[initializedTag]

            elseChild = False
            currentNode1 = currentNode
            while True:
                rule, correctTag, imp, cornerstoneCases, needToCorrectObjects, errorRaisingObjects = self.findMostEfficientRule(
                    initializedTag, objectSet, correctCounts)
                if imp < self.improvedThreshold:
                    break

                node = Node(rule, "object.conclusion = \"" + correctTag +
                            "\"", currentNode, None, None, cornerstoneCases, 2)

                if not elseChild:
                    currentNode1.exceptChild = node
                    elseChild = True
                else:
                    currentNode1.elseChild = node

                currentNode1 = node

                for object in cornerstoneCases:
                    objectSet[correctTag].remove(object)

                for tag in needToCorrectObjects:
                    for object in needToCorrectObjects[tag]:
                        objectSet[tag].remove(object)

                for object in errorRaisingObjects:
                    rules = generateRules(object)
                    for rule in rules:
                        correctCounts[rule] -= 1

                self.buildNodeForObjectSet(needToCorrectObjects, currentNode1)
