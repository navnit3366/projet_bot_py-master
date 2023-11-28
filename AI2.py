# ---------fichier pour stocker l'IA suggeré par Pierre

# ----------LIBS----------
from class_plateau import *
from poooc import order, state, state_on_update, etime
import parse
import inspect
import logging
import random

global board              # les variables globales, ça craint
board = plateau()                  # variable plateau


def register_pooo(uid):
    board.set_uid(uid)
    logging.info('[register_pooo] Bot {} registered'.format(uid))
    pass


def init_pooo(init_string):
    # logging.info('[init_pooo] Game init: {!r}'.format(init_string))
    parse.parser_init(init_string, board)
    board.display()
    pass


def play_pooo():
    logging.info('Entering play_pooo fonction from {} module...'.format(inspect.currentframe().f_back.f_code.co_filename))

    while True:
        msg = state_on_update()
        if 'STATE' in msg:
            liste_node_ennemi = []      # liste de noeuds ennemis
            liste_node_neutre = []      # liste de noeuds neutres
            liste_node_allie = []       # liste de nos noeuds
            logging.debug('[play_pooo] Received state: {}'.format(msg))
            parse.parser_state(msg, board)      # parsage de STATE
            board.display()
            for i in range(len(board.liste_node)):          # actualisation des liste
                if board.liste_node[i].owner == board.flag:
                    liste_node_allie.append(board.liste_node[i].id)
                elif board.liste_node[i] == -1:
                    liste_node_neutre.append(board.liste_node[i].id)
                else:
                    liste_node_ennemi.append(board.liste_node[i].id)
            for a in range(len(liste_node_allie)):     # Parcours des cellules alliées
                source = board.find_node(a)            # Copie l'addresse memoire dans source # source est de "type Node"
                if check_in(source.neighbor, liste_node_ennemi) and source.offsize > 0:     # si le node a un ennemi
                    for i in range(len(source.neighbor)):
                        cible = board.find_node(source.neighbor[i])
                        if cible != board.flag and cible != -1:   # on trouve l'ennemi
                            if source.offsize > (cible.offsize + cible.defsize) or (board.liste_node[i].offsize == 20 and board.liste_node[i].prod_off == 'I') or (board.liste_node[i].offsize == 30 and board.liste_node[i].prod_off == 'II') or (board.liste_node[i].offsize == 40 and board.liste_node[i].prod_off == 'III'):
                                order(parse.ordre_builder(board.uid, 100, source.id, cible.id))   # on l'attaque
                elif check_in(source.neighbor, liste_node_neutre) and source.offsize > 0:
                    # on peut mettre qu'une seule condition, l'autre est déjà testé
                    # Si les voisins sont neutres (ou allié)
                    cible = board.find_node(source.neighbor[0])  # cible est de type node
                    troupe_a_envoyer_min = cible.defsize + cible.offsize + 1
                    # Nbre de vaisseaux à envoyé pour prendre la planète
                    for b in range(len(source.neighbor)):
                        # On parcourt les voisins neutres
                        cible_2 = board.find_node(source.neighbor[b])       # 2e cible pour comparer avec cible
                        troupe_a_envoyer = (cible_2.defsize + cible_2.offsize + 1)
                        if troupe_a_envoyer < troupe_a_envoyer_min:
                            troupe_a_envoyer_min = troupe_a_envoyer
                            cible = cible_2         # la cible 2 devient la cible
                    if troupe_a_envoyer_min < source.offsize:     # Teste si on peut attaquer
                        ordre = parse.ordre_builder(board.uid, 100, source.id, cible.id)   # creer l'ordre
                        # crée l'ordre d'attaque
                        order(ordre)
                        # A l'ATTAQUE
                elif source.offsize > 0:
                    # Si les voisins sont alliés
                    if len(source.neighbor) == 1:   # le noeud n'a qu'un voisin allié
                        cible = board.find_node(source.neighbor[0])
                        order(parse.ordre_builder(board.uid, max_renfort(source, cible), source.id, cible.id))
                    else:
                        for b in range(len(source.neighbor)):   # On parcourt ses voisins
                            source_2 = source.neighbor[b]
                            if check_in(source_2.neighbor,liste_node_ennemi) or check_in(source_2,liste_node_neutre):
                                # on envoie des renforts si le voisin a un ennemi ou neutre
                                if source.offsize != 0:
                                    order(parse.ordre_builder(board.uid, max_renfort(source, source_2), source.id, source_2.id))
                                    pass
                        if source.offsize != 0:
                            cible = board.find_node(random.choice(source.neighbor))
                            order(parse.ordre_builder(board.uid, max_renfort(source, cible), source.id, cible.id))
                            # on envoie des unités au hasard
            logging.info('============ ( {} / {} ) ============='.format(len(liste_node_allie), board.nb_node))
        elif 'GAMEOVER' in msg:      # on arrête d'envoyer des ordres. On observe seulement...
            order('[{}]GAMEOVEROK'.format(board.uid))
            logging.debug('[play_pooo] Received game over: {}'.format(msg))
        elif 'ENDOFGAME' in msg:     # on sort de la boucle de jeu
            logging.debug('[play_pooo] Received end of game: {}'.format(msg))
            break
        else:
            logging.error('[play_pooo] Unknown msg: {!r}'.format(msg))
    logging.info('>>> Exit play_pooo function')
    pass


def check_in(liste1, liste2):   # fonction qui verifie la présence d'un élément commun aux deux listes
    for i in range(len(liste1)):
        for j in range(len(liste2)):
            if liste1[i] == liste2[j]:
                return True
    return False

def max_renfort(source,cible):  # optimise le nombre d'unités de renfort à envoyer
    if cible.prod_off == 'I':
        return ((20-cible.offsize)*100)/source.offsize
    elif cible.prod_off == 'II':
        return ((30-cible.offsize)*100)/source.offsize
    else:
        return ((40-cible.offsize)*100)/source.offsize