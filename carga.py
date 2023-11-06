
# First networkx library is imported  
# along with matplotlib 
import networkx as nx 
import matplotlib.pyplot as plt 
import sys

# Defining a Class 
class GraphVisualization: 
   
    def __init__(self, caso): 
          
        # visual is a list which stores all  
        # the set of edges that constitutes a 
        # graph 
        self.visual = [] 
        self.caso = caso
          
    # addEdge function inputs the vertices of an 
    # edge and appends it to the visual list 
    def addEdge(self, a, b):
        temp = [a, b] 
        self.visual.append(temp) 
          
    # In visualize function G is an object of 
    # class Graph given by networkx G.add_edges_from(visual) 
    # creates a graph with a given list 
    # nx.draw_networkx(G) - plots the graph 
    # plt.show() - displays the graph 
    def visualize(self): 
        G = nx.DiGraph() 
        G.add_edges_from(self.visual)
        plt.figure(self.caso) 
        nx.draw_networkx(G, arrows=True)
        plt.savefig('graph'+str(self.caso)+'.png')
        #plt.show() 

def main():
    
    linea = sys.stdin.readline() 
    
    for caso in range(int(linea)):
        
        linea = sys.stdin.readline()
        
        datos = linea.split()
        
        M = int(datos[0])
        N = int(datos[1])
        k = int(datos[2])

        # la matriz

        matriz = [[0 for _ in range(N)] for _ in range(M)]
        #diccionario con las coordenadas del mínimo rectángulo de cada llave. Cada valor de cada llave es una lista con [min_x,min_y,max_x,max_y]
        
        dic = {}
        
        #recorremos la matriz

        for i in range(M):
            
            linea = sys.stdin.readline()
            llaves = linea.split()
            
            for j in range(N):
                
                llave = int(llaves[j])
                
                # vamos llenamos la matriz
                matriz[i][j] = llave
                
                # Si la llave es nueva, la agregamos al diccionario

                if llave not in dic:
                    #min_y no se vuelve a modificar
                    dic[llave] = [j,i,j,i]
                
                # Si no es nueva actualizamos 
                else:
                    
                    coordenadas = dic[llave]
                    
                    #actualizar min_x
                    if coordenadas[0] > j:
                        coordenadas[0] = j
                    
                    #min_y no se vuelve a modificar

                    #actualizar max_x
                    if coordenadas[2] < j:
                        coordenadas[2] = j
                    
                    #actualizar max_y, siempre se actualiza
                    coordenadas[3] = i

                    dic[llave] = coordenadas
            
        
        """ print("**** CASO " + str(caso) + " ****")
        
        for llavei in range(1,k+1):

            print("\nllave = " + str(llavei))
            print("min_x = " + str(dic[llavei][0]))
            print("min_y = " + str(dic[llavei][1]))
            print("max_x = " + str(dic[llavei][2]))
            print("max_y = " + str(dic[llavei][3]))
            print("-----------------\n") """
        
        G = GraphVisualization(caso) 
        
        for llave in range(1,k+1):
            
            hijos = set()
            for row in range(dic[llave][1],dic[llave][3]+1):
                for col in range(dic[llave][0],dic[llave][2]+1):
                    hijos.add(matriz[row][col])
            
            hijos.remove(llave)
            
            for hijo in hijos:
                G.addEdge(llave, hijo) 
                
        G.visualize() 



                
main()