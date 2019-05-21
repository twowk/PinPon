import numpy as np

########################################
#Permet la lecture du document en entrée, renvoie : 
#dico : toutes les infos pour chaque zone à évacuer
#graph : infos du graphe avec les capacités des arcs, longeurs,...
#evac node : listes des noeuds des zones à évacuer
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
		struct["length"] = int(float(line[3]))
		struct["capacity"] = int(float(line[4]))
	
		liste_edge.append([int(line[0]),int(line[1])])
		graph[(int(line[0]),int(line[1]))] = struct



	f.close()
	return (dico, graph, liste_evac_node, liste_edge)
########################################


########################################
#Permet de lire un fichier solution, renvoie :
#dico_soluce : pour chaque zone à evacuer, 
#	l'id de la zone de depart
#	le taux d'evac
#	la date de debut
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
#Permet de verifier que la solution est realisable
#Renvoie True ou False
def verif(dico_soluce,dico,graph,liste_evac_node):

	liste_R = []
	liste_master = []

	for i in range(len(liste_evac_node)):
		decalage = dico_soluce[i+1]["date_debut"]
		for j in range(dico[i+1]["k"]):
			if j == 0:
				liste = [dico[i+1]["id"],dico[i+1]["v"][0]]
			else:
				liste = [dico[i+1]["v"][j-1],dico[i+1]["v"][j]]
			if not (liste in liste_R):
				liste_R.append(liste)
				duree = dico[i+1]["pop"] / dico_soluce[i+1]["taux_evac"]
				liste_master.append([liste,[[dico[i+1]["id"],duree,decalage,dico_soluce[i+1]["taux_evac"]]]])

			else:
				duree = dico[i+1]["pop"] / dico_soluce[i+1]["taux_evac"]
				liste_master[liste_R.index(liste)][1].append([dico[i+1]["id"],duree,decalage,dico_soluce[i+1]["taux_evac"]])

			decalage = decalage + graph[(liste[0],liste[1])]["length"]
	
	for K in liste_master:
		capa = graph[(K[0][0],K[0][1])]["capacity"]
	
		decal = []
		for L in K[1]:
				decal.append(L[2])
		for date in decal:
			somme = 0
			for	L in K[1]:
				somme += getFlow(L,date)
			if somme>capa:
				return False
	decal_max = 0
	for z in liste_evac_node:
		if (dico_soluce[z]["date_debut"]>decal_max):
			decal_max = dico_soluce[z]["date_debut"]
	
	if((borne_inf(dico,graph)+decal_max)==dico_soluce["val_fct_obj"]):
		return True
	else:
		return False
########################################	

def borne_inf(dico,graph):	#Comme si tout le monde partait en même sans qu'il y ait de problème sur les arcs
	maxe = 0
	
	for E in dico:
		somme = dico[E]["pop"] / dico[E]["max_rate"]
		for j in range(dico[E]["k"]):
			if j == 0:
				somme += graph[(dico[E]["id"],dico[E]["v"][j])]["length"]
			else:
				somme += graph[(dico[E]["v"][j-1],dico[E]["v"][j])]["length"]
		if somme > maxe :
			maxe = somme
	return maxe

def borne_sup(dico,graph):	#Les zones s'évacuent les unes après les autres, une zone commençant seulement quand la précédente a terminé
	maxe = 0
	
	for E in dico:
		somme = dico[E]["pop"] / dico[E]["max_rate"]
		for j in range(dico[E]["k"]):
			if j == 0:
				somme += graph[(dico[E]["id"],dico[E]["v"][j])]["length"]
			else:
				somme += graph[(dico[E]["v"][j-1],dico[E]["v"][j])]["length"]
		maxe += somme
	return maxe

##############################
#Fonction d'evaluation
#Retourne un tuple contenant la valeur de la fonc objectif
#et un boolean disant si la solution est valide
def fonc_eval(liste_depart,dico,graph,liste_evac_node):
	print("fonc_eval")
	dico_soluce = {}
	for i in range(len(liste_depart)):
		dico_soluce[i+1] = {"id" : i+1,"taux_evac" : dico[i+1]["max_rate"], "date_debut" : liste_depart[i]}
	dico_soluce["val_fonc_obj"] = liste_depart[-1] + borne_inf(dico,graph)
	sol_ok = verif(dico_soluce,dico,graph,liste_evac_node)
	return (dico_soluce["val_fonc_obj"],sol_ok)

#Recherche locale - Intensification
def intensification(liste_evac_node,dico,graph):
	print("intensification")
	liste_depart = []
	#On se place à borne sup
	maxe = 0
	for E in dico:
		liste_depart.append(maxe)
		somme = dico[E]["pop"] / dico[E]["max_rate"]
		for j in range(dico[E]["k"]):
			if j == 0:
				somme += graph[(dico[E]["id"],dico[E]["v"][j])]["length"]
			else:
				somme += graph[(dico[E]["v"][j-1],dico[E]["v"][j])]["length"]
		maxe += somme
	print(liste_depart)
	continuer = 1
	coeff = 2 #coeff pour reduire rapidement les dates de depart
	while (continuer):
		


##############################

(dico, graph, liste_evac_node, liste_edge) = file_read("exemple.txt")
(dico_soluce,liste_evac_node_soluce) = soluce("soluce.txt")

resultat = verif(dico_soluce,dico,graph,liste_evac_node)

print("dico soluce : ",dico_soluce)
print("evac node soluce : ", liste_evac_node_soluce)
#print(resultat)
#print(borne_inf(dico,graph))
#print(borne_sup(dico,graph))

intensification(liste_evac_node,dico,graph)




