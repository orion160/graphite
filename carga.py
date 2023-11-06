import sys


def main():
    
    linea = sys.stdin.readline() 
    
    for caso in range(int(linea)):
        
        linea = sys.stdin.readline()
        
        datos = linea.split()
        
        M = int(datos[0])
        N = int(datos[1])
        k = int(datos[2])

        #diccionario con las coordenadas del mínimo rectángulo de cada llave. Cada valor de cada llave es una lista con [min_x,min_y,max_x,max_y]
        
        dic = {}
        
        #recorremos la matriz

        for i in range(M):
            
            linea = sys.stdin.readline()
            llaves = linea.split()
            
            for j in range(N):
                
                llave = int(llaves[j])
                
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
                
main()