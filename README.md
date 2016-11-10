# MiniProject Hogeschool Utrecht

##Introductie

####Auteur
Alle code is volledig geschreven door **Matthias Krijgsman.**

####Korte Omschrijving
Dit uitgebreide MiniProject is als afsluiting voor de cursus 'Python Programming' op de Hogeschool Utrecht.

De applicatie heeft als doel om van een beurs genoteerd bedrijf, een koers analyse te maken,
om vervolgens een poging te doen om een voorspelling te maken.
</br></br></br>
##Benodigdheden

Python Versie `3.5.4`

Enkele modules die gebruikt zijn:
- Tkinter
- Matplotlib
- Yahoo Finance


```
pip install tkinter
pip install matplotlib
pip install yahoo_finance
```
</br></br></br>

##Gebruikte technieken
####Neural Networks
Dit is een techniek om problemen op te lossen op dezelfde manier als dat een menselijk brein dat doet.
Het probeert patronen te zien in de beurs data die er gegeven wordt
> https://en.wikipedia.org/wiki/Artificial_neural_network

####Genetic Algorithm
Een genetisch algoritme wordt hier gebruikt als optimalisatie techniek voor een Neural Network.
Het werkt op dezelfde manier als de evolutie, en probeert in deze toepassing een Neural Network te maken
die zo goed mogelijk aansluit op de beurs data.
> https://en.wikipedia.org/wiki/Genetic_algorithm

</br></br></br>

##Programmastructuur
De applicatie is opgedeeld in 5 onderdelen, die op elkaar aansluiten. 
Ook worden hier de extra functionaliteiten (Importeren en Exporteren) aangestuurd.

####UI Controller
De UI Controller (class `App`) zorgt voor de User Interface en de gebruikers interactie.
Ook worden hier alle controllers aangestuurd.

####API Controller
De API Controller (class `apiController`) haalt de beursprijzen op van `Yahoo Finance`.

####Data Controller
In de Data Controller (class `dataController`) wordt de data uit de API Controller genormaliseerd zodat 
deze gebruikt kan worden door Neural Network.
Een Neural Network kan namelijk alleen getallen tussen de 0 en de 1 verwerken.

####Genetic Algorithm
Bestaat uit 2 onderdelen.

Het DNA (class `DNA`) houd voor elk Neural Network bij wat zijn 'DNA' is, en test het Neural Network en geeft 
deze een score op basis van hoe goed hij is in het reproduceren van de beurs data.
```
De genen bestaan uit 75 floats tussen de -2.0 en 2.0
De individuele genen zijn de gewichten voor de Neurale Netwerken
```

De populatie (class `Population`) verzorgt het 'natuurlijke selectie' proces. De Neural Networks die de data 
zo slecht mogelijk gereproduceert hebben worden vervangen door combinaties van de best presterende.
```
De Populatie bestaat uit 100 Neural Networks met elk hun eigen DNA
```

####Neural Network
Bestaat uit 3 onderdelen.
De Neuron (class `Neuron`) die een Bias van `+1.0` hebben en een Sigmoid Activation Function.
De Layer (class `Layer`) wordt gebruikt als Hidden of Output Layer, en is niks anders als een verzameling van Neurons.
Het Netwerk (class `Network`) is een geordende verzameling van Layers.

De Neural Networks in deze applicatie hebben de volgende structuur:
```
Input layer: 4 Neurons
Hidden layer: 15 Neurons
Output layer: 1 Neuron
```
</br></br></br>

##Applicatie Flow

Voor de applicatieflow maak ik geen gebruik van PSD's, omdat het dan té groot wordt.
Daarom een meer globale flow:

![alt tag](http://www.matthiaskrijgsman.nl/HUProject/MiniProjectDiagram.png)

</br></br></br>

##Extra functionaliteiten
Een eerder getrainde situatie kan opgeslagen worden, en later worden geïmporteerd.

</br></br></br>

##Afwijkingen van orgineel ontwerp

> Zie orgineel document: Design/Design.docx

De gerealiseerde applicatie heeft een aantal kleine verschillen met het orginele ontwerp.
Zo is er geen Option `Window Controller, Graph Window Controller, en Import/Export Controller`, maar worden deze 
allemaal gehandled door de `App` class

</br></br></br>

##Voorbeeld (Screencast)
[![Screencast](https://img.youtube.com/vi/wRUugPL6Mzw/0.jpg)](https://www.youtube.com/watch?v=wRUugPL6Mzw)
> https://www.youtube.com/watch?v=wRUugPL6Mzw

</br></br></br>

##Zelfreflectie
Ik vond het ontwerpen en realisatie van de applicatie prettig verlopen, daarnaast ben ik ook erg tevreden met het resultaat.
Er is echter zoals altijd wel plaats voor verbetering.
</br></br>
####Verbeterpunten:
- Op voorhand beter onderzoek doen naar de onderwerpen waarmee je te maken krijgt
- Vóór het programmeren eerst een gedetailleerde flow maken zodat duidelijk is hoe de applicatie **exact** moet gaan werken
- Meer tijd besteden aan het optimaliseren van de Algoritmen
</br></br>

####Sterke punten:
- Onderweg relatief weinig problemen tegengekomen
- Weinig bugs, door vaak te testen kom je deze snel tegen
- De problemen/bugs die er waren, creatief opgelost
- Code is relatief netjes geschreven
