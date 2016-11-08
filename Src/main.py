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
        mainloop()

    def optionWindow(self):
        self.root.title("MiniProject | Stock Exchange Predictor")
        self.clearView()

        optionGroup = LabelFrame(self.appView, text="Options", padx=5, pady=5)

        symbolLabel = Label(optionGroup, text="Ticker Symbol: ")
        dataDaysLabel = Label(optionGroup, text="Number of days: ")
        orLabel = Label(optionGroup, text="or")

        self.symbolInput = Entry(optionGroup)
        self.dataDaysInput = Entry(optionGroup)

        importButton = Button(optionGroup, text="Import Existing", command=self.selectImportFile)
        createButton = Button(optionGroup, text="Create", command=self.loadData)

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

        apiConnection = apiController()
        apiConnection.getData(self.symbolInput.get(), self.dataDaysInput.get())



        dataCon = dataController(apiConnection.data)
        self.data = dataCon.parseData()

        #Data
        self.data.reverse()

        self.actualData = []
        self.predictedData = []

        #todo: Normalise Data and initialize Pool with NN's

        for x in self.data:
            self.actualData.append(x[1])
            self.predictedData.append(x[1])

        self.network = Network([4, 10, 5, 1])

        self.calculateGraph()

        self.predictionWindow()


    def predictionWindow(self):
        self.root.title("MiniProject | Stock Exchange Predictor")
        self.clearView()

        neuralGroup = LabelFrame(self.appView, text="Neural Network", padx=5, pady=5)
        actionGroup = LabelFrame(self.appView, text="Info & Actions", padx=5, pady=5)

        neuralGroup.grid(sticky=W)
        actionGroup.grid(sticky=E)

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot(self.actualData)
        a.plot(self.predictedData)

        canvas = FigureCanvasTkAgg(f, neuralGroup)
        canvas.show()
        canvas.get_tk_widget().pack(expand=True)

        self.appView.pack(padx=10, pady=10)

    def selectImportFile(self):
        print(filedialog.askopenfilename())

    def importNetwork(self):
        pass

    def exportNetwork(self):
        pass

    def calculateGraph(self):
        inputList = []
        self.predictedData = []
        for x in range(len(self.data)):
            inputList.append([self.data[x][1], self.data[x][2], self.data[x][3], self.data[x][4]])
            self.predictedData.append(self.network.activate(inputList[x]))



MiniProject = App()
MiniProject.run()
