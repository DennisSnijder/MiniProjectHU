from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from yahoo_finance import Share
import datetime
from datetime import date, timedelta
import random
import math
import json

class Neuron:

    def __init__(self, numberOfWeights):
        self.bias = 1.0

        self.weights = []
        for x in range(numberOfWeights):
            self.weights.append(random.uniform(-1.0, 1.0))

    def activate(self, inputs):
        value = 0.0
        for x in range(len(inputs)):
            value += self.weights[x] * inputs[x]
        value += self.bias
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

    def activate(self, inputs):
        for x in range(len(self.layers)):
            inputs = self.layers[x].feed(inputs)
        return inputs

    def getTotalError(self, inputs, desiredOutputs):
        return sum(self.getErrors(inputs, desiredOutputs))

    def getErrors(self, inputs, desiredOutputs):
        inputs = self.activate(inputs)
        for x in range(len(inputs)):
            inputs[x] = 0.5*(desiredOutputs[x]-inputs[x])**2
        return inputs

    def exportWeights(self):
        export = []
        for x in self.layers:
            for y in x.neurons:
                for z in y.weights:
                    export.append(z)
        return export

    def importWeights(self, weights):
        ex = 0
        for x in range(len(self.layers)):
            for y in range(len(self.layers[x].neurons)):
                for z in range(len(self.layers[x].neurons[y].weights)):
                    self.layers[x].neurons[y].weights[z] = weights[ex]
                    ex += 1

class DNA:

    def __init__(self, min, max, length):
        self.min = min
        self.max = max
        self.length = length
        self.gene = []
        self.fitness = 0

        for x in range(length):
            self.gene.append(self.randomGene())

    def randomGene(self):
        return random.uniform(self.min, self.max)

    def mutate(self, rate):
        for x in range(self.length):
            if rate > random.uniform(0.0, 1.0):
                self.gene[x] = self.randomGene()

    def partner(self, partner, mutationRate):
        p = random.randrange(0, self.length)

        g1 = self.gene[0:p]
        g2 = partner.gene[p:]

        child = DNA(self.min, self.max, self.length)
        child.gene = g1 + g2
        child.mutate(mutationRate)

        return child

    def getFitness(self, network, inputs, output):
        self.fitness = 0

        network.importWeights(self.gene)
        for x in range(len(inputs)):
            r = network.activate(inputs[x])[0]
            self.fitness -= (0.5 * (output[x] - r) ** 2)

        self.fitness = -1/self.fitness
        self.fitness = math.pow(self.fitness, 4)

class Population:

    def __init__(self, size, mutationRate, eliminationRate, geneOptions):
        self.size = size
        self.mutationRate = mutationRate
        self.eliminationRate = eliminationRate
        self.geneOptions = geneOptions

        self.pool = []

        self.currentGeneration = 0
        self.averageFitness = 0
        self.bestDNA = DNA(geneOptions[0], geneOptions[1], geneOptions[2])

        for x in range(self.size):
            self.pool.append(DNA(geneOptions[0], geneOptions[1], geneOptions[2]))

    def calcFitness(self, network, inputs, output):
        self.averageFitness = 0
        for x in range(len(self.pool)):
            self.pool[x].getFitness(network, inputs, output)
            self.averageFitness += self.pool[x].fitness
        self.averageFitness /= self.size

    def naturalSelection(self):
        self.matingpool = []

        self.pool = sorted(self.pool, key=lambda fitness: fitness.fitness)

        el = math.floor(self.size * self.eliminationRate)

        for x in range(el):
            self.pool.pop(0)

        maxFitness = self.pool[-1].fitness
        self.bestDNA = self.pool[-1]

        for x in range(len(self.pool)):
            n = round((self.pool[x].fitness / maxFitness)*100)
            for y in range(n):
                self.matingpool.append(self.pool[x])

    def crossover(self):
        n = self.size - len(self.pool)
        for x in range(n):
            p1 = random.choice(self.matingpool)
            p2 = random.choice(self.matingpool)
            self.pool.append(p1.partner(p2, self.mutationRate))

    def nextGeneration(self, network, inputs, output):
        self.calcFitness(network, inputs, output)
        self.naturalSelection()
        self.crossover()
        self.currentGeneration += 1

class dataController:

    def __init__(self, data):
        self.data = data

    def normalise(self, value, min, max):
        value = float(value)
        min = float(min)
        max = float(max)
        return (value-min)/(max-min)


    def parseData(self):

        data = self.data

        result = []

        dataHighMin = 1000000
        dataHighMax = 0

        dataLowMin = 1000000
        dataLowMax = 0

        dataOpenMin = 1000000
        dataOpenMax = 0

        dataCloseMin = 1000000
        dataCloseMax = 0


        for x in range(len(data)):

            if float(data[x]['High']) > dataHighMax:
                dataHighMax = float(data[x]['High'])
            if float(data[x]['High']) < dataHighMin:
                dataHighMin = float(data[x]['High'])

            if float(data[x]['Low']) > dataLowMax:
                dataLowMax = float(data[x]['Low'])
            if float(data[x]['Low']) < dataLowMin:
                dataLowMin = float(data[x]['Low'])

            if float(data[x]['Open']) > dataOpenMax:
                dataOpenMax = float(data[x]['Open'])
            if float(data[x]['Open']) < dataOpenMin:
                dataOpenMin = float(data[x]['Open'])

            if float(data[x]['Close']) > dataCloseMax:
                dataCloseMax = float(data[x]['Close'])
            if float(data[x]['Close']) < dataCloseMin:
                dataCloseMin = float(data[x]['Close'])

        #Structure of result data [ Day, Open, Close, High, Low, DesiredOutput ]
        self.High = dataHighMax
        self.Low= dataLowMax
        self.Close = dataCloseMax
        self.Open = dataOpenMax

        for x in range(1, len(data)):
            result.append([x,self.normalise(data[x]['Open'], dataOpenMin, dataOpenMax),self.normalise(data[x]['Close'], dataCloseMin, dataCloseMax),self.normalise(data[x]['High'], dataHighMin, dataHighMax),self.normalise(data[x]['Low'], dataLowMin, dataLowMax), self.normalise(data[x-1]['Close'], dataCloseMin, dataCloseMax)])

        return result

class apiController:

    def getData(self, quote, numberOfDays):
        numberOfDays = int(numberOfDays)
        self.quote = Share(quote)

        currentDate = datetime.datetime.now()
        endDate = date(currentDate.year, currentDate.month, currentDate.day)
        startDate = endDate - timedelta(days=numberOfDays)

        endDate = '{}-{}-{}'.format(endDate.year, endDate.month, endDate.day)
        startDate= '{}-{}-{}'.format(startDate.year, startDate.month, startDate.day)

        self.data = self.quote.get_historical(startDate, endDate)

class App:

    def __init__(self):
        self.root = Tk()

        self.root.resizable(width=False, height=False)

        self.appView = Frame(self.root, height=300, width=400)

        self.optionWindow()

    def run(self):
        while True:
            try:
                mainloop()
                break
            except UnicodeDecodeError:
                pass

    def optionWindow(self):
        self.root.title("MiniProject | Stock Exchange Predictor")
        self.clearView()
        self.export = 'None'
        optionGroup = LabelFrame(self.appView, text="Options", padx=5, pady=5)

        symbolLabel = Label(optionGroup, text="Ticker Symbol: ")
        dataDaysLabel = Label(optionGroup, text="Number of days: ")
        orLabel = Label(optionGroup, text="or")

        self.symbolInput = Entry(optionGroup)
        self.dataDaysInput = Entry(optionGroup)

        importButton = Button(optionGroup, text="Import Existing", command=self.selectImportFile)
        createButton = Button(optionGroup, text="Create", command=self.predictionWindow)

        symbolLabel.grid_forget()
        dataDaysLabel.grid_forget()
        orLabel.grid_forget()
        self.symbolInput.grid_forget()
        self.dataDaysInput.grid_forget()
        importButton.grid_forget()
        createButton.grid_forget()

        symbolLabel.grid(row=0, column=0, sticky=E)
        dataDaysLabel.grid(row=1, column=0, sticky=E)
        orLabel.grid(row=2, column=1, sticky=W, pady=20)
        self.symbolInput.grid(row=0, column=1)
        self.dataDaysInput.grid(row=1, column=1)
        importButton.grid(row=3, column=1, sticky=W)
        createButton.grid(row=4, column=1, sticky=E, pady=10)

        optionGroup.pack(padx=40, pady=40, ipadx=10)

        self.appView.pack()

    def clearView(self):
        for child in self.appView.winfo_children():
            child.pack_forget()

    def loadData(self):

        if self.symbolInput.get() == "":
            messagebox.showerror("Error", "No symbol")
            self.optionWindow()
        if self.dataDaysInput.get() == "":
            messagebox.showerror("Error", "Need more days as data!")
            self.optionWindow()

        self.apiConnection = apiController()
        self.apiConnection.getData(self.symbolInput.get(), self.dataDaysInput.get())

        self.dataCon = dataController(self.apiConnection.data)
        self.data = self.dataCon.parseData()

        #Data
        self.data.reverse()

        self.actualData = []
        self.predictedData = []

        for x in self.data:
            self.actualData.append(x[1])
            self.predictedData.append(x[1])

        # YOU CAN CHANGE NETWORK STRUCTURE AND POOL SETTINGS HERE
        self.network = Network([4, 15, 1])
        self.pool = Population(100, 0.01, 0.4, [-5, 5, 75])

        inputs = []
        desiredOutputs = []

        for x in range(len(self.data)):
            inputs.append(self.data[x][1:5])
            desiredOutputs.append(self.data[x][5])

        self.calculateGraph()

    def nextGen1(self):
        self.nextGenX(1)

    def nextGen10(self):
        self.nextGenX(10)

    def nextGen100(self):
        self.nextGenX(100)

    def nextGen1000(self):
        self.nextGenX(1000)

    def nextGenX(self, i):
        inputs = []
        desiredOutputs = []

        for x in range(len(self.data)):
            inputs.append(self.data[x][1:5])
            desiredOutputs.append(self.data[x][5])

        for x in range(i):
            self.generationLabel.config(text='Generation: {}'.format(self.pool.currentGeneration))
            self.pool.nextGeneration(self.network, inputs, desiredOutputs)
            print("Generation:", self.pool.currentGeneration, "Best Fitness :", self.pool.bestDNA.fitness)

        self.calculateGraph()
        self.a.clear()
        self.a.plot(self.actualData)
        self.a.plot(self.predictedData)
        self.canvas.draw()

    def predictionWindow(self):
        self.root.title("MiniProject | Stock Exchange Predictor")
        self.clearView()
        if(self.export == 'None'):
            self.loadData()

        neuralGroup = LabelFrame(self.appView, text="Neural Network", padx=5, pady=5)
        actionGroup = LabelFrame(self.appView, text="Info & Actions", padx=5, pady=5)

        neuralGroup.grid(row=1, column=1, sticky=E, pady=10)
        actionGroup.grid(row=1, column=2, sticky=E, pady=10)

        self.generationLabel = Label(actionGroup, text="Generation: {}".format(self.pool.currentGeneration))


        nextGen1 = Button(actionGroup, text="1x Iterations", command=self.nextGen1)
        nextGen2 = Button(actionGroup, text="10x Iterations", command=self.nextGen10)
        nextGen3 = Button(actionGroup, text="100x Iterations", command=self.nextGen100)
        nextGen4 = Button(actionGroup, text="1000x Iterations", command=self.nextGen1000)
        predictButton = Button(actionGroup, text="Predict tomorrow", command=self.predict)
        exportButton = Button(actionGroup, text="Export", command=self.exportNetwork)
        nextGen1.grid_forget()
        nextGen2.grid_forget()
        nextGen3.grid_forget()
        nextGen4.grid_forget()
        predictButton.grid_forget()
        exportButton.grid_forget()
        self.generationLabel.grid_forget()
        self.generationLabel.grid(row=1, column=1, sticky=E, pady=10)

        nextGen1.grid(row=4, column=1, sticky=E, pady=10)
        nextGen2.grid(row=5, column=1, sticky=E, pady=10)
        nextGen3.grid(row=6, column=1, sticky=E, pady=10)
        nextGen4.grid(row=7, column=1, sticky=E, pady=10)
        predictButton.grid(row=8, column=1, sticky=E, pady=10)
        exportButton.grid(row=9, column=1, sticky=E, pady=10)

        self.f = Figure(figsize=(5,5), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.plot(self.actualData)
        self.a.plot(self.predictedData)

        self.canvas = FigureCanvasTkAgg(self.f, neuralGroup)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(expand=True)

        self.appView.pack(padx=10, pady=10)

    def predict(self):
        d = [float(self.dataCon.data[0]['Open']) / self.dataCon.Open, float(self.dataCon.data[0]['Close']) / self.dataCon.Close, float(self.dataCon.data[0]['High']) / self.dataCon.High, float(self.dataCon.data[0]['Low']) / self.dataCon.Low]
        self.network.importWeights(self.pool.bestDNA.gene)
        result = self.network.activate(d)[0] * self.dataCon.Close
        result = round(result, 2)
        messagebox.showinfo('Prediction', "Next day's Close prediction $"+str(result))

    def selectImportFile(self):
        self.importNetwork(filedialog.askopenfilename())

    def importNetwork(self, path):
        try:
            f = open(path, 'r')
            result = json.loads(f.read())
            self.export = result
            f.close()

        except:
            messagebox.showerror("Error", "Something went wrong")
        self.initExport()

    def initExport(self):
        self.apiConnection = apiController()
        self.apiConnection.data = self.export['apiConnectionData']
        self.dataCon = dataController(self.export['apiConnectionData'])
        self.data = self.dataCon.parseData()
        #Data
        self.data.reverse()
        self.actualData = []
        self.predictedData = []
        for x in self.data:
            self.actualData.append(x[1])
            self.predictedData.append(x[1])
        # YOU CAN CHANGE NETWORK STRUCTURE AND POOL SETTINGS HERE
        self.network = Network([4, 15, 1])
        self.pool = Population(100, 0.01, 0.4, [-5, 5, 75])
        for x in range(len(self.pool.pool)):
            self.pool.pool[x].gene = self.export['pool'][x]['gene']
            self.pool.pool[x].fitness = float(self.export['pool'][x]['fitness'])
        self.pool.currentGeneration = int(self.export['currentGeneration'])
        self.pool.averageFitness = float(self.export['averageFitness'])
        self.pool.bestDNA.gene = self.export['bestDNAgene']
        self.pool.bestDNA.fitness = float(self.export['bestDNAfitness'])
        inputs = []
        desiredOutputs = []
        for x in range(len(self.data)):
            inputs.append(self.data[x][1:5])
            desiredOutputs.append(self.data[x][5])
        self.calculateGraph()
        self.predictionWindow()

    def exportNetwork(self):
        export = {}
        export['apiConnectionData'] = self.apiConnection.data
        export['pool'] = []
        for x in range(len(self.pool.pool)):
            export['pool'].append({'gene': self.pool.pool[x].gene, 'fitness': self.pool.pool[x].fitness})
        export['currentGeneration'] = self.pool.currentGeneration
        export['averageFitness'] = self.pool.averageFitness
        export['bestDNAgene'] = self.pool.bestDNA.gene
        export['bestDNAfitness'] = self.pool.bestDNA.fitness
        try:
            filen = filedialog.asksaveasfile().name
            f = open(filen, 'w')
            f.write(json.dumps(export))
            f.close()
        except:
            messagebox.showerror("Error", "Something went wrong")

    def calculateGraph(self):
        inputList = []
        self.predictedData = []
        self.network.importWeights(self.pool.bestDNA.gene)
        for x in range(len(self.data)):
            inputList.append([self.data[x][1], self.data[x][2], self.data[x][3], self.data[x][4]])
            self.predictedData.append(self.network.activate(inputList[x]))

MiniProject = App()
MiniProject.run()
