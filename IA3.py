# -*- coding: utf-8 -*-


"""Robot-joueur de Pooo
    
    Le module fournit les fonctions suivantes :
        register_pooo(uid)
        init_pooo(init_string)
        play_pooo()
        
"""

__version__='0.1'
 

## chargement de l'interface de communication avec le serveur
from poooc import order, state, state_on_update, etime


from parse import *
# mieux que des print partout
import logging
# pour faire de l'introspection
import inspect
#import des fonctions de l'IA
from fonctions_ia3 import *


global monflag
global plateau
global identifiant

def register_pooo(uid):
    global identifiant
    identifiant = uid
    """Inscrit un joueur et initialise le robot pour la compétition

        :param uid: identifiant utilisateur
        :type uid:  chaîne de caractères str(UUID) 
        
        :Example:
        
        "0947e717-02a1-4d83-9470-a941b6e8ed07"

    """

def init_pooo(init_string):
    global identifiant
    global plateau
    """Initialise le robot pour un match
        
        :param init_string: instruction du protocole de communication de Pooo (voire ci-dessous)
        :type init_string: chaîne de caractères (utf-8 string)
       
       
       INIT<matchid>TO<#players>[<me>];<speed>;\
       <#cells>CELLS:<cellid>(<x>,<y>)'<radius>'<offsize>'<defsize>'<prod>,...;\
       <#lines>LINES:<cellid>@<dist>OF<cellid>,...

       <me> et <owner> désignent des numéros de 'couleur' attribués aux joueurs. La couleur 0 est le neutre.
       le neutre n'est pas compté dans l'effectif de joueurs (<#players>).
       '...' signifie que l'on répète la séquence précédente autant de fois qu'il y a de cellules (ou d'arêtes).
       0CELLS ou 0LINES sont des cas particuliers sans suffixe.
       <dist> est la distance qui sépare 2 cellules, exprimée en... millisecondes !
       /!\ attention: un match à vitesse x2 réduit de moitié le temps effectif de trajet d'une cellule à l'autre par rapport à l'indication <dist>.
       De manière générale temps_de_trajet=<dist>/vitesse (division entière).
        
        :Example:
        
        "INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3"
        
    """
    #creation du plateau
    plateau = plateau()
    
    #recuperation des informations de init_string
    plateau = parser_init(init_string,plateau)
    plateau.uid = identifiant
    
    #initialisation du plateau
    #plateau.nb_player = etat_debut[0]
    #plateau.nb_node = etat_debut[1]
    #plateau.ls_node = etat_debut[2]
    #plateau.flag = etat_debut[3]
    #plateau.speed = etat_debut[4]
    #plateau.uid = etat_debut[5]
    
    #ajout de tous les noeuds dans le plateau
    #for i in range(nb_node):
    #    plateau.add_node(ls_node[i])
    
    
def play_pooo():
    global plateau
    global identifiant
    """Active le robot-joueur
    
    """
    logging.info('Entering play_pooo fonction from {} module...'.format(inspect.currentframe().f_back.f_code.co_filename))
    ### Début stratégie joueur ### 
    # séquence type :
    # (1) récupère l'état initial 
    # init_state = state()
    # (2) TODO: traitement de init_state
    # (3) while True :
    # (4)     state = state_on_update()    
    # (5)     TODO: traitement de state et transmission d'ordres order(msg)
    
    while True:
        a = state_on_update()
        if 'Game over' in a:
            break
        plateau = parser_state(a,plateau)
        plateau.display()
        

        noeuds = nos_noeuds(plateau)
        order(str(voisins_ennemis(plateau,noeuds)))
        order(str(voisins_neutres(plateau,noeuds)))
        order(str(monseulvoisin_estmoi(plateau,noeuds)))
        order(str(de_quel_cote_aller(plateau,noeuds)))

    #INIT20ac18ab-6d18-450e-94af-bee53fdc8fcaTO6[2];1;3CELLS:1(23,9)'2'30'8'I,2(41,55)'1'30'8'II,3(23,103)'1'20'5'I;2LINES:1@3433OF2,1@6502OF3
    #STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]33'6;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3

        


