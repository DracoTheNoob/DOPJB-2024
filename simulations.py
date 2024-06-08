import json
import csv
from random import randint as r

from no_print_core import Fight

enemies = ['P1', 'P2', 'P3', 'L1', 'L2', 'L3', 'MV1', 'MV2', 'MV3', 'D1']


def load_fight(players_level: int, enemy_id: str):
    # load players from json configuration file
    players_configuration_file = open(f'generated_data/players_{players_level}.json', 'r')
    players_configuration = json.load(players_configuration_file)
    players_configuration_file.close()
    del players_configuration_file

    return Fight(players_configuration, enemy_id)


def write_csv(results: list[list[str]]):
    with open(f'generated_data/results/{r(0, 999)}.csv', 'w+', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Lvl.'] + enemies)

        for row in results:
            writer.writerow(row)


def main(exponent: int = 2):
    depth = 10**exponent
    results: list[list[str]] = [
        ['1'] + ['-1'] * len(enemies),
        ['2'] + ['-1'] * len(enemies),
        ['3'] + ['-1'] * len(enemies),
        ['4'] + ['-1'] * len(enemies),
        ['5'] + ['-1'] * len(enemies)
    ]

    # load enemy from json configuration file
    for level in range(1, 6):
        for enemy_id in range(len(enemies)):
            enemy = enemies[enemy_id]
            wins = 0

            for generation in range(depth):
                fight = load_fight(level, enemy)

                while len(fight.players) > 0 and fight.enemy.hp > 0:
                    fight.next_action()

                if fight.enemy.hp <= 0:
                    wins += 1

            winrate = int(round(wins / depth * 1000)) / 10
            results[level-1][enemy_id+1] = f'{str(winrate).replace('.', ',')} %'

            print(f'lvl. {level} VS {enemy} -> {results[level-1][enemy_id+1]}')
        print()

    write_csv(results)


if __name__ == '__main__':
    main(2)
