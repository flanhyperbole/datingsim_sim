#%%
import random


## FEATURES
# Charaters
    # attaction score to each character
    # three stats, (ex/in)troversion, open/calculating, wis/emote    

# Events
    # individual meets
    # group scenes

    # Depending on the attraction score between each charater could do:
    # attract
    # sabbotage
    # pact to help each other get with their preferred charater
    # betrayal

# Items
    # +/- to stats
    # can be used on others eg: buff / attack
    # ITEMS BE GIFTS 

# A game:
    # 10 rounds, and event each round
#%%


#%%

class Stats:
    STATRANGE = [i for i in range(-5, 6)]
    
    def __init__(self, randomise=False):
        self.randomise = randomise
        if not self.randomise:
            print("""
                A statblock is made of three statistics 
                - extraversion / introversion
                - openess / calculation
                - emotional intelligence / intelligence
                each of these can range between -5 and +5
            """)

        self.extraversion_intraversion = self.set_stat('extraversion vs intraversion')
        self.openess_calculation = self.set_stat('openess vs calculation')
        self.emotion_intelligence = self.set_stat('emotional intelligence vs intelliegence')

    def __repr__(self) -> str:
        return f"""
            extraversion <-> intraversion {self.extraversion_intraversion}
            openess <-> calculation = {self.openess_calculation}
            emotion <-> intelligence = {self.emotion_intelligence}
        """
    
    @staticmethod
    def statbar(stat):
        reverse = stat < 0
        stat_abs = abs(stat)
        statrange = [i for i in range(0, stat_abs)]
        print(statrange)
        barlist = ['.' for i in Stats.STATRANGE]
        for i in statrange:
            barlist[i] = '|'
        if reverse:
            barlist = barlist[::1]
        return f"[{''.join(barlist)}]"


    def set_stat(self, statname):
        if not self.randomise:
            stat = input(f'enter rating for {statname} between -5 and +5')
            if int(stat) not in Stats.STATRANGE:
                print(f'must set {statname} between -5 and +5')
                self.set_stat(statname)
        else:
            stat = random.choice(Stats.STATRANGE)
        return int(stat)

class Character:
    def __init__(self, name):
        self.name = name
        self.attraction = {}
        self.stats = self._set_stats()

    def __repr__(self) -> str:
        return f"""
            Character: {self.name}
            {self.stats=}
        """

    def _set_stats(self):
        randomise = input('would you like to set this characters stats? yes/no').lower().strip() != 'yes' 
        return Stats(randomise)

#%%

class Game:
    def __init__(self):
        self.characters = []
        self.round = 0
        while True:
            if len(self.characters) < 3:
                self.add_character()
            else:
                add = input('add another charater (yes/no)').lower().strip() == 'yes'
                if add:
                    self.add_character()
                else:
                    break

    def add_character(self):
        name = input(f'charater {len(self.characters) + 1} name:')
        self.characters.append(Character(name)) 



#%%
def run():
    print('running....')