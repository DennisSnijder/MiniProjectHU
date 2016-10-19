import random
import math




class Neuron:

    def __init__(self, numberOfWeights):
        self.weights = []
        for x in range(numberOfWeights):
            self.weights.append(random.uniform(-1.0, 1.0))

    def activate(self, inputs):
        value = 0
        for x in range(len(inputs)):
            value += self.weights[x] * inputs[x]
        return 1 / (1 + math.exp(-value))


class Layer:

    def __init__(self, numberOfNeurons, numberOfInputs):
        self.neurons = []
        for x in range(numberOfNeurons):
            self.neurons.append(Neuron(numberOfInputs))

    def feed(self, inputs):
        outputs = []
        for x in range(len(self.neurons)):
            outputs.append(self.neurons[x].activate(inputs))
        return outputs


class Network:

    def __init__(self, structure):
        self.layers = []
        for x in range(1, len(structure)):
            self.layers.append(Layer(structure[x], structure[x-1]))

    def feedforward(self, inputs):
        for x in range(len(self.layers)):
            inputs = self.layers[x].feed(inputs)
        return inputs
