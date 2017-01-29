import tkinter as tk
from priorityQueue import PriorityQueue
from adjGraph import Graph
from adjGraph import Vertex
from DFS import DFSGraph
"""Builds an interface using tkinter and assigns the buttons to functions.
    Allows for graphs to be taken from files or input manually, then the user is given the choice of
    of using single-source shortest path or all-pairs shortest path for undirected weighted graphs,
    and topological sort for directed weighted graphs. I ended up having to reset the built
    graph between each call of dijkstra because there was weird things happening that messed up
    the results, but the program should be fine to run over and over without having to start it each time"""

class Application(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        self.pack(anchor='w')
        self.create_widgets()
        root.wm_title("Graph Builder")

        
    def create_widgets(self):
        """Builds the interface"""
        self.selectedGraphArray = ''
        self.selectedGraph = ''
        self.output = tk.Text(self)
        self.currentGraph = tk.Label(self, text='Current Graph: '+'None',fg='blue')
        self.keyboardInput = tk.Button(self, text="Input a graph from the keyboard",command=self.kInput)
        self.fileInput = tk.Button(self, text="Input a graph from a file", command=self.fInput)
        self.singleSource = tk.Button(self, text="Single-source shortest path", command=self.singleShortest)
        self.viewGraph = tk.Button(self, text="View graph",command = self.viewGF)
        self.shortestPath = tk.Button(self, text="All-pairs shortest path", command=self.allShortest)
        self.topo = tk.Button(self, text="Topological sort", command = self.topoSort)
        
        self.currentGraph.pack(side='top',anchor='w')
        self.output.pack(side='right',padx=20,pady=20)
        self.output.see(tk.END)
        self.keyboardInput.pack(side='top',anchor='w')
        self.fileInput.pack(side='top',anchor='w')
        self.viewGraph.pack(side='top',anchor='w')
        self.singleSource.pack(side='top',anchor='w')
        self.shortestPath.pack(side='top',anchor='w')
        self.topo.pack(side='top',anchor='w')
        
        
        self.quit = tk.Button(self, text="QUIT", fg="red",command=root.destroy)
        self.quit.pack(side="top",anchor='w')

    def updateGF(self):
        """Updates what graph is selected and lets the user know."""
        test = self.selectedGraphArray[0]
        if test[1] == '-':
            self.currentGraph['text']='Current Graph: Undirected weighted'
            self.undirectedGraph()
        else:
            self.currentGraph['text']='Current Graph: Directed weighted'
            self.directedGraph()

    def viewGF(self):
        """Gives the user a simple array of what their graph is."""
        self.output.insert(tk.END,'\n'+"Currently selected graph represnted as an array:\n")
        self.output.insert(tk.END,self.selectedGraphArray)
        self.output.insert(tk.END,'\n')

    def singleShortest(self):
        """Asks for which node to start from."""

        if self.currentGraph['text']=='Current Graph: Directed weighted' or self.currentGraph['text'] == "Error: Directed weighted graph only for topological sort.":
            self.currentGraph['text'] = "Error: Directed weighted graph only for topological sort."
        else:
            self.currentGraph['text'] = "Current Graph: Undirected weighted"
            self.inLabel = tk.Label(text="Start node: ")
            self.inEntry = tk.Entry()
            self.bt = tk.Button(text="Done",command = lambda: self.single2(self.selectedGraph,self.inEntry.get()))
            
            self.inLabel.pack(side='top',anchor='w')
            self.inEntry.pack(side='left',anchor='w')
            self.bt.pack(side='left',anchor='w')

    def single2(self,graph,start):
        """Transistion node of the single sort. Calls dijstra and printSingleShort on
        singleShortest's button press."""  
        try:
            self.dijkstra(graph,start)
            self.printSingleShort(start)
            self.undirectedGraph()
        except:
            self.currentGraph['text'] = "Error: Node does not exist."

    def allShortest(self):
        """Runs dijkstra with each node one by one and collects the results in an array."""
        if self.currentGraph['text']=='Current Graph: Directed weighted' or self.currentGraph['text'] == "Error: Directed weighted graph only for topological sort." :
            self.currentGraph['text'] = "Error: Directed weighted graph only for topological sort."
        else:
            self.currentGraph['text'] = "Current Graph: Undirected weighted"
            idArray = []
            allShortArray = []
            display = ''
            
            for item in self.selectedGraphArray:
                if item[0] not in idArray:
                    idArray.append(item[0])
                if item[2] not in idArray:
                    idArray.append(item[2])
            idArray.sort()
            
            for item in idArray:
                self.dijkstra(self.selectedGraph,item)
                self.undirectedGraph()
                count = 0
                for item in self.resultsArray:
                    self.resultsArray[count]=item[1:]
                    count += 1
                allShortArray.append(self.resultsArray)
                del(self.resultsArray)
            self.output.insert(tk.END,'\nAll-pairs shortest path matrix:\n')
            self.output.insert(tk.END,"************************************************\n")
            self.output.insert(tk.END,'   '+'    '.join(idArray))
                
            for i in range(len(idArray)):
                self.output.insert(tk.END,'\n'+idArray[i]+':'+''+', '.join(allShortArray[i])+'\n')
            self.output.insert(tk.END,"************************************************\n")

    def topoSort(self):
        """Runs DFS sort on the graph and prints the results."""
        if self.currentGraph['text']=='Current Graph: Undirected weighted' or self.currentGraph['text'] == "Error: Undirected weighted graph only for Single-source and All-pairs shortest path.":
            self.currentGraph['text'] = "Error: Undirected weighted graph only for Single-source and All-pairs shortest path."
        else:
            self.currentGraph['text'] = "Current Graph: Directed weighted"
            aGraph = self.selectedGraph
            aGraph.dfs()
            self.output.insert(tk.END,'\n'+"Nodes and finish time in shortest to longest order:\n")
            self.output.insert(tk.END,aGraph.topoArray)
            self.output.insert(tk.END,'\n')
        

    def fInput(self):
        """Asks for file name"""
        self.inLabel = tk.Label(text="File name: ")
        self.inEntry = tk.Entry()
        self.bt = tk.Button(text="Done",command = self.fInput2)
        
        self.inLabel.pack(side='top',anchor='w')
        self.inEntry.pack(side='left',anchor='w')
        self.bt.pack(side='left',anchor='w')

        
    def fInput2(self):
        """Takes in file and creates an array from it"""
        try:
            graphArray = []
            file = self.inEntry.get()
            f = open(file,'r')
            for item in f:
                graphArray.append(item.strip('\n'))
                
            self.inLabel.destroy()
            self.inEntry.destroy()
            self.bt.destroy()
            self.currentGraph
            self.selectedGraphArray = graphArray
            self.updateGF()
        except:
            self.currentGraph['text'] = "Error: File not found or formatted correctly."
        
        
    def kInput(self):
        """Asks for the number of entries that will be needed."""
        self.inLabel = tk.Label(text="Number of entries: ")
        self.inEntry = tk.Entry()
        self.bt = tk.Button(text="Done",command = self.kInput2)
        
        self.inLabel.pack(side='top',anchor='w')
        self.inEntry.pack(side='left',anchor='w')
        self.bt.pack(side='left',anchor='w')

        
    def kInput2(self):
        """Creates entry boxes for the number of entries that are wanted"""
        try:
            entries = int(self.inEntry.get())
            entriesArray = []
            prompt = tk.Label(self, text="Enter edges and lengths of format \"A-B: 30\", or \"A>B: 30\": ")
            prompt.pack(side='top',anchor='w')
            for n in range(entries):
                entriesArray.append('entry'+str(n))
            for n in range(entries):
                 entriesArray[n] = tk.Entry(self)
                 entriesArray[n].pack(side='top',anchor='w')
            self.inLabel.destroy()
            self.inEntry.destroy()
            self.bt.destroy()
            self.bt = tk.Button(text="Done",command = lambda: self.kInput3(entries,entriesArray,prompt))
            self.bt.pack(side='top',anchor='w')
        except:
            self.currentGraph['text'] = "Error: Only integers accepted."
        
    
    def kInput3(self,n,array,p):
        """Collects inputs from entry boxes"""
        try:
            graphArray = []
            for i in range(n):
                graphArray.append(array[i].get())
            for i in range(n):
                array[i].destroy()
            p.destroy()
            self.bt.destroy()
            self.selectedGraphArray = graphArray
            self.updateGF()
        except:
            self.currentGraph['text'] = "Error: Format not correct, please try again."

        
    def undirectedGraph(self):
        """For undirected Graphs creates a graph with edges going back and forth from each node"""
        unGraph = Graph()
        for item in self.selectedGraphArray:
            if item[0] not in unGraph.vertices:
                unGraph.addVertex(item[0])
            if item[2] not in unGraph.vertices:
                unGraph.addVertex(item[2])
        for item in self.selectedGraphArray:
            unGraph.addEdge(item[0],item[2],int(item[4:]))
            unGraph.addEdge(item[2],item[0],int(item[4:]))
        self.selectedGraph = unGraph


    def directedGraph(self):
        """For directed Graphs only creates edges one way"""
        drGraph = DFSGraph()
        for item in self.selectedGraphArray:
            if item[0] not in drGraph.vertices:
                drGraph.addVertex(item[0])
            if item[2] not in drGraph.vertices:
                drGraph.addVertex(item[2])
        for item in self.selectedGraphArray:
            drGraph.addEdge(item[0],item[2],int(item[4:]))
        self.selectedGraph = drGraph
        

    def printSingleShort(self,start):
        """prints the results from the single-source shortest path algorithm"""
        self.output.insert(tk.END,"\nThe shortest paths from vertex "+start+" are:\n")
        self.output.insert(tk.END,"************************\n")
        self.output.insert(tk.END,"  Vertex     Distance   \n")
        for item in self.resultsArray:
            self.output.insert(tk.END,"    "+item[0]+"          "+item[1:]+'\n')
        self.output.insert(tk.END,"************************\n")
        
    def dijkstra(self,aGraph,starting):
        """Dijkstra algorithm that is used for singe cource and all pairs"""
        tempG = self.selectedGraph
        self.resultsArray = []
        testArray = []
        start = self.selectedGraph.vertices[starting]
        temp = start.getDistance()
        pq = PriorityQueue()
        start.setDistance(0)
        pq.buildHeap([(v.getDistance(),v) for v in aGraph])
        while not pq.isEmpty():
            currentVert = pq.delMin()
            for nextVert in currentVert.getConnections():
                newDist = currentVert.getDistance() \
                        + currentVert.getWeight(nextVert)
                if newDist < nextVert.getDistance():
                    nextVert.setDistance( newDist )
                    nextVert.setPred(currentVert)
                    pq.decreaseKey(nextVert,newDist)
                if nextVert.getId() not in testArray:
                    testArray.append(nextVert.getId())
                    self.resultsArray.append(nextVert.getId()+' '+str(nextVert.getDistance()))
        self.selectedGraph.vertices[starting].setDistance(temp)
        self.selectedGraph = tempG
        self.resultsArray.sort()
        self.inLabel.destroy()
        self.inEntry.destroy()
        self.bt.destroy()
        
      

root = tk.Tk()
Application(root)
root.mainloop()
