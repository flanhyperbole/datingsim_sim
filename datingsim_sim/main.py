#%%
import random


## FEATURES
# Charaters
    # attaction score to each character
    # three stats, (ex/in)troversion, open/calculating, wis/emote    

# Events
    # individual meets
    # group scenes

    # an event will one, two or three stats, which will define how character interact with it

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
            extraversion {Stats.statbar(self.extraversion_intraversion)} intraversion
            openess      {Stats.statbar(self.openess_calculation)} calculation
            emotion      {Stats.statbar(self.emotion_intelligence)} intelligence
        """
    
    @staticmethod
    def statbar(stat):
        reverse = stat < 0
        stat_abs = abs(stat)
        statrange = [i for i in range(0, stat_abs+1)]
        barlist = ['.' for i in Stats.STATRANGE]
        for i in statrange:
            barlist[i+5] = '|'
        if reverse:
            barlist = barlist[::-1]
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
    
    def get_stat_iter(self):
        return [
            self.extraversion_intraversion
            , self.openess_calculation
            , self.emotion_intelligence
        ]
    

class Character:
    def __init__(self, name, prompt=True):
        self.name = name
        self.prompt = prompt
        self.attraction = {}
        self.stats = self._set_stats()

    def __repr__(self) -> str:
        return f"""
            Character: {self.name}
            stats: {self.stats}
        """

    @classmethod
    def create_character_with_stats(
        cls
        , name
        , extraversion_intraversion = 0
        , openess_calculation = 0
        , emotion_intelligence = 0
    ):
        anon = Character(name, False)
        anon.stats.extraversion_intraversion = extraversion_intraversion
        anon.stats.openess_calculation       = openess_calculation 
        anon.stats.emotion_intelligence      = emotion_intelligence
        return anon

    def _set_stats(self):
        randomise = True if not self.prompt else input('would you like to set this characters stats? yes/no').lower().strip() != 'yes' 
        return Stats(randomise)
    
    def _add_attraction(self, other):
        self.attraction[other.name] = 0 
        self.calculate_attraction(other)
    
    def calculate_attraction(self, other):
        #total attraction is the inverse of the distance between two characters stats
        attraction = 0
        for stat_compare in zip(self.stats.get_stat_iter(), other.stats.get_stat_iter()):
            stat_diff = stat_compare[0] - stat_compare[1]
            attraction += (10 - stat_diff)
        self.attraction[other.name] = attraction
#%%

class Game:
    def __init__(self, prompt=True):
        self.characters = {}
        self.round = 0
        if prompt:
            while True:
                if len(self.characters) < 3:
                    self.add_character()
                else:
                    add = input('add another charater (yes/no)').lower().strip() == 'yes'
                    if add:
                        self.add_character()
                    else:
                        break

    def _set_initial_attraction(self):        
        for character_name, character in self.characters.items():
            for other_character_name, other_character in self.characters.items():
                if character_name == other_character_name:
                    continue
                else:
                    character._add_attraction(other_character)

    def add_character(self):
        name = input(f'charater {len(self.characters) + 1} name:')
        self.characters[name] = Character(name) 



#%%
def run():
    print('running....')