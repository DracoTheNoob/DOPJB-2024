import json

import no_print_core
from no_print_core import Fight


def main(exponent: int = 2):
    depth = 10**exponent

    # load enemy from json configuration file
    enemy_id = 'D1'
    wins = 0

    objective = .9
    largest_sum = 0
    largest = None
    largest_stat = None

    players_configuration_file = open(f'data/players.json', 'r')
    players_configuration = json.load(players_configuration_file)
    players_configuration_file.close()
    del players_configuration_file

    players = no_print_core.load_players(players_configuration)

    for hp in range(600, 1100, 100):
        for atk in range(100, 190, 10):
            for defense in range(30, 80, 10):
                stat = f'[hp={hp}, atk={atk}, def={defense}]'

                for generation in range(depth):
                    fight = Fight(None, enemy_id, players=players)

                    fight.enemy.hp = fight.enemy.max_hp
                    fight.enemy.atk = atk
                    fight.enemy.defense = defense

                    while len(fight.players) > 0 and fight.enemy.hp > 0:
                        fight.next_action()

                    if fight.enemy.hp <= 0:
                        wins += 1

                winrate = wins / depth

                if hp/1100 + atk/190 + defense/80 > largest_sum and winrate >= objective:
                    largest = winrate
                    largest_sum = hp/1100 + atk/190 + defense/80
                    largest_stat = stat

                print(stat, '->', int(round(winrate*1000)) / 10, '%')
                wins = 0

    print()
    print('nearest winrate:', largest, largest_sum, largest_stat)


if __name__ == '__main__':
    main(2)
