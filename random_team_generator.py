from random import randint as rand
import os


def generate(directory: str):
    path = f'{directory}{'/' if len(directory) > 0 else ''}'

    if not os.path.isdir(path):
        os.mkdir(path)

    roles = ['G', 'G', 'G', 'D', 'D']

    numbers: dict[str: str] = {
        'G': "1",
        'V': "2",
        'M': "3",
        'D': "4"
    }

    for level in range(6):
        json: str = '{'

        for j in range(len(roles)):
            if j != 0:
                json += ', '

            offset = rand(0, 2)

            player: dict = {
                "role": roles[j],
                "level": level,
                "weapon": "" "0" + numbers[roles[j]] + str(level) + "0",
                "item": "" if level - offset <= 0 else ("0" + str(numbers[roles[j]]) + str(level-offset) + "0")
            }

            json += f'"{j}": {str(player)}'

        json += '}'

        formatted = (json
                     .replace('\'', '"')
                     .replace(',', ',\n')
                     .replace('{', '{\n')
                     .replace('}', '}\n')
                     .replace('"}', '"\n}')
                     .replace('}\n,', '},')
                     .replace('\n "', '\n"')
                     )

        with open(f'{path}players_{level}.json', 'w') as file:
            file.write(formatted)
            file.flush()

            print(f'Created "{path}players_{level}.json"')


def main():
    generate('generated_data')


if __name__ == '__main__':
    main()
