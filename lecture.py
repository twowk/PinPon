import numpy as np

########################################
filename = "exemple.txt"
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
	dico[int(line[0]),int(line[1])] = struct



f.close()
#retourner gros dico degeu
########################################


########################################
filename = "soluce.txt"
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
	dico[int(line[0])] = struct

valid =  f.readline()
val_fct_obj =  int(f.readline())
temps_calc =  float(f.readline())
methode =  f.readline()
champ_libre =  f.readline()
#retourner gros dico degeu
########################################


########################################
#input dico jeu donnee et dico soluce




#return True/False
########################################






