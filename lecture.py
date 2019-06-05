import numpy as np
import random as rd
import copy as cp
import operator as op
import math as m


########################################
#Permet la lecture du document en entree, renvoie : 
#dico : toutes les infos pour chaque zone a evacuer
#graph : infos du graphe avec les capacites des arcs, longeurs,...
#evac node : listes des noeuds des zones a evacuer
#liste edge : liste de tous les arcs 
def file_read(filename):
    f = open(filename, 'r')
    f.readline()

    line = f.readline()
    (nb_evac_node, id_safe_node) = line.split(' ')
    nb_evac_node = int(nb_evac_node)
    id_safe_node = int(id_safe_node)

    dico = {}
    liste_evac_node = []

    for i in range(nb_evac_node):
        struct = {}
        line = f.readline().split(' ')
    
        struct["id"] = int(line[0])
        struct["pop"] = int(line[1])
        struct["max_rate"] = int(line[2])
        struct["k"] = int(line[3])
        struct["v"] = list(np.int_(line[4:]))
    
        liste_evac_node.append(int(line[0]))
        dico[int(line[0])] = struct

    f.readline()



    (nb_node, nb_edge) = f.readline().split(' ')
    nb_node = int(nb_node)
    nb_edge = int(nb_edge)


    graph = {}
    liste_edge = []

    for i in range(nb_edge):
        struct = {}
        line = f.readline().split(' ')
    
        struct["n1"] = int(line[0])
        struct["n2"] = int(line[1])
        struct["duedate"] = int(line[2])
        struct["length"] = int(float(line[3])) #+ 1
        struct["capacity"] = int(float(line[4]))
    
        liste_edge.append([int(line[0]),int(line[1])])
        graph[(int(line[0]),int(line[1]))] = struct



    f.close()
    return (dico, graph, liste_evac_node, liste_edge)
########################################


########################################
#Permet de lire un fichier solution, renvoie :
#dico_soluce : pour chaque zone a evacuer, 
#   l'id de la zone de depart
#   le taux d'evac
#   la date de debut
#liste_evac_node_soluce : id des zones de depart
def soluce(filename):
    f = open(filename, 'r')

    nom_inst_soluce = f.readline()
    nb_evac_node_soluce = int(f.readline())

    dico_soluce = {}
    liste_evac_node_soluce = []

    for i in range(nb_evac_node_soluce):
        struct = {}
        line = f.readline().split(' ')
    
    
        struct["id"] = int(line[0])
        struct["taux_evac"] = int(line[1])
        struct["date_debut"] = int(line[2])
    
        liste_evac_node_soluce.append(int(line[0]))
        dico_soluce[int(line[0])] = struct

    valid =  f.readline()
    val_fct_obj =  int(f.readline())
    temps_calc =  float(f.readline())
    methode =  f.readline()
    champ_libre =  f.readline()
    
    dico_soluce["valid"] = valid
    dico_soluce["val_fct_obj"] = val_fct_obj
    dico_soluce["temps_calc"] = temps_calc
    dico_soluce["methode"] = methode
    dico_soluce["champ_libre"] = champ_libre

    return (dico_soluce,liste_evac_node_soluce)
########################################

########################################
#
def getFlow(L,date):
    if date<(L[2]):
        return 0
    elif date>(L[2]+L[1]-1):
        return 0
    else:
        return L[3]
########################################


########################################
def verif2(dico_soluce,dico,graph,liste_evac_node,liste_edge):  
    objectif_value = dico_soluce["val_fct_obj"]
    edgesData = {}
    for t in range(objectif_value):
        struct = {}
        for e in graph:
            struct[e] = graph[e]["capacity"]
        edgesData[t] = struct

    tmax = 0    
    for aNode in dico:
        aNode = dico[aNode]
        tInit = dico_soluce[aNode["id"]]["date_debut"]
        remainPeople = aNode["pop"]
        
        while(remainPeople>0):
            t=tInit
            a_tmp = aNode["id"]
            for e in aNode["v"]:
                b_tmp = e
                if (t>objectif_value):  
                    print("error above obj fct")
                    return False
                if((a_tmp,b_tmp) in edgesData[t]):
                    edgesData[t][(a_tmp,b_tmp)] = edgesData[t][(a_tmp,b_tmp)] - dico_soluce[aNode["id"]]["taux_evac"]
                    if (edgesData[t][(a_tmp,b_tmp)] < 0):
                        print("error above capacity")
                        return False
                    t = t + graph[a_tmp,b_tmp]["length"]
                elif((b_tmp,a_tmp) in edgesData[t]):
                    edgesData[t][(b_tmp,a_tmp)] = edgesData[t][(b_tmp,a_tmp)] - dico_soluce[aNode["id"]]["taux_evac"]
                    if (edgesData[t][(b_tmp,a_tmp)] < 0):
                        print("error above capacity")
                        return False
                    t = t + graph[b_tmp,a_tmp]["length"]
                #print("id: " + str(aNode["id"]) + " arc: " + str(a_tmp) + "-" + str(b_tmp) + " t: " + str(t))
    

                if(t>tmax):
                    tmax = t

                a_tmp = b_tmp
            remainPeople = remainPeople - dico_soluce[aNode["id"]]["taux_evac"]
            tInit = tInit+1


    #print("tmax: " + str(tmax+1) + " fct_val: " + str(objectif_value))
    if((tmax+1) == objectif_value):
        return True
    else:
        print("error obj fct does not match")
        return False

########################################    

def borne_inf(dico,graph):  #Comme si tout le monde partait en meme sans qu'il y ait de probleme sur les arcs
    maxe = 0
    
    for E in dico:
        somme = m.ceil(dico[E]["pop"] / dico[E]["max_rate"])
        for j in range(dico[E]["k"]):
            if j == 0:
                a_tmp = dico[E]["id"]   #L ordre des noeuds d un arc peut etre inverse il faut tester les deux possibilites
                b_tmp = dico[E]["v"][j]
                if (a_tmp,b_tmp) in graph:
                    somme += graph[(a_tmp,b_tmp)]["length"]
                else:
                    somme += graph[(b_tmp,a_tmp)]["length"]
            else:
                a_tmp = dico[E]["v"][j-1]   
                b_tmp = dico[E]["v"][j]
                if (a_tmp,b_tmp) in graph:
                    somme += graph[(a_tmp,b_tmp)]["length"]
                else:
                    somme += graph[(b_tmp,a_tmp)]["length"]
        if somme > maxe :
            maxe = somme
    return maxe

def borne_sup(dico,graph):  #Les zones s'evacuent les unes apres les autres, une zone commencant seulement quand la precedente a termine
    maxe = 0
    
    for E in dico:
        somme = m.ceil(dico[E]["pop"] / dico[E]["max_rate"])
        for j in range(dico[E]["k"]):
            if j == 0:
                a_tmp = dico[E]["id"]   #L ordre des noeuds d un arc peut etre inverse il faut tester les deux possibilites
                b_tmp = dico[E]["v"][j]
                if (a_tmp,b_tmp) in graph:
                    somme += graph[(a_tmp,b_tmp)]["length"]
                else:
                    somme += graph[(b_tmp,a_tmp)]["length"]
            else:
                a_tmp = dico[E]["v"][j-1]   
                b_tmp = dico[E]["v"][j]
                if (a_tmp,b_tmp) in graph:
                    somme += graph[(a_tmp,b_tmp)]["length"]
                else:
                    somme += graph[(b_tmp,a_tmp)]["length"]
        maxe += somme
    return maxe

##############################
#Recherche locale - Intensification
def intensification(liste_evac_node,dico,graph,liste_edge,input_file):
    print("intensification")
    #Mise a jour des max rates
    #max rate du secteur = rate min de son chemin d'evacuation
    for cle in dico:
        max_rate = dico[cle]["max_rate"]
        for j in range(dico[cle]["k"]):
            if j == 0:
                a_tmp = dico[cle]["id"] #L ordre des noeuds d un arc peut etre inverse il faut tester les deux possibilites
                b_tmp = dico[cle]["v"][j]
                if (a_tmp,b_tmp) in graph:
                    if graph[(a_tmp,b_tmp)]["capacity"] < max_rate:
                        max_rate = graph[(a_tmp,b_tmp)]["capacity"]
                else:
                    if graph[(b_tmp,a_tmp)]["capacity"] < max_rate:
                        max_rate = graph[(b_tmp,a_tmp)]["capacity"]
            else:
                a_tmp = dico[cle]["v"][j-1] 
                b_tmp = dico[cle]["v"][j]
                if (a_tmp,b_tmp) in graph:
                    if graph[(a_tmp,b_tmp)]["capacity"] < max_rate:
                        max_rate = graph[(a_tmp,b_tmp)]["capacity"]
                else:
                    if graph[(b_tmp,a_tmp)]["capacity"] < max_rate:
                        max_rate = graph[(b_tmp,a_tmp)]["capacity"]
        dico[cle]["max_rate"] = max_rate

    sol = []
    maxe = 0

    for E in dico:
        sol.append([dico[E]["id"],dico[E]["k"],dico[E]["max_rate"]])
    #on trie pour mettre en 1er dans la liste de solution le noeud qui a le chemin d'evacuation le plus proche de la fin
    sol = sorted(sol,key=op.itemgetter(1))

    for i in sol:
        E = i[0]
        i[1] = maxe
        somme = m.ceil(dico[E]["pop"] / dico[E]["max_rate"])
        
        for j in range(dico[E]["k"]):
            if j == 0:
                a_tmp = dico[E]["id"]   #L ordre des noeuds d un arc peut etre inverse il faut tester les deux possibilites
                b_tmp = dico[E]["v"][j]
                if (a_tmp,b_tmp) in graph:
                    somme += graph[(a_tmp,b_tmp)]["length"]
                else:
                    somme += graph[(b_tmp,a_tmp)]["length"]
            else:
                a_tmp = dico[E]["v"][j-1]   
                b_tmp = dico[E]["v"][j]
                if (a_tmp,b_tmp) in graph:
                    somme += graph[(a_tmp,b_tmp)]["length"]
                else:
                    somme += graph[(b_tmp,a_tmp)]["length"]
        maxe+=somme

    print(sol)
    (val,ok) = fonc_eval_rate(sol,dico,graph,liste_evac_node,liste_edge)
    print(ok)
    print(val)

    for i in range(len(sol)):
        (val,ok) = fonc_eval_rate(sol,dico,graph,liste_evac_node,liste_edge)
        while (sol[i][1] > 0 and ok == True):
            #print(sol)
            sol_tmp = cp.deepcopy(sol)
            sol_tmp[i][1] = int(sol_tmp[i][1] /2)
            (val,ok) = fonc_eval_rate(sol_tmp,dico,graph,liste_evac_node,liste_edge)
            if (ok == True):
                sol = cp.deepcopy(sol_tmp)

        (val,ok) = fonc_eval_rate(sol,dico,graph,liste_evac_node,liste_edge)
        while (sol[i][1] > 0 and ok == True):
            #print(sol)
            sol_tmp = cp.deepcopy(sol)
            sol_tmp[i][1] = sol_tmp[i][1] -1
            (val,ok) = fonc_eval_rate(sol_tmp,dico,graph,liste_evac_node,liste_edge)
            if (ok == True):
                sol = cp.deepcopy(sol_tmp)

    write_sol(sol)
    
    return sol  
        
def write_sol(sol):
    #print into out.txt
    f = open("out.txt", 'w')
    f.write(input_file + "\n")
    f.write(str(len(sol)) + "\n")
    z = 0
    for s in sol:
        f.write(str(s[0]) + " " + str(s[2]) + " " + str(s[1]) + "\n")
    (val,ok) = fonc_eval_rate(sol,dico,graph,liste_evac_node,liste_edge)
    if(ok==True):
        f.write("valid" + "\n")
        print("Solution VALID")
    else:
        f.write("invalid" + "\n")
        print("Solution INVALID")
    print("Val fonc obj: " + str(val))
    f.write(str(val) + "\n")
    f.write("1000" + "\n")
    f.write("resolu par intensification" + "\n")
    f.write("no comment" + "\n")
    f.close()

def doable(sol,dico,graph,liste_evac_node,liste_edge):
    for i in range(len(sol)):
        if (dico[sol[i][0]]["max_rate"]<sol[i][2]):
                        return 0
        if (sol[i][1]<0):
            return 0
        if (sol[i][2]<=0):
            return 0
    if(fonc_eval_rate(sol,dico,graph,liste_evac_node,liste_edge)[1] != True):
        return 0
    return 1

#Fonction d'evaluation avec rate d'evac pris en compte
#Retourne un tuple contenant la valeur de la fonc objectif
#et un boolean disant si la solution est valide
#sol: [[id,date_depart,rate],...]
def fonc_eval_rate(sol,dico,graph,liste_evac_node,liste_edge):
    longest_node = 0
    longest_node_time= 0
    dico_soluce_tmp = {}
    #set dico soluce    
    for i in range(len(sol)):
        dico_soluce_tmp[sol[i][0]] = {"id" : sol[i][0],"taux_evac" : sol[i][2], "date_debut" : sol[i][1]}
            
        time = sol[i][1] + m.ceil(dico[sol[i][0]]["pop"] / sol[i][2])
        a_tmp = sol[i][0]
        for b_tmp in dico[sol[i][0]]["v"]:
            if((a_tmp,b_tmp) in graph):
                time+= graph[(a_tmp,b_tmp)]["length"]
            if((b_tmp,a_tmp) in graph):
                time+= graph[(b_tmp,a_tmp)]["length"]       
            a_tmp = b_tmp
        if(time>longest_node_time):
            longest_node_time = time
            longest_node = sol[i][0]

    dico_soluce_tmp["val_fct_obj"] = longest_node_time
    sol_ok = verif2(dico_soluce_tmp,dico,graph,liste_evac_node,liste_edge)
    return (dico_soluce_tmp["val_fct_obj"],sol_ok)

def rand_sol(i):
    l = [-1, 1]
    m = rd.choice(l)
    n = rd.randint(0,i)
    k = rd.randint(1,2)
    #k=1
    
    return (n,k,m)

def voisin_random(solu,dico,graph,liste_evac_node,liste_edge):
    i = len(solu)
    n,k,m = rand_sol(i)

    sol_random = cp.deepcopy(solu)
    sol_random[n-1][k] = sol_random[n-1][k] + m
    while(doable(sol_random,dico,graph,liste_evac_node,liste_edge)!= 1):
        n,k,m = rand_sol(i)
        sol_random = cp.deepcopy(solu)
        sol_random[n-1][k] = sol_random[n-1][k] + m
    return sol_random
    
#Diversification par recuit simule
def diversification(sol_initiale,temp_initiale,liste_evac_node,dico,graph):
    s = cp.deepcopy(sol_initiale)
    T = temp_initiale
    k = 0.99
    
    while(T>0.000000000001):
        print("T: " + str(T))
        random = rd.uniform(0.0,1.0)
        s_prime = voisin_random(s,dico,graph,liste_evac_node,liste_edge)
        deltaf = fonc_eval_rate(s_prime,dico,graph,liste_evac_node,liste_edge)[0] - fonc_eval_rate(s,dico,graph,liste_evac_node,liste_edge)[0]
        if((deltaf<0) or (random<np.exp(-deltaf/T))):
            s = cp.deepcopy(s_prime)
        T = k*T
    write_sol(s)
    return s
##############################

input_file = "exemple.txt"
#input_file = "sparse_10_30_3_1_I.full"

(dico, graph, liste_evac_node, liste_edge) = file_read(input_file)

sol_intens = intensification(liste_evac_node,dico,graph,liste_edge,input_file)
sol_diver = diversification(sol_intens,5000,liste_evac_node,dico,graph)

(dico_soluce,liste_evac_node_soluce) = soluce("out.txt")
#(dico_soluce,liste_evac_node_soluce) = soluce("soluce.txt")
resultat = verif2(dico_soluce,dico,graph,liste_evac_node,liste_edge)

print("MIN: ", borne_inf(dico,graph))
print("MAX: ", borne_sup(dico,graph))

print("intens = " ,sol_intens," val_fct_obj = ",fonc_eval_rate(sol_intens,dico,graph,liste_evac_node,liste_edge)[0])
print("divers = " ,sol_diver," val_fct_obj = ",fonc_eval_rate(sol_diver,dico,graph,liste_evac_node,liste_edge)[0])

print("resultat : ",resultat)

