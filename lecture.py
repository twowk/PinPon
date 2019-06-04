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
		struct["length"] = int(float(line[3])) # + 1 ?????????
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
	for i in liste_evac_node:
		decalage = dico_soluce[i]["date_debut"]
		for j in range(dico[i]["k"]):
			if j == 0:
				liste = [dico[i]["id"],dico[i]["v"][0]]
			else:
				liste = [dico[i]["v"][j-1],dico[i]["v"][j]]
			if not (liste in liste_R):
				liste_R.append(liste)
				duree = int(dico[i]["pop"] / dico_soluce[i]["taux_evac"]) 
				liste_master.append([liste,[[dico[i]["id"],duree,decalage,dico_soluce[i]["taux_evac"]]]])

			else:
				duree = int(dico[i]["pop"] / dico_soluce[i]["taux_evac"]) 
				liste_master[liste_R.index(liste)][1].append([dico[i]["id"],duree,decalage,dico_soluce[i]["taux_evac"]])
			if((liste[0],liste[1]) in graph):
				decalage = decalage + graph[(liste[0],liste[1])]["length"]
			else:
				decalage = decalage + graph[(liste[1],liste[0])]["length"]

	#print("liste_master : " , liste_master)
	for K in liste_master:
		
		if((K[0][0],K[0][1]) in graph):
			capa = graph[(K[0][0],K[0][1])]["capacity"]
		else:
			capa = graph[(K[0][1],K[0][0])]["capacity"]
	
		decal = []
		for L in K[1]:
				decal.append(L[2])
		
		for date in decal:
			somme = 0
			for	L in K[1]:
				
				somme += getFlow(L,date)

			if somme>capa:
				#print("pas ok 1")
				return False
	decal_max = 0
	for z in liste_evac_node:
		if (dico_soluce[z]["date_debut"]>decal_max):
			decal_max = dico_soluce[z]["date_debut"]
	
	if((borne_inf(dico,graph)+decal_max)==dico_soluce["val_fct_obj"]):
		#print("ok")
		return True
	else:
		#print("pas ok 2")
		return False

########################################	

def borne_inf(dico,graph):	#Comme si tout le monde partait en même sans qu'il y ait de problème sur les arcs
	maxe = 0
	
	for E in dico:
		somme = int(dico[E]["pop"] / dico[E]["max_rate"])
		for j in range(dico[E]["k"]):
			if j == 0:
				a_tmp = dico[E]["id"]	#L ordre des noeuds d un arc peut être inverse il faut tester les deux possibilites
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

def borne_sup(dico,graph):	#Les zones s'évacuent les unes après les autres, une zone commençant seulement quand la précédente a terminé
	maxe = 0
	
	for E in dico:
		somme = dico[E]["pop"] / dico[E]["max_rate"]
		for j in range(dico[E]["k"]):
			if j == 0:
				a_tmp = dico[E]["id"]	#L ordre des noeuds d un arc peut être inverse il faut tester les deux possibilites
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
#Fonction d'evaluation
#Retourne un tuple contenant la valeur de la fonc objectif
#et un boolean disant si la solution est valide
def fonc_eval(liste_depart,dico,graph,liste_evac_node):
	#print("fonc_eval")
	dico_soluce = {}
	for i in range(len(liste_depart)):
		dico_soluce[liste_evac_node[i]] = {"id" : liste_evac_node[i],"taux_evac" : dico[liste_evac_node[i]]["max_rate"], "date_debut" : liste_depart[i]}
	dico_soluce["val_fct_obj"] = max(liste_depart) + borne_inf(dico,graph)
	sol_ok = verif(dico_soluce,dico,graph,liste_evac_node)
	return (dico_soluce["val_fct_obj"],sol_ok)

#Renvoie 
def transforme_liste(lst):
	lst_tmp = lst.copy()
	for i in range(len(lst)):
		j = lst.index(min(lst))
		lst_tmp[j] = i
		lst[j] = 9999999999
	return lst_tmp
#Recherche locale - Intensification
def intensification(liste_evac_node,dico,graph):
	print("intensification")
	#Mise a jour des max rates
	for cle in dico:
		max_rate = dico[cle]["max_rate"]
		for j in range(dico[cle]["k"]):
			if j == 0:
				a_tmp = dico[cle]["id"]	#L ordre des noeuds d un arc peut être inverse il faut tester les deux possibilites
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


	liste_depart = []
	rang = []
	#On se place à borne sup
	maxe = 0
	for E in dico:
		
		liste_depart.append(maxe)
		somme = dico[E]["pop"] / dico[E]["max_rate"]
		for j in range(dico[E]["k"]):
			if j == 0:
				a_tmp = dico[E]["id"]	#L ordre des noeuds d un arc peut être inverse il faut tester les deux possibilites
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
		rang.append(somme)
	rang = transforme_liste(rang)

	for i in range(len(rang)):
		ind = rang.index(i)
		liste_depart[ind] = maxe
		E = liste_evac_node[ind]
		somme = int(dico[E]["pop"] / dico[E]["max_rate"]) + 1
		for j in range(dico[E]["k"]):
			if j == 0:
				a_tmp = dico[E]["id"]	#L ordre des noeuds d un arc peut être inverse il faut tester les deux possibilites
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

	#print("liste depart : ",liste_depart)
	#On divise chaque temps de depart par 2 puis on enleve 1 quand ce n est plus possible
	for j in range(len(liste_depart)):
		i = rang.index(j)
		(val,ok) = fonc_eval(liste_depart,dico,graph,liste_evac_node)
		print(ok)
		while (liste_depart[i] > 0 and ok == True):
			lst_tmp = liste_depart.copy()
			lst_tmp[i] = int(liste_depart[i] /2)
			(val,ok) = fonc_eval(lst_tmp,dico,graph,liste_evac_node)
			print(ok)
			if (ok == True):
				liste_depart = lst_tmp.copy()

		(val,ok) = fonc_eval(liste_depart,dico,graph,liste_evac_node)
		print(ok)
		while (liste_depart[i] > 0 and ok == True):
			lst_tmp = liste_depart.copy()
			lst_tmp[i] = liste_depart[i]-1
			(val,ok) = fonc_eval(lst_tmp,dico,graph,liste_evac_node)
			print(ok)
			if (ok == True):
				liste_depart = lst_tmp.copy()


	for cle in dico:
		print("noeud" , dico[cle]["id"], "rate" , dico[cle]["max_rate"])
	print(liste_evac_node)
	return liste_depart
##############################



(dico, graph, liste_evac_node, liste_edge) = file_read("exemple.txt")

#(dico_soluce,liste_evac_node_soluce) = soluce("sparse_10_30_3_10_I2019052809_35_12")
#resultat = verif(dico_soluce,dico,graph,liste_evac_node)

#print("dico soluce : ",dico_soluce)
#print("resultat : ",resultat)


print(borne_inf(dico,graph))
print(borne_sup(dico,graph))


print("intens = " ,intensification(liste_evac_node,dico,graph))

