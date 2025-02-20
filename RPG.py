import random

magias_iniciais =  {
            "Mago": {"Bola de Fogo": {"level": 1,"mana": 10,"tooltip": ['int'],"dano": 2,"exp": [0,30]}},
            "Guerreiro":{"Golpe Forte":{"level": 1,"rage": 20,"tooltip": ['str'],"dano": 4,"exp": [0,30]}},
            "Ladino":{"Backstab":{"level": 1,"energy": 50,"tooltip": ['dex'],"dano": 3,"exp": [0,30]}},
            "Paladino":{"Smite":{"level": 1,"mana": 10,"tooltip":['int','str'],"dano": 2,"exp": [0,30]},
                        "Heal":{"level": 1,"mana": 10,"tooltip": ['int'],"cura": 3,"exp": [0,30]}}
        }

atributos = {
            "Guerreiro": {"hp": 100, "rage": 100, "str": 12, "dex": 4, "int": 2, "crit": 5, "dodge": 0},
            "Mago": {"hp": 60, "mana": 100, "str": 2, "dex": 4, "int": 12, "crit": 5, "dodge": 5},
            "Ladino": {"hp": 80, "energy": 100, "str": 3, "dex": 12, "int": 3, "crit": 30, "dodge": 10},
            "Paladino": {"hp": 100, "mana": 50, "str": 8, "dex": 2, "int": 8, "crit": 10, "dodge": 0},
        }

dice = []
for i in range(1, 100):
    dice.append(i)


class Player:
    def __init__(self, name, classe):
        self.name = name
        self.classe = classe
        self.level = 1
        self.exp = 0
        self.exp_max = 100
        self.gold = 1000
        self.arma = {}
        self.armor = {}
        self.aces = {}
        self.vivo = True
        self.agir = False
        self.hp_regen = 0
        self.mana_regen = 0
        self.exp_multi = 1

        if classe in atributos:
            self.hp = self.hp_max = atributos[classe]["hp"]
            if "mana" in atributos[classe]:
                self.mana = self.mana_max = atributos[classe]["mana"]
                self.recurso = 'mana'
                if self.classe == 'Mago':
                    self.mana_regen = 10
                else:
                    self.mana_regen = 5
            elif "rage" in atributos[classe]:
                self.mana = 0
                self.mana_max = atributos[classe]["rage"]
                self.recurso = 'rage'
                self.hp_regen = 5
            elif "energy" in atributos[classe]:
                self.mana = self.mana_max = atributos[classe]["energy"]
                self.recurso = 'energy'
                self.mana_regen = 20
            self.str = atributos[classe]["str"]
            self.dex = atributos[classe]["dex"]
            self.int = atributos[classe]["int"]
            self.crit = atributos[classe]["crit"]
            self.dodge = atributos[classe]["dodge"]
            self.magias = magias_iniciais[classe]
        else:
            raise ValueError("Classe inválida!\n")

    def status(self):
        print('--------------------------------------------------------------------')
        print(f'Personagem: {self.name} | Classe: {self.classe} | Level: {self.level}')
        print(f'HP: {self.hp}/{self.hp_max} | {self.recurso.capitalize()}: {self.mana}/{self.mana_max}')
        print(f'Força: {self.str} | Destreza: {self.dex} | Inteligência: {self.int}')
        print(f'Critico: {self.crit}% | Dodge: {self.dodge}%')
        print(f'EXP: {self.exp}/{self.exp_max} | Gold: {self.gold}')
        item = list(self.arma.keys())[0]
        print(f'Arma: {item}', end='  |  ')
        for stats,valor in self.arma[item].items():
            if stats != 'gold':
                print(f' {stats.upper()} : {valor}',end= '  |  ')
        item = list(self.armor.keys())[0]
        print(f'\nArmadura: {item}', end='  |  ')
        for stats, valor in self.armor[item].items():
            if stats != 'gold':
                print(f' {stats.upper()} : {valor}', end='  |  ')
        item = list(self.aces.keys())[0]
        print(f'\nAcessorio: {item}', end='  |  ')
        for stats, valor in self.aces[item].items():
            if stats != 'gold':
                print(f' {stats.upper()} : {valor}', end='  |  ')
        print('\n--------------------------------------------------------------------')
        print('Magias')
        for magia, atributos in self.magias.items():
            print(f"{magia} ->", " | ".join(f"{atributo}:{descri}" for atributo, descri in atributos.items()))


    def __str__(self):
        return f'Personagem: {self.name}, Classe: {self.classe},{self.level}'

class Monster:
    def __init__(self, jogador, dificuldade):
        match dificuldade:
            case 1:
                self.level = jogador.level
            case 2:
                self.level = jogador.level + 1
            case 3:
                self.level = jogador.level + random.randint(2,3)
            case 4:
                self.level = jogador.level + 5

        self.name = f"Monstro {self.level}"
        if dificuldade == 4:
            self.dano = 6 * self.level
            self.hp = self.hp_max = 60 * self.level
            self.crit = 10 + (self.level / 2)
            self.exp = 50 * self.level
            self.gold = 50 * self.level
            self.status = 'boss'
        else:
            self.dano = 4 * self.level
            self.hp = self.hp_max = 40 * self.level
            self.crit = 10 * (self.level / 2)
            self.exp = 200 * self.level
            self.gold = 30 * self.level
            self.status = 'comum'

def gerarbatalha(jogador, dificuldade):
    monstro = Monster(jogador, dificuldade)
    fight(jogador,monstro)

def fight(jogador, monstro):
    print(f'Monstro level {monstro.level} encontrado')
    while True:
        jogador.agir = False
        escolhas_disponiveis = {"1": "Atacar", "2": "Magia", "3": "Fugir"}
        print("-" * 30)
        print(f'MONSTRO -> HP: {monstro.hp}/{monstro.hp_max} | Dano: {monstro.dano}')
        print(f'{jogador.name} -> HP: {jogador.hp}/{jogador.hp_max} | {jogador.recurso.upper()}: {jogador.mana}/{jogador.mana_max} ')
        print("-"* 30)
        escolha = input("Escolha uma ação(1-Atacar|2-Magia|3-Fugir): ").capitalize()

        if escolha in escolhas_disponiveis or escolha in escolhas_disponiveis.values():
            escolha = escolhas_disponiveis.get(escolha, escolha)
            match escolha:
                case '1' | 'Atacar':
                    atacar(jogador,monstro)
                    jogador.agir = True
                case '2' | 'Magia':
                    usar_magia(jogador,monstro)
                case '3' | 'Fugir':
                    if monstro.status == 'boss':
                        print('Nao é possivel fudgir')
                    else:
                        if fugir(jogador):
                            break
                        else:
                            jogador.agir = True
        else:
            print('Opção indisponivel')

        if jogador.agir:
            if monstro.hp <= 0:
                print('Monstro morreu')
                exp_gold_gain(jogador, monstro)
                if jogador.classe == 'Ladino':
                    jogador.mana = jogador.mana_max
                elif jogador.classe == 'Guerreiro':
                    jogador.mana = 0
                break
            else:
                monstro_ataca(jogador, monstro)
                regen(jogador)

        if jogador.hp <= 0:
            jogador.vivo = False
            print('Voce morreu')
            break

def regen(jogador):
    match jogador.classe:
        case 'Ladino':
            jogador.mana += jogador.mana_regen
            if jogador.mana > jogador.mana_max:
                jogador.mana = jogador.mana_max

        case 'Mago' | 'Paladino':
            jogador.mana += jogador.mana_regen
            if jogador.mana > jogador.mana_max:
                jogador.mana = jogador.mana_max

        case 'Guerreiro':
            jogador.hp += jogador.hp_regen
            if jogador.hp > jogador.hp_max:
                jogador.hp = jogador.hp_max

def exp_gold_gain(jogador, monstro):
    print(f'Voce recebeu {monstro.exp} de exp e {monstro.gold} de gold')
    jogador.gold += monstro.gold
    jogador.exp += int(monstro.exp * round(jogador.exp_multi, 1))
    while True:
        if jogador.exp >= jogador.exp_max:
            jogador.exp -= jogador.exp_max
            levelup(jogador)
        else:
            break

def atacar(jogador,monstro):
    crit_check = False
    dano = 0

    if jogador.crit != 0:
        crit_check = critico_check(jogador)

    match jogador.classe:
        case 'Guerreiro' | 'Paladino':
            dano = jogador.str
        case 'Mago':
            dano = jogador.int
        case 'Ladino':
            dano = jogador.dex

    if crit_check:
            print("Causo dano critico!!")
            print(f"Voce causou {dano * 2} de dano")
            monstro.hp -= dano * 2
            if jogador.classe == 'Guerreiro':
                jogador.mana += 10
                if jogador.mana > jogador.mana_max:
                    jogador.mana = jogador.mana_max
    else:
        print(f"Voce causou {dano} de dano")
        monstro.hp -= dano
        if jogador.classe == 'Guerreiro':
            jogador.mana += 5
            if jogador.mana > jogador.mana_max:
                jogador.mana = jogador.mana_max

    if monstro.hp > 0:
        print(f"O monstro ficou com {monstro.hp} de vida")
    jogador.agir = True

def usar_magia(jogador,monstro):
    while True:
        crit_check = False
        lista_de_magias = {}
        tooltip = 0
        print(f'Voce tem {jogador.mana} de {jogador.recurso}')

        for num,(magia, atributos) in enumerate(jogador.magias.items(), start=1):
            lista_de_magias[num] = magia
            print(f"{num} - {magia} ->", " | ".join(f"{atributo}:{descri}" for atributo, descri in atributos.items()))

        escolha = input('Escolha uma magia("S" ou "Sair"): ').capitalize()
        if escolha == 'Sair' or escolha == 'S':
            break
        elif escolha.title() in jogador.magias.keys() or int(escolha) in lista_de_magias:
            if escolha.isdigit():
                escolha = lista_de_magias[int(escolha)]

            if jogador.mana < jogador.magias[escolha][jogador.recurso]:
                print(f"Voce nao tem {jogador.recurso} suficiente para usa esta magia")
            else:
                jogador.mana -= jogador.magias[escolha][jogador.recurso]
                jogador.magias[escolha]['exp'][0] += int(10 * round(jogador.exp_multi, 1))
                if "dano" in jogador.magias[escolha]:
                    total = jogador.magias[escolha]["dano"]
                    for atributo in jogador.magias[escolha]["tooltip"]:
                        match atributo:
                             case 'str':
                               tooltip += jogador.str
                             case 'dex':
                                tooltip += jogador.dex
                             case 'int':
                                tooltip += jogador.int
                    total *= tooltip
                    if 'bonus' in jogador.magias[escolha]:
                        match jogador.magias[escolha]['bonus']:
                            case 'lifesteal':
                                print('Voce utilizou uma habilidade com LIFESTEAL e vai se cura pelo dano causado')
                                jogador.hp += total
                                if jogador.hp > jogador.hp_max:
                                    jogador.hp = jogador.hp_max
                    if jogador.crit != 0:
                        crit_check = critico_check(jogador)
                    if crit_check:
                        print("Causo dano critico!!")
                        print(f"Voce causou {total * 2} de dano")
                        monstro.hp -= total * 2
                    else:
                        print(f"Voce causou {total} de dano")
                        monstro.hp -= total
                    if monstro.hp > 0:
                        print(f"O monstro ficou com {monstro.hp} de vida")

                elif "cura" in jogador.magias[escolha]:
                    total = jogador.magias[escolha][jogador.recurso]
                    for atributo in jogador.magias[escolha]["tooltip"]:
                        match atributo:
                            case 'str':
                                tooltip += jogador.str
                            case 'dex':
                                tooltip += jogador.dex
                            case 'int':
                                tooltip += jogador.int
                    total *= tooltip
                    if jogador.crit != 0:
                        crit_check = critico_check(jogador)
                    if crit_check:
                        print("Voce critou!!")
                        print(f"Voce curou {total * 2} de hp")
                        jogador.hp += total * 2
                    else:
                        print(f"Voce curou {total} de hp")
                        jogador.hp += total
                    if jogador.hp > jogador.hp_max:
                        jogador.hp = jogador.hp_max
                    print(f"Voce esta com {jogador.hp} de vida")
                if jogador.magias[escolha]['exp'][0] >= jogador.magias[escolha]['exp'][1]:
                    levelup_magia(jogador, escolha)
                jogador.agir = True
                break
        else:
            print('Opção indisponivel')

def monstro_ataca(jogador,monstro):
    if jogador.dodge > random.choice(dice):
        print("Voce desviou do ataque!")
    else:
        crit_check = critico_check(monstro)

        if crit_check:
            print('\nVoce recebeu Dano Critico!!')
            print(f"O monstro causou {monstro.dano * 2} em voce")
            jogador.hp -= monstro.dano * 2
        else:
            print(f"\nO monstro causou {monstro.dano} em voce")
            jogador.hp -= monstro.dano
        if jogador.hp > 0:
            print(f'Voce tem {jogador.hp} de vida restante')

        if jogador.classe == 'Guerreiro':
            if monstro.dano / 10 < 5:
                jogador.mana += 5
            else:
                jogador.mana += int(monstro.dano / 10)
                if jogador.mana > jogador.mana_max:
                    jogador.mana = jogador.mana_max

def critico_check(npc):
    if npc.crit > random.choice(dice):
        return True
    else:
        return False

def fugir(jogador):
    fuga = 50 + jogador.dodge
    if fuga >= random.choice(dice):
        print('Voce fugiu')
        return True
    else:
        print('Voce nao conseguiu escapar')
        return False

def levelup(jogador):
    jogador.level += 1
    jogador.exp_max = int(jogador.exp_max * 1.3)
    match jogador.classe:
        case 'Guerreiro':
            jogador.hp_max += 50
            jogador.hp = jogador.hp_max
            jogador.str += 3

        case 'Mago':
            jogador.hp_max += 20
            jogador.hp = jogador.hp_max
            jogador.mana_max += 50
            jogador.mana = jogador.mana_max
            jogador.int += 3

        case 'Ladino':
            jogador.hp_max += 30
            jogador.hp = jogador.hp_max
            jogador.dex += 3

        case 'Paladino':
            jogador.hp_max += 40
            jogador.hp = jogador.hp_max
            jogador.mana_max += 40
            jogador.mana = jogador.mana_max
            if jogador.level % 2 == 0:
                jogador.str += 2
                jogador.int += 1
            else:
                jogador.str += 1
                jogador.int += 2
    gain_magic(jogador)

    st = {"Mago": "Mana", "Paladino": "Mana", "Guerreiro": "Rage", "Ladino": "Energy"}
    print(f'\nVoce upou para o level {jogador.level}!!')
    print('-' * 30)
    print(f'Personagem: {jogador.name} | Classe: {jogador.classe} | Level: {jogador.level}')
    print(f'HP: {jogador.hp}/{jogador.hp_max} | {st[jogador.classe]}: {jogador.mana}/{jogador.mana_max}')
    print(f'Força: {jogador.str} | Destreza: {jogador.dex} | Inteligência: {jogador.int}')
    print(f'EXP: {jogador.exp}/{jogador.exp_max}')
    print('-' * 30)

def levelup_magia(jogador, escolha):
    print('#' * 30)
    if 'dano' in jogador.magias[escolha]:
        jogador.magias[escolha]['level'] += 1
        jogador.magias[escolha]['dano'] += 1
        if 'mana' in jogador.magias[escolha]:
            jogador.magias[escolha]['mana'] += 2
        jogador.magias[escolha]['exp'][0] -= jogador.magias[escolha]['exp'][1]
        jogador.magias[escolha]['exp'][1] += 10 * (jogador.magias[escolha]['level'] - 1 )
        print(f"Sua magia {escolha} upou para o level {jogador.magias[escolha]['level']}")
        print(f"Agora ela tem {jogador.magias[escolha]['dano']} de dano base")

    elif 'cura' in jogador.magias[escolha]:
        jogador.magias[escolha]['level'] += 1
        jogador.magias[escolha]['cura'] += 1
        jogador.magias[escolha]['mana'] += 2
        jogador.magias[escolha]['exp'][0] -= jogador.magias[escolha]['exp'][1]
        jogador.magias[escolha]['exp'][1] += 10 * (jogador.magias[escolha]['level'] - 1 )
        print(f"Sua magia {escolha} upou para o level {jogador.magias[escolha]['level']}")
        print(f"Agora ela tem {jogador.magias[escolha]['cura']} de cura base")
    print('#' * 30)

def gain_magic(jogador):
    match jogador.classe:
        case 'Mago':
            match jogador.level:
                case 3:
                    jogador.magias["Seta de gelo"] = {"level": 1,"mana": 15,"tooltip": ['int'],"dano": 4,"exp": [0,30]}
                    print('%' * 30)
                    print('Voce aprendeu a magia "SETA DE GELO"')
                    print('%' * 30)
                case 5:
                    jogador.magias["Inferno"] = {"level": 1,"mana": 50,"tooltip": ['int'],"dano": 10,"exp": [0,30]}
                    print('%' * 30)
                    print('Voce aprendeu a magia "INFERNO"')
                    print('%' * 30)
        case 'Paladino':
            match jogador.level:
                case 3:
                    jogador.magias["Consagração"] = {"level": 1, "mana": 15, "tooltip": ['int'], "dano": 6,"exp": [0, 30]}
                    print('%' * 30)
                    print('Voce aprendeu a magia "CONSAGRAÇÃO"')
                    print('%' * 30)
                case 5:
                    jogador.magias["Julgamento"] = {"level": 1, "mana": 25, "tooltip": ['str','int'], "dano": 10, "exp": [0, 30]}
                    print('%' * 30)
                    print('Voce aprendeu a magia "JULGAMENTO"')
                    print('%' * 30)
        case 'Guerreiro':
            match jogador.level:
                case 3:
                    jogador.magias["Golpe Feroz"] = {"level": 1, "rage": 40, "tooltip": ['str'], "dano": 10,
                                                     "exp": [0, 30]}
                    print('%' * 30)
                    print('Voce aprendeu a magia "GOLPE FEROZ"')
                    print('%' * 30)
                case 5:
                    jogador.magias["Golpe Sangrento"] = {"level": 1, "rage": 50, "tooltip": ['str'], "dano": 10,'bonus':'lifesteal',
                                                    "exp": [0, 30]}
                    print('%' * 30)
                    print('Voce aprendeu a magia "REDEMOINHO"')
                    print('%' * 30)
        case 'Ladino':
            match jogador.level:
                case 3:
                    jogador.magias["Estocada"] = {"level": 1, "energy": 50, "tooltip": ['dex'], "dano": 6,
                                                     "exp": [0, 30]}
                    print('%' * 30)
                    print('Voce aprendeu a magia "ESTOCADA"')
                    print('%' * 30)
                case 5:
                    jogador.magias["Golpe duplo"] = {"level": 1, "energy": 80, "tooltip": ['dex'], "dano": 10,
                                                    "exp": [0, 30]}
                    print('%' * 30)
                    print('Voce aprendeu a magia "GOLPE DUPLO"')
                    print('%' * 30)

def loja(jogador):
    tipo = {'1': 'Arma', '2': 'Armadura', '3': 'Acessorio', '9': 'Sair'}

    while True:
        for num, op in tipo.items():
            print(f'{num} - {op}')
        escolha = input('O que deseja comprar ? ').strip().capitalize()

        match escolha:
            case '1' | 'Arma':
                loja_armas(jogador)
            case '2' | 'Armadura':
                loja_armor(jogador)
            case '3' | 'Acessorio':
                loja_aces(jogador)
            case '9':
                break
            case _:
                print('Opção invalida')

def loja_armas(jogador):
    choice_list = {}
    gold_value = 0
    lista_de_armas = {'Machado': {'str': 5, 'crit': 5, 'gold': 50},
                      'Adaga': {'dex': 5, 'crit': 10, 'gold': 50},
                      'Cajado': {'int': 5, 'crit': 5, 'gold': 50},
                      'Espada': {'str': 3, 'int': 2, 'crit': 5, 'gold': 50},
                      'Espada de Treino': {'exp':1.2, 'gold': 50}
                      }
    while True:
        for num, arma in enumerate(lista_de_armas.keys()):
            print(f"{num + 1} - {arma} ->", end=' ')
            for desc in lista_de_armas[arma].keys():
                match desc:
                    case 'str':
                        print(f"STR: {lista_de_armas[arma][desc]}", end=' | ')
                    case 'dex':
                        print(f"DEX: {lista_de_armas[arma][desc]}", end=' | ')
                    case 'int':
                        print(f"INT: {lista_de_armas[arma][desc]}", end=' | ')
                    case 'crit':
                        print(f"CRIT: {lista_de_armas[arma][desc]}%", end=' | ')
                    case 'exp':
                        print(f"Multiplicador de EXP: {lista_de_armas[arma][desc]}", end=' | ')
                    case 'gold':
                        print(f"Custo:  {lista_de_armas[arma][desc]} de gold")
            choice_list[num + 1] = arma
        escolha = input('Qual arma deseja comprar ?("S" ou "Sair")').capitalize()
        if escolha == 'Sair' or escolha == 'S':
            break
        if escolha.isdigit():
            escolha = int(escolha)
        if escolha in choice_list:
            escolha = choice_list[escolha]
            if jogador.gold >= lista_de_armas[escolha]['gold']:
                if jogador.arma == {}:
                    escolha2 = input(
                        f'Deseja comprar mesmo um(a) {escolha} custando {lista_de_armas[escolha]['gold']} de gold? [Y]').upper()
                    if escolha2 == 'Y':
                        jogador.gold -= lista_de_armas[escolha]['gold']
                        equipar_arma(jogador, escolha, lista_de_armas[escolha])
                        break
                elif list(jogador.arma.keys())[0] != escolha:
                    escolha2 = input(
                        f'Voce possui um {list(jogador.arma.keys())[0]}, deseja trocar mesmo por um(a) {escolha} custando {lista_de_armas[escolha]['gold']} de gold? [Y]').upper()
                    if escolha2 == 'Y':
                        for item in jogador.arma.values():
                            gold_value = int(item.get('gold') / 2)
                        jogador.gold += gold_value
                        print(f'Voce recebeu {gold_value} de gold pela sua arma antiga')
                        jogador.gold -= lista_de_armas[escolha]['gold']
                        equipar_arma(jogador, escolha, lista_de_armas[escolha])
                        break
                elif list(jogador.arma.keys())[0] == escolha:
                    print('Voce ja possui esta arma')
            else:
                print('Gold insuficiente')
        else:
            print('Opção invalida')

def loja_armor(jogador):
    choice_list = {}
    gold_value = 0
    lista_de_armaduras = {'Armadura de Ferro': {'hp': 200, 'str': -2, 'dex': -2, 'dodge': -50, 'gold': 100},
                          'Roupa de Couro': {'hp': 40, 'energy': 40, 'dex': 2, 'dodge': 10, 'gold': 100},
                          'Manto': {'hp': 20, 'mana': 100, 'int': 5, 'dodge': 5, 'gold': 100},
                          'Armadura Leve': {'hp': 50, 'mana': 50, 'str': 2, 'int': 2, 'gold': 100},
                          'Roupa de Treino': {'hp': 20,'exp':1.2, 'gold': 100}
                          }
    while True:
        for num, armadura in enumerate(lista_de_armaduras.keys()):
            print(f"{num + 1} - {armadura} ->", end=' ')
            for desc in lista_de_armaduras[armadura].keys():
                match desc:
                    case 'hp':
                        print(f"HP: {lista_de_armaduras[armadura][desc]}", end=' | ')
                    case 'mana':
                        print(f"Mana: {lista_de_armaduras[armadura][desc]}", end=' | ')
                    case 'str':
                        print(f"STR: {lista_de_armaduras[armadura][desc]}", end=' | ')
                    case 'dex':
                        print(f"DEX: {lista_de_armaduras[armadura][desc]}", end=' | ')
                    case 'int':
                        print(f"INT: {lista_de_armaduras[armadura][desc]}", end=' | ')
                    case 'crit':
                        print(f"CRIT: {lista_de_armaduras[armadura][desc]}%", end=' | ')
                    case 'dodge':
                        print(f"Dodge: {lista_de_armaduras[armadura][desc]}%", end=' | ')
                    case 'exp':
                        print(f"Multiplicador de EXP: {lista_de_armaduras[armadura][desc]}", end=' | ')
                    case 'gold':
                        print(f"Custo:  {lista_de_armaduras[armadura][desc]} de gold")
            choice_list[num + 1] = armadura
        escolha = input('Qual armadura deseja comprar ?("S" ou "Sair")')
        if escolha == 'Sair' or escolha == 'S':
            break
        if escolha.isdigit():
            escolha = int(escolha)
        if escolha in choice_list:
            escolha = choice_list[escolha]
            if jogador.gold >= lista_de_armaduras[escolha]['gold']:
                if jogador.armor == {}:
                    escolha2 = input(
                        f'Deseja comprar mesmo um(a) {escolha} custando {lista_de_armaduras[escolha]['gold']} de gold? [Y]').upper()
                    if escolha2 == 'Y':
                        jogador.gold -= lista_de_armaduras[escolha]['gold']
                        equipar_armadura(jogador, escolha, lista_de_armaduras[escolha])
                        break
                elif list(jogador.armor.keys())[0] != escolha:
                    escolha2 = input(
                        f'Voce possui um {list(jogador.armor.keys())[0]}, deseja trocar mesmo por um(a) {escolha} custando {lista_de_armaduras[escolha]['gold']} de gold? [Y]').upper()
                    if escolha2 == 'Y':
                        for item in jogador.armor.values():
                            gold_value = int(item.get('gold') / 2)
                        jogador.gold += gold_value
                        print(f'Voce recebeu {gold_value} de gold pela sua armadura antiga')
                        jogador.gold -= lista_de_armaduras[escolha]['gold']
                        equipar_armadura(jogador, escolha, lista_de_armaduras[escolha])
                        break
                elif list(jogador.armor.keys())[0] == escolha:
                    print('Voce ja possui esta arma')
            else:
                print('Gold insuficiente')
        else:
            print('Opção invalida')

def loja_aces(jogador):
    choice_list = {}
    gold_value = 0
    lista_de_acess = {'Anel de STR': {'str': 5,'gold': 300},
                          'Anel de DEX': {'dex': 5,'gold': 300},
                          'Anel de INT': {'int': 5,'gold': 300},
                          'Pesos': {'str': -2,'dex': -2,'int': -2,'exp': 1.2,'gold': 100}
                          }
    while True:
        for num, aces in enumerate(lista_de_acess.keys()):
            print(f"{num + 1} - {aces} ->", end=' ')
            for desc in lista_de_acess[aces].keys():
                match desc:
                    case 'hp':
                        print(f"HP: {lista_de_acess[aces][desc]}", end=' | ')
                    case 'mana':
                        print(f"Mana: {lista_de_acess[aces][desc]}", end=' | ')
                    case 'str':
                        print(f"STR: {lista_de_acess[aces][desc]}", end=' | ')
                    case 'dex':
                        print(f"DEX: {lista_de_acess[aces][desc]}", end=' | ')
                    case 'int':
                        print(f"INT: {lista_de_acess[aces][desc]}", end=' | ')
                    case 'crit':
                        print(f"CRIT: {lista_de_acess[aces][desc]}%", end=' | ')
                    case 'dodge':
                        print(f"Dodge: {lista_de_acess[aces][desc]}%", end=' | ')
                    case 'exp':
                        print(f"Multiplicador de EXP: {lista_de_acess[aces][desc]}", end=' | ')
                    case 'gold':
                        print(f"Custo:  {lista_de_acess[aces][desc]} de gold")
            choice_list[num + 1] = aces
        escolha = input('Qual armadura deseja comprar ?("S" ou "Sair")')
        if escolha == 'Sair' or escolha == 'S':
            break
        if escolha.isdigit():
            escolha = int(escolha)
        if escolha in choice_list:
            escolha = choice_list[escolha]
            if jogador.gold >= lista_de_acess[escolha]['gold']:
                if jogador.aces == {}:
                    escolha2 = input(
                        f'Deseja comprar mesmo um(a) {escolha} custando {lista_de_acess[escolha]['gold']} de gold? [Y]').upper()
                    if escolha2 == 'Y':
                        jogador.gold -= lista_de_acess[escolha]['gold']
                        equipar_aces(jogador, escolha, lista_de_acess[escolha])
                        break
                elif list(jogador.aces.keys())[0] != escolha:
                    escolha2 = input(
                        f'Voce possui um(a) {list(jogador.aces.keys())[0]}, deseja trocar mesmo por um(a) {escolha} custando {lista_de_acess[escolha]['gold']} de gold? [Y]').upper()
                    if escolha2 == 'Y':
                        for item in jogador.aces.values():
                            gold_value = int(item.get('gold') / 2)
                        jogador.gold += gold_value
                        print(f'Voce recebeu {gold_value} de gold pela seu acessorio antigo')
                        jogador.gold -= lista_de_acess[escolha]['gold']
                        equipar_aces(jogador, escolha, lista_de_acess[escolha])
                        break
                elif list(jogador.aces.keys())[0] == escolha:
                    print('Voce ja possui esta arma')
            else:
                print('Gold insuficiente')
        else:
            print('Opção invalida')

def equipar_arma(jogador, arma_nova , stats):
    if jogador.arma != {}:
        arma_antiga = list(jogador.arma.keys())[0]
        for atributo, valor in jogador.arma[arma_antiga].items():
            match atributo:
                case 'str':
                    jogador.str -= valor
                case 'dex':
                    jogador.dex -= valor
                case 'int':
                    jogador.int -= valor
                case 'crit':
                    jogador.crit -= valor
                case 'exp':
                    jogador.exp_multi -= valor - 1

    jogador.arma = {arma_nova: stats}

    for atributo, valor in stats.items():
        match atributo:
            case 'str':
                jogador.str += valor
            case 'dex':
                jogador.dex += valor
            case 'int':
                jogador.int += valor
            case 'crit':
                jogador.crit += valor
            case 'exp':
                jogador.exp_multi += valor - 1

    print(f'Arma equipada: {arma_nova}')
    print(f'HP: {jogador.hp}/{jogador.hp_max} | {jogador.recurso.upper()}: {jogador.mana}/{jogador.mana_max}')
    print(f'Força: {jogador.str} | Destreza: {jogador.dex} | Inteligência: {jogador.int}')
    print(f'Critico: {jogador.crit}% | Dodge: {jogador.dodge}%')

def equipar_armadura(jogador, armadura_nova , stats):
    if jogador.armor != {}:
        armadura_antiga = list(jogador.armor.keys())[0]
        for atributo, valor in jogador.armor[armadura_antiga].items():
            match atributo:
                case 'hp':
                    jogador.hp_max -= valor
                    if jogador.hp > jogador.hp_max:
                        jogador.hp = jogador.hp_max
                case 'mana' | 'energy':
                    jogador.mana_max -= valor
                    if jogador.mana > jogador.mana_max:
                        jogador.mana = jogador.mana_max
                case 'str':
                    jogador.str -= valor
                case 'dex':
                    jogador.dex -= valor
                case 'int':
                    jogador.int -= valor
                case 'crit':
                    jogador.crit -= valor
                case 'dodge':
                    jogador.dodge -= valor
                case 'exp':
                    jogador.exp_multi -= valor - 1

    jogador.armor = {armadura_nova: stats}

    for atributo, valor in stats.items():
        match atributo:
            case 'hp':
                jogador.hp_max += valor
                jogador.hp += valor
            case 'mana' | 'energy' if jogador.recurso in [atributo]:
                jogador.mana_max += valor
                jogador.mana += valor
            case 'str':
                jogador.str += valor
            case 'dex':
                jogador.dex += valor
            case 'int':
                jogador.int += valor
            case 'crit':
                jogador.crit += valor
            case 'dodge':
                jogador.dodge += valor
            case 'exp':
                jogador.exp_multi += valor - 1


    print(f'Armadura equipada: {armadura_nova}')
    print(f'HP: {jogador.hp}/{jogador.hp_max} | {jogador.recurso.upper()}: {jogador.mana}/{jogador.mana_max}')
    print(f'Força: {jogador.str} | Destreza: {jogador.dex} | Inteligência: {jogador.int}')
    print(f'Critico: {jogador.crit}% | Dodge: {jogador.dodge}%')

def equipar_aces(jogador, aces_novo, stats):
    if jogador.aces != {}:
        item_antiga = list(jogador.aces.keys())[0]
        for atributo, valor in jogador.aces[item_antiga].items():
            match atributo:
                case 'hp':
                    jogador.hp_max -= valor
                    if jogador.hp > jogador.hp_max:
                        jogador.hp = jogador.hp_max
                case 'mana' | 'energy':
                    jogador.mana_max -= valor
                    if jogador.mana > jogador.mana_max:
                        jogador.mana = jogador.mana_max
                case 'str':
                    jogador.str -= valor
                case 'dex':
                    jogador.dex -= valor
                case 'int':
                    jogador.int -= valor
                case 'crit':
                    jogador.crit -= valor
                case 'dodge':
                    jogador.dodge -= valor
                case 'exp':
                    jogador.exp_multi -= valor - 1

    jogador.aces = {aces_novo: stats}

    jogador.aces = {aces_novo: stats}

    for atributo, valor in stats.items():
        match atributo:
            case 'hp':
                jogador.hp_max += valor
                jogador.hp += valor
            case 'mana' | 'energy' if jogador.recurso in [atributo]:
                jogador.mana_max += valor
                jogador.mana += valor
            case 'str':
                jogador.str += valor
            case 'dex':
                jogador.dex += valor
            case 'int':
                jogador.int += valor
            case 'crit':
                jogador.crit += valor
            case 'dodge':
                jogador.dodge += valor
            case 'exp':
                valor -= 1
                jogador.exp_multi += valor

    print(f'Arma equipada: {aces_novo}')
    print(f'HP: {jogador.hp}/{jogador.hp_max} | {jogador.recurso.upper()}: {jogador.mana}/{jogador.mana_max}')
    print(f'Força: {jogador.str} | Destreza: {jogador.dex} | Inteligência: {jogador.int}')
    print(f'Critico: {jogador.crit}% | Dodge: {jogador.dodge}%')

def create_character():
    nome = input('Digite o nome do seu personagem: ').title()

    classes_disponiveis = {"1": "Guerreiro", "2": "Ladino", "3": "Mago", "4":"Paladino"}

    while True:
        print('Classes disponíveis:')
        for num, classe in classes_disponiveis.items():
            print(f'{num} - {classe}')
        escolha = input('Qual é a sua classe? ').strip().capitalize()

        if escolha in classes_disponiveis or escolha in classes_disponiveis.values():
            classe_escolhida = classes_disponiveis.get(escolha, escolha)
            confirmacao = input(f"Confirma escolha como '{classe_escolhida}'? (Y/N) ").strip().upper()
            if confirmacao == 'Y':
                return Player(nome, classe_escolhida)
        else:
            print('Classe indisponível, tente novamente.')

def main():
    jogador = create_character()
    cidade = {'1':'Status','2':'Inn','3':'Loja','4':'Campo de Batalha','9':'Sair'}
    while jogador.vivo:
        for num,op in cidade.items():
            print(f'{num} - {op}')
        choice = input('Escolha uma opção: ').strip().title()

        match choice:
            case '1' | 'Status':
                jogador.status()

            case '2' | 'Inn':
                print('\nVoce visitou a taverna local e se recuperou de seus ferimentos')
                jogador.hp = jogador.hp_max
                if jogador.classe == 'Mago' or jogador.classe == 'Paladino':
                    jogador.mana = jogador.mana_max

            case '3' | 'Loja':
                loja(jogador)

            case '4' | 'Campo de Batalha':
                lista = {"1":"Facil","2":"Medio","3":"Dificil","4":"Chefe"}
                dificuldade = input('Escolha a dificuldade: (1-Facil | 2-Medio | 3-Dificil | 4-Chefe): ')
                if dificuldade.isdigit() and dificuldade in lista.keys():
                    dificuldade = int(dificuldade)
                    if dificuldade == 4:
                        escolha = input('Voce nao podera fugir da luta , deseja realmente enfrenta um chefe ? [Y]').upper()
                        if escolha == 'Y':
                            gerarbatalha(jogador, dificuldade)
                    else:
                        gerarbatalha(jogador, dificuldade)
                elif dificuldade.capitalize() in lista.values():
                    chave = [key for key, value in lista.items() if value == dificuldade.capitalize()][0]
                    dificuldade = int(chave)
                    if dificuldade == 4:
                        escolha = input('Voce nao podera fugir da luta , deseja realmente enfrenta um chefe ? [Y]').upper()
                        if escolha == 'Y':
                            gerarbatalha(jogador, dificuldade)
                    else:
                        gerarbatalha(jogador, dificuldade)
                else:
                    print('Dificuldade nao encontrada')

            case '9' | 'Sair':
                print("Saindo do jogo...")
                break
            case _:
                print("Opção inválida, tente novamente.")

print('teste')
if __name__ == "__main__":
    main()


