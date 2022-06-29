
import random
import sys
import time
from graph import Graph


def add_frontier(frontier,city):
    i=0
    h= city[2]
    g = city[3]
    f = h + g

    if len(frontier)==0:
        frontier.append(city)
        return frontier
    for elt in frontier:

        if f < elt[2] + elt[3]:
            frontier.insert(i,city)
            return(frontier)
        if f == elt[2] + elt[3] :
            if h<elt[2] :
                frontier.insert(i,city)
                return(frontier)
            if h == elt[2] :
                frontier.insert(i,city)
                return(frontier)
        i+=1

    if city not in frontier:
        frontier.append(city)
        return (frontier)

def Astar(G, start):
    starter = time.time()
    new_visited = []
    numVertices = len(G.adjMatrix[0])
    frontier = [[start, [], mst(G), 0]]
    taille_max_frontier=len(frontier)
    explored = []
    current_city = start
    h = mst(G)
    g = frontier[0][3]
    cpt=0
    while len(frontier[0][1]) != numVertices +1:

        #print("Nous sommes à la", cpt,"ème itération(s) voici la frontière : ",frontier)
        frontier.pop(0)
        for i in range(numVertices):
            if len(new_visited) == numVertices - 1 and i == current_city and i not in new_visited:
                new_city = i
                new_visited = explored + [current_city] + [start]
                g = g + G.adjMatrix[start][current_city]
                frontier = add_frontier(frontier, [new_city, new_visited, 0, g])
                break
            if i in explored+[current_city]:
                continue
            if len(new_visited) == numVertices - 1 :
                h = G.adjMatrix[current_city][i]

            elif len(new_visited) == numVertices:
                h=0
            else:
                sub = subgraph(G, explored)
                h = mst(sub)
            new_city = i
            new_visited = explored + [current_city]
            value = g + G.adjMatrix[current_city][i]
            frontier = add_frontier(frontier, [new_city, new_visited, h, value])
        if len(frontier) > taille_max_frontier:
            taille_max_frontier = len(frontier)
        [current_city, explored, h, g] = frontier[0]
        cpt+=1
    ending = time.time()
    timee = ending - starter
    print("astar runs in : ", round(timee,2), "s")

    return (explored, g, taille_max_frontier)








#Cette fonction permet de générer une premier chemin hamiltonien de manière aléatoire

def randomSolution(g):
    cities = list(range(len(g)))
    solution = []
    for i in range(len(g)):
        randomCity = cities[random.randint(0,len(cities)-1)]
        solution.append(randomCity)
        cities.remove(randomCity)
    solution.append(solution[0])
    return solution

#Permet de récupérer la valeur de mon chemin hamiltonien choisi
def routeLength(g,solution):
    length = 0
    count = 0
    i = 0
    while ( count <len(solution)-1):
        length = length + g[solution[i]][solution[i+1]]
        i = i + 1
        count = count + 1
    return length

#Permet de recupérer
def getNeighbors(g,solution):
    best = solution
    amelioration = True
    getNeigh = []
    getNeigh.append(solution)

    while(amelioration):
        #print("on entre dans la boucle")
        amelioration = False
        for i in range(1,len(solution)-2):
                for j in range(i+1,len(solution)):
                    if j-i == 1 : continue
                    new_solution = solution[:]
                    new_solution[i:j]=solution[j-1:i-1:-1]
                    getNeigh.append(new_solution)

                    if routeLength(g,new_solution)<routeLength(g,best):
                        best = new_solution
                        amelioration = True

        solution = best
        resultantNeigh = []

        for element in getNeigh:
            if element not in resultantNeigh:
                resultantNeigh.append(element)
        resultantNeigh.pop(0)
    return best,resultantNeigh


#Permet de calculer le taux d'amélioration, le taux initial correspond au poids de mon chemin initial,
#et le taux final correspond au poids de mon chemin final obtenue.
def taux(t_initial,t_final):
    taux = ((t_initial - t_final)/t_initial)*100
    return taux

def hillclimbing(g):
    start = time.time()
    currentSolution = randomSolution(g.adjMatrix) #A partir de notre graphe, on récupère un premier chemin hamiltonien

    print("\n\nNotre chemin initial, choisi de manière aléatoire, est le suivant : ",currentSolution,"\n")

    currentRouteLenght = routeLength(g.adjMatrix, currentSolution)   #

    print("Initiallement, notre chemin initial a un coût de :",currentRouteLenght,".En partant de la ville ", currentSolution[0],"notre objectif est de trouver le chemin le plus intéressant en terme de coût. \nNous allons utiliser pour cela l'algorithme de hillClimbing afin d'améliorer ce coût.")

    taux_initial = currentRouteLenght

    bestNeigh,neighbours = getNeighbors(g.adjMatrix,currentSolution)
    bestLenght = routeLength(g.adjMatrix,bestNeigh)


    while(bestLenght<currentRouteLenght):
        currentSolution = bestNeigh
        currentRouteLenght= bestLenght
        bestNeigh,neighbours = getNeighbors(g.adjMatrix,currentSolution)
        bestLenght=routeLength(g.adjMatrix,bestNeigh)

    print("Apres exécution de l'algorithme, la chemin le plus intéressant pour résoudre notre problème est le suivant :",currentSolution,)
    print("\nNotre nouveau chemin se parcourt avec le coût suivant : ",currentRouteLenght)
    taux_final = currentRouteLenght
    print("Voici nos valeurs pour calculer le taux d'amélioration,avec respectivement le taux initial et le taux final : ",taux_initial,"et",taux_final)
    taux_sol = taux(taux_initial,taux_final)
    end = time.time()
    print("Le taux d'amélioration est de ",round(taux_sol,2),"%")
    print("Le temps d'exécution est de :",round(end-start,4),"secondes.\n")

    return currentSolution,currentRouteLenght,taux_sol


def subgraph(g,l):

    n = len(g.getVertices())
    taille = n - len(l)
    G = Graph(taille, directed=directed)
    t = g.getVertices()

    k = 0
    p = 0

    if(len(l)==n):
        raise "Liste complète, le graphe vaut 0"


    for i in l:
        if i in t:
            t.remove(i)

    for i in t:
        G.addVertex(i)

    for i in t:
        if(k<len(t)):
            for j in t :
                if(p<len(t)):
                    G.adjMatrix[k][p] =  g.adjMatrix[i][j]
                    G.adjMatrix[p][k] =  g.adjMatrix[j][i]
                    G.adjMatrix[k][k] =  0
                    p +=1
            k+=1
            p = 0

    return G

def mst(g):

    numVertices = len(g.getVertices())
    visited = [0]* numVertices
    edgeNum = 0
    visited[0] = True
    nodes_un = []
    nodes_deux = []


    while(edgeNum<numVertices-1):
        min = sys.maxsize

        for i in range(numVertices):
                if visited[i]:
                    for j in range(numVertices):
                            if((not visited[j]) and g.adjMatrix[i][j]):

                                if min>g.adjMatrix[i][j]:
                                    min = g.adjMatrix[i][j]

                                    s = i
                                    d = j


        nodes_un.append(s)
        nodes_deux.append(d)

        nodes_tuple = list(zip(nodes_un,nodes_deux))


        visited[d]=True
        edgeNum +=1
    nodes = list(nodes_tuple)
    weight = []
    for i in range(len(nodes)):
            weight.append(g.adjMatrix[nodes[i][0]][nodes[i][1]])
    total_weight = sum(weight)

    return total_weight
 

def generate(n):
    G = Graph(n, directed=directed)
    for i in range(0,n):
        G.addVertex(i)
    for i in range(0,n-1):
        for j in range(i+1,n):
            print("Quelle est la valeur entre la ville",i,"et la ville",j,"?")
            distance = input()
            G.adjMatrix[i][j] = int(distance)
            G.adjMatrix[j][i] = int(distance)
            G.adjMatrix[i][i] = 0

    return G

def generate_random(n_villes,n_distance):
    G = Graph(n_villes,directed = directed)
    for i in range(0,n_villes):
        G.addVertex(i)

    for i in range(0,n_villes-1):
        for j in range(i+1,n_villes):
            distance = random.randint(1,n_distance)
            print("La distance entre la ville",i,'et la ville',j,'a été initialisée à :',distance)
            G.adjMatrix[i][j] = int(distance)
            G.adjMatrix[j][i] = int(distance)
            G.adjMatrix[i][i] = 0
    return G



def initialise_graph():
    print("Bonjour.Choisissez la manière d'initialiser votre graphe :\n\n"
          "1)Initialiser de manière aléatoire (en entrant le nombre de villes et la distance maximum).\n"
          "2)Initalisation manuelle (en entrant le nombre de villes et la distance parcourue chaque ville).\n")
    choix = input()

    if choix != "1" and choix != "2":
        while (choix != "1" and choix != "2"):
            print("Entrée incorrecte."
                  "Choisissez la manière d'initialiser votre graphe :\n"
                  "1)Initialiser de manière aléatoire (en entrant nombre de villes et distance maximum).\n"
                  "2)Initalisation manuelle (en entrant le nombre de villes et la distance parcourue chaque ville).\n")
            choix = input()
    if choix == "2":
        print("Vous avez choisi une initialisation manuelle.")
        print("Combien de ville souhaitez vous saisir?")
        n = int(input())
        G = generate(n)
        print("\nVoici la matrice présentant les coûts entre chaque ville")
        G.printMatrix()
    else:
        print("Vous avez choisi une initialisation aléatoire.")
        print("Combien de villes souhaitez vous entrer?")
        n = int(input())
        print("Quelle distance souhaitez maximum initialiser entre deux villes?")
        dist = int(input())
        G = generate_random(n, dist)
        print("\nVoici la matrice présentant les coûts entre chaque ville")
        G.printMatrix()
    return G,n



if __name__== '__main__':
    #for directed in [False,True]:

        directed = True
        G,n= initialise_graph()


        print("\n\nIl reste à choisir quelle recherche effectuer.Faites un choix : \n"
              "1)Recherche informée (avec utilisation de A*).\n"
              "2)Recherche locale (avec utilisation de HillClimbing).\n")
        algo = input()

        if (algo!="1" and algo!="2"):
            while(algo!="1" and algo!="2"):
                print("Saisie incorrecte. Refaites un choix:\n"
                      "1)Recherche informée (avec utilisation de A*).\n"
                      "2)Recherche locale (avec utilisation de HillClimbing).\n")
                algo = input()
        if(algo == "1"):
            print("De quelle ville souhaitez vous partir? Choisissez une ville entre 0 et ",n-1,".")
            start = int(input())
            if (start>=n or start < 0):
                while(start>=n or start<0):
                    print("Choisissez une ville entre 0 et",n-1,".")
                    start = int(input())

            astar_path = Astar(G, start)
            print("Le chemin le plus court est :", astar_path[0])
            print("Le cout du chemin est :", astar_path[1])
            print("La taille maximale de la frontière est de :", astar_path[2])
        else :
            "Vous avez choisi la recherche locale. \n\n"
            res1, res2, taux = hillclimbing(G)







