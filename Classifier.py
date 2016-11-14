import random
import math
# The code for this class is courtesy of Jason Brownlee of
# machinelearningmastery.com, and can be found at
# http://www.machinelearningmastery.com/naive-bayes-classifier-scratch-python/


class Classifier:

    def splitDataset(self, dataset, splitRatio):
        trainSize = int(len(dataset) * splitRatio)
        trainset = []
        copy = list(dataset)
        while len(trainset) < trainSize:
            index = random.randrange(len(copy))
            trainset.append(copy.pop(index))
        return [trainset, copy]

    def separate_by_class(self, dataset):
        separated = {}
        for i in range(len(dataset)):
            vector = dataset[i]
            if vector[-1] not in separated:
                separated[vector[-1]] = []
            separated[vector[-1]].append(vector)
        return separated

    def mean(self, numbers):
        return sum(numbers)/float(len(numbers))

    def stdev(self, numbers):
        avg = self.mean(numbers)
        variance = sum([pow(x-avg, 2) for x in numbers])/float(len(numbers)-1)
        return math.sqrt(variance)

    def summarize(self, dataset):
        summaries = [(self.mean(self, attribute), self.stdev(self, attribute)) for attribute in zip(*dataset)]
        del summaries[-1]
        return summaries

    def summarize_by_class(self, dataset):
        separated = self.separate_by_class(self, dataset)
        summaries = {}
        for classValue, instances in separated.iteritems():
            summaries[classValue] = self.summarize(instances)
        return summaries

    def calculate_probability(self, x, mean, stdev):
        exponent = math.exp(-(math.pow(x-mean, 2)/(2*math.pow(stdev, 2))))
        return (1/(math.sqrt(2*math.pi)*stdev))*exponent

    def calculate_class_probabilities(self, summaries, inputVector):
        probabilities = {}
        for classValue, classSummaries in summaries.iteritems():
            probabilities[classValue] = 1
            for i in range(len(classSummaries)):
                mean, stdev = classSummaries[i]
                x = inputVector[i]
                probabilities[classValue] *= self.calculateProbability(self, x, mean, stdev)
        return probabilities

    def predict(self, summaries, inputVector):
        probs = self.calculateClassProbabilities(self, summaries, inputVector)
        bestLabel, bestProb = None, -1
        for classValue, prob in probs.iteritems():
            if bestLabel is None or prob > bestProb:
                bestProb = prob
                bestLabel = classValue
        return bestLabel

    def get_predictions(self, summaries, testSet):
        predictions = []
        for i in range(len(testSet)):
            result = self.predict(self, summaries, testSet[i])
            predictions.append(result)
        return predictions

