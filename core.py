from rpg import *

states: list[str] = ['idle', 'enemy', 'p1', 'p2', 'p3', 'p4', 'p5', 'heal']
colors: dict = {'G': (255, 25, 30), 'V': (255, 135, 40), 'M': (100, 120, 255), 'D': (70, 255, 100)}


def load_players(configuration: dict) -> list[Player]:
    players: list[Player] = []

    for key in list(configuration.keys()):
        current: dict = configuration[key]
        players.append(load_player(current['role'], current['level'], key, current['weapon'], current['item']))

    return players


class Fight:
    def __init__(self, players_configuration: dict, enemy_id: str, logs: bool = True):
        self.logs = logs
        self.attacks: list[Attack] = []
        self.current_state: str = states[-1]
        self.players: list[Player] = load_players(players_configuration)
        self.dead_players: list[Player] = []
        self.enemy: Entity = load_enemy(enemy_id, hp_modifier=len(self.players))
        self.turn = -1
        self.running = True
        self.heals = [0]*6

    def get_next_state(self) -> str:
        index = states.index(self.current_state) + 1

        if index == len(states):
            return 'idle'

        if states[index][1].isdigit() and int(states[index][1]) > len(self.players):
            return 'heal'

        return states[index]

    def player_attack(self, player_id: int):
        current_player: Player = self.players[player_id]

        if current_player.hp <= 0:
            return

        attack = self.attacks[0]

        print(f'* Player {current_player.name} is attacking the enemy : {attack}')

        if attack.hit:
            attack = self.enemy.roll_defense(attack)

            if attack.hit:
                print(f'* Player {current_player.name} hits the enemy : {attack}')
            else:
                print(f'* The enemy dodges')
        else:
            print('* The player misses the attack')

        if self.enemy.hp <= 0:
            print('\n--> The enemy is defeated : the players win !')
            self.running = False
            return

        if self.get_next_state() == 'heal':
            self.attacks.clear()

            for i in range(len(self.players)):
                self.heals[i] = self.players[i].regen_in

            for i in range(len(self.players)):
                heal: int = self.players[i].regen_out

                if heal == 0:
                    continue

                for j in range(len(self.players)):
                    if i != j:
                        self.heals[j] += heal

            self.heals[-1] = self.enemy.regen_in
        else:
            self.attacks = [self.players[player_id + 1].roll_attack()]

    def enemy_attack(self, front_range, back_range):
        picking_range: list[Player] = front_range if len(front_range) > 0 else back_range

        target_id = random.randint(0, len(picking_range) - 1)
        self.enemy.targets.append(picking_range[target_id].name)
        self.attacks.append(self.players[target_id].roll_defense(self.enemy.roll_attack()))
        picking_range.pop(target_id)

        return front_range, back_range

    def get_player_by_name(self, player_name: str) -> Player | None:
        for p in self.players:
            if p.name == player_name:
                return p

        return None

    def next_action(self):
        self.current_state = self.get_next_state()

        if self.current_state == 'idle':
            self.turn += 1

        print(f'\n-- Turn {self.turn} : {self.current_state} --')

        match self.current_state:
            case 'idle':
                print('Players :')

                for p in self.players:
                    print('-', p)

                print(f'Enemy:', self.enemy)

                self.attacks.clear()

                front_range: list[Player] = [p for p in self.players if p.role in ['G', 'V']]
                back_range: list[Player] = [p for p in self.players if p.role in ['M', 'D']]
                n = len(self.players)

                # first attack
                front_range, back_range = self.enemy_attack(front_range, back_range)

                # second attack
                if len(back_range) > 0 and random.random() <= -0.1*n**2 + 1.1*n - 2.1:
                    front_range, back_range = self.enemy_attack(front_range, back_range)

                    # TODO :
                    #  hesitation between the third attack is possible IF AND ONLY IF 5 players are alive or
                    #  JUST IF 5 players are in the team, alive or dead
                    #  for the moment, we consider that the third attack is only possible if there are at least 5
                    #  players ALIVE

                    # third attack
                    if n == 5 and len(self.players) > 0 and random.random() <= 0.3:
                        self.enemy_attack(front_range, back_range)

            case 'enemy':
                to_remove_players: list[Player] = []

                for i in range(len(self.attacks)):
                    attack = self.attacks[i]
                    target = self.get_player_by_name(self.enemy.targets[i])

                    print(f'The enemy is attacking the player {target.name} : {attack}')

                    if attack.hit:
                        attack = self.attacks[i]

                        if attack.hit:
                            print(f'* The player {target.name} takes {attack.damage} damages')
                            target.hp -= attack.damage

                            if target.hp <= 0:
                                to_remove_players.append(target)
                                print(f'* Player {target.name} dies from the attack')
                        else:
                            print(f'* The player {target.name} dodges the attack')
                    else:
                        print('* The enemy misses the attack')

                self.enemy.targets.clear()

                for dead_player in to_remove_players:
                    self.players.remove(dead_player)
                    self.dead_players.append(dead_player)

                if len(self.players) == 0:
                    print('--> All players are dead : they lose the fight')
                    self.running = False
                    return

                self.attacks.clear()
                self.attacks.append(self.players[0].roll_attack())

            case 'p1':
                self.player_attack(0)
            case 'p2':
                self.player_attack(1)
            case 'p3':
                self.player_attack(2)
            case 'p4':
                self.player_attack(3)
            case 'p5':
                self.player_attack(4)

            case 'heal':
                for i in range(len(self.players)):
                    self.players[i].hp = min(self.players[i].hp + self.heals[i], self.players[i].max_hp)
                    print(f'* Healing the player {self.players[i].name} by {self.heals[i]} hp')

                self.enemy.hp = min(self.enemy.hp + self.heals[-1], self.enemy.max_hp)
                print(f'Healing enemy by {self.heals[-1]} hp')

                self.heals = [0]*6
