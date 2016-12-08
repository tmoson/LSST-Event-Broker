import random
import math


class Classifier:
    def __init__(self, cls, f1, f2, factor):
        self.alphabet = [26]
        self.__class = cls
        self.__fact = factor
        self.__f1 = f1
        self.__f2 = f2
        self.alphabet = {'a' 'b' 'c' 'd' 'e' 'f' 'g' 'h' 'i' 'j' 'k' 'l' 'm' 'n' 'o' 'p' 'q' 'r' 's' 't' 'u' 'v' 'w' 'x' 'y' 'z'}

    def get_type(self):
        return self.__class

    def substring(self, ineq):
        index = 0
        substring = ""
        while ineq[index] != '<' and ineq[index] != '>' and ineq[index] != '=':
            if ineq[index] != ' ':
                substring = substring + ineq[index]
            index += 1
        return substring

    def getcmp(self, ineq, i):
        index = i + 1
        cmp = ineq[index]
        if ineq[index] == '=' or ineq[index] == '<' or ineq[index] == '>':
            index += 1
            cmp = ineq[index]
        if index != ineq.len() - 1:
            index += 1
            for num in range(index, ineq.len()):
                cmp = cmp + ineq[num]
        return int(cmp)

    def apply_rules(self, i):
        index = 0
        sub1 = self.substring(self.__f1)
        check = int(sub1[0])
        f1cmp = self.getcmp(self.__f1, sub1.len())
        f1res = False
        f2res = False
        sub2 = self.substring(self.__f2)
        f2cmp = self.getcmp(self.__f1, sub2.len())
        if "+" or "-" or "*" or "/" in sub1:
            while index < sub1.len():
                if sub1[index] == '+':
                    if sub1[index + 1] not in self.alphabet:
                        check += int(sub1[index + 1])
                    else:
                        check += i
                    index += 2
                elif sub1[index] == '-':
                    if sub1[index + 1] not in self.alphabet:
                        check -= int(sub1[index + 1])
                    else:
                        check -= i
                    index += 2
                elif sub1[index] == '*':
                    if sub1[index + 1] not in self.alphabet:
                        check *= int(sub1[index + 1])
                    else:
                        check *= i
                    index += 2
                elif sub1[index] == '/':
                    if sub1[index + 1] not in self.alphabet:
                        check /= int(sub1[index + 1])
                    else:
                        check /= i
                    index += 2
        else:
            check = i
        if '=' and '>' in self.__f1:
            if check >= f1cmp:
                f1res = True
        elif '=' and '<' in self.__f1:
            if check <= f1cmp:
                f1res = True
        elif '>' in self.__f1:
            if check > f1cmp:
                f1res = True
        elif '<' in self.__f1:
            if check < f1cmp:
                f1res = True
        check = sub2[0]
        index = 0
        if "+" or "-" or "*" or "/" in sub2:
            while index < sub2.len():
                if sub1[index] == '+':
                    if sub2[index + 1] not in self.alphabet:
                        check += int(sub1[index + 1])
                    else:
                        check += i
                    index += 2
                elif sub2[index] == '-':
                    if sub2[index + 1] not in self.alphabet:
                        check -= int(sub2[index + 1])
                    else:
                        check -= i
                    index += 2
                elif sub2[index] == '*':
                    if sub2[index + 1] not in self.alphabet:
                        check *= int(sub2[index + 1])
                    else:
                        check *= i
                    index += 2
                elif sub2[index] == '/':
                    if sub2[index + 1] not in self.alphabet:
                        check /= int(sub1[index + 1])
                    else:
                        check /= i
                    index += 2
        if '=' and '>' in self.__f2:
            if check >= f2cmp:
                f2res = True
        elif '=' and '<' in self.__f2:
            if check <= f2cmp:
                f2res = True
        elif '>' in self.__f2:
            if check > f2cmp:
                f2res = True
        elif '<' in self.__f2:
            if check < f2cmp:
                f2res = True

        return f1res and f2res

    def classify(self, trans):
        if trans.getnumobs(trans) < 10:
            return False
        elif self.__fact == "period":
            if self.apply_rules(trans.period):
                trans.lastClassifier = self.get_type()
                trans.classification = self.get_type()
                return True
            else:
                trans.lastClassifier = self.get_type()
                return False
        elif self.__fact == "frequency":
            if self.apply_rules(trans.freq):
                trans.lastClassifier = self.get_type()
                trans.classification = self.get_type()
                return True
            else:
                trans.lastClassifier = self.get_type()
                return False
        elif self.__fact == "magnitude":
            if self.apply_rules(trans.magnitude):
                trans.lastClassifier = self.get_type()
                trans.classification = self.get_type()
                return True
            else:
                trans.lastClassifier = self.get_type()
                return False
