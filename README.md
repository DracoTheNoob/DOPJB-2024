core.py -> script principal, appelé directement par le main.py
drawing.py -> fonctions pour dessiner avec pygame
excel.py -> fonctions pour lire des fichiers .xlsx (pas .xls car déprécié)
main.py -> code à ouvrir pour lancer le programme : contient simplement la structure "if __name__ == '__main__':"
no_print_core.py -> exactement comme core.py mais sans les prints, pour faire des simulations
rpg.py -> classes liées à la base du jeu de rôle : Weapon, Item, Entity, Player
simulations.py -> pour tester une quantité définie de testes de combats : sert d'équilibrage
team_generator.py -> génère des équipes aléatoires du niveau 0 inclus au 5 inclus.