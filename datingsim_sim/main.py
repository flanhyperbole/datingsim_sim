#%%
import random
from collections import abc

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

    def __str__(self) -> str:
        return f"""
            extraversion {Stats.statbar(self.extraversion_intraversion)} intraversion
            openess      {Stats.statbar(self.openess_calculation)} calculation
            emotion      {Stats.statbar(self.emotion_intelligence)} intelligence
        """
    
    @staticmethod
    def statbar(stat):
        reverse = stat < 0
        stat_abs = abs(stat)
        if stat_abs > 5:
            # alter state
            return "[...ERROR...]"
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
        self.game = None

    def __str__(self) -> str:
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

    def get_preferred(self):
        return self.get_max_min_attraction()
    
    def get_least_preferred(self):
        return self.get_max_min_attraction(False)

    def get_max_min_attraction(self, _max=True):
        _index = {v:k for k,v in self.attraction.items()}
        _key = max(list(_index)) if _max else min(list(_index))
        return self.game.characters[_index[_key]]
    
    def calculate_attraction(self, other):
        #total attraction is the inverse of the distance between two characters stats
        attraction = 0
        for stat_compare in zip(self.stats.get_stat_iter(), other.stats.get_stat_iter()):
            stat_diff = abs(stat_compare[0] - stat_compare[1])
            # print(f"got {stat_diff} from {stat_compare} => {10 - stat_diff}")
            attraction += (10 - stat_diff)
        if attraction > 30 or attraction < 0:
            if not self.game.allow_yandare:
                attraction = 30 if attraction > 30 else 0
        self.attraction[other.name] = attraction

    def become_closer(self, other, statblock, amount = 1):
        if amount == 0:
            return ""
        self.adjust_relationship(other, statblock, amount, adjustment = 'positive')
        return f"{self.name} became closer with {other.name}!"

    def increase_distaste(self, other, statblock, amount = 1):
        if amount == 0:
            return ""
        self.adjust_relationship(other, statblock, amount, adjustment = 'negative')
        return f"{self.name}'s distate for {other.name} bacame more pronounced..."
    
    def adjust_relationship(self, other, statblock, amount, adjustment):
        # if both on same end of spectrum the lower moves to the extreme,
        #if on opposite sides both character move towards the center
        symbolA, symbolB = ('+', '-') if adjustment == 'positive' else ('-', '+')
        
        self_stat = getattr(self.stats, statblock)
        other_stat = getattr(other.stats, statblock)
        set_self_stat = lambda x: setattr(self.stats, statblock, x)
        set_other_stat = lambda x: setattr(other.stats, statblock, x)

        if self_stat == other_stat:
            if adjustment != 'positive':
                set_self_stat(self_stat - amount)
                set_other_stat(other_stat + amount)
            else:
                #no changes necessary
                pass
        elif (self_stat > 0 > other_stat) or (self_stat < 0 < other_stat):
            if self_stat > 0:
                set_self_stat(eval(f"{self_stat} {symbolB} {amount}"))
                set_other_stat(eval(f"{other_stat} {symbolA} {amount}"))
            else:
                set_self_stat(eval(f"{self_stat} {symbolA} {amount}"))
                set_other_stat(eval(f"{other_stat} {symbolB} {amount}"))
        else:
            if abs(self_stat) > abs(other_stat):
                if self_stat > 0:
                    set_other_stat(eval(f"{other_stat} {symbolA} {amount}"))
                else:
                    set_other_stat(eval(f"{other_stat} {symbolB} {amount}"))
            else:
                if other_stat > 0:
                    set_self_stat(eval(f"{self_stat} {symbolA} {amount}"))
                else:
                    set_self_stat(eval(f"{self_stat} {symbolB} {amount}"))

        self.calculate_attraction(other)
                
                
#%%

class Game:
    def __init__(self, prompt=True):
        self.characters = {}
        self.round = 0
        self.allow_yandare = False
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
        self.event_count = 10
        self.events = []

    def _set_initial_attraction(self):        
        for character_name, character in self.characters.items():
            setattr(character, 'game', self)
            for other_character_name, other_character in self.characters.items():
                if character_name == other_character_name:
                    continue
                else:
                    character._add_attraction(other_character)

    def add_character(self):
        name = input(f'charater {len(self.characters) + 1} name:')
        self.characters[name] = Character(name) 

    def end_game(self):
        # at game end each character has a chance to confess their emotions
        # to another character. Chances of success are attraction / 32, where
        # there is always one bad end and a great end
        # how to sort...
        paired = []
        action_list = self.get_sort()
        # action_list = self.compute_poly(action_list)
        pass

    def get_sort(self):
        res = {}
        for character_name, character in self.characters.items():
            for other_name, other_score in character.attraction.items():
                others_score_for_character = self.characters[other_name].attraction[character_name]
                total_score = other_score + others_score_for_character
                _key = "|".join(sorted([character_name, other_name]))
                res[_key] = total_score
        res = self.compute_poly(res)
        res_sort = {k: v for k, v in sorted(res.items(), key=lambda item: item[1], reverse=True)}
        #compute poly
        return res_sort

    def compute_poly(self, action_list):
        scores = list(action_list.values())
        for score in scores:
            if scores.count(score) > 1:
                candidites = [i for k,v in action_list.items() for i in k.split('|') if v == score]
                canidate_count = [candidites.count(c) for c in candidites]
                if len(set(canidate_count)) == 1:
                    polyset = "|".join(sorted(list(set(candidites))))
                    action_list = {k:v for k,v in action_list.items() if v != score}
                    action_list[polyset] = score
        return action_list


        

#%%

# an event affects each charaters stats that match the stat(s) that 
# are defined in the event. for each matching stat the character rolls a d4.
# > 15 great success
# < 5 great fail
# 5 - 10 normal
# 
# If character is using the opposite stat (eg: introvert on an extrovert event) 
# abs the stat for dice rolls but the effect will be repulsion against enemy
# 
# 1 in 20 chance to sabotage another pairing
# 1 in 10 chance to accidentially repulse fav, or attract enemy
  
class Event:
    D4 =  list(range(1, 5))
    D10 = list(range(1, 11))
    D20 = list(range(1, 21))

    def __init__(self):
        self.name = None
        self.desc = None
        
        self.desc_sabotage = None
        self.desc_success = None
        self.desc_fail = None
        self.desc_normal = None

        self.character_number = None
        self.characters = None
        self.stat_affects = None
        self.stat_positive = True
        self.stat_amounts = (3, 1, 0)
        self.game = None

        self.desc_result = ""

    @classmethod
    def from_json(cls):
        pass

    def event_run(self):
        self.add_result(self.name)
        self.add_result(self.desc)
        self.affecting_characters()
        self.each_characters()
        self.results()    
    
    def roll(self, die):
        return random.choice(die)
    
    def affecting_characters(self):
        if self.character_number == 0 or self.character_number > len(self.game.characters):
            self.characters = self.game.characters 
        else:
            self.characters = random.choices(self.game.characters, self.character_number)
    
    def each_characters(self):
        statblock = self.stat_affects
        for _, character in self.characters.items():
            preferred = True
            if self.roll(Event.D20) == 1:
                self.sabotage(character)
            if self.roll(Event.D10) == 1:
                preferred = False
            self.event_result(character, statblock, preferred)

    def event_result(self, character, statblock, preferred):
        self_stat = getattr(character.stats, statblock)
        attract = True if self_stat >= 0 else False
        attract = attract if self.stat_positive else not(attract)
        result = sum([self.roll(Event.D4) for _ in range(0, abs(self_stat))])
        args = [character, statblock, preferred, attract]
        # print(f"""
        #     {character.name} event
        #     {preferred=}
        #     {attract=}
        #     {result=}
        # """)
        if result > 15:
            self.affect(*args, amount=self.stat_amounts[0], desc=self.desc_success)
        elif result < 5:
            self.affect(*args, amount=self.stat_amounts[2], desc=self.desc_fail)
        else:
            self.affect(*args, amount=self.stat_amounts[1], desc=self.desc_normal)
        
    def affect(self, character, statblock, preferred, attract, amount, desc):
        other = character.get_preferred() if preferred else character.get_least_preferred()
        self.add_result(desc.format(self_name = character.name, other_name = other.name))
        match attract:
            case True:
                self.add_result(character.become_closer(other, statblock, amount))
            case False:
                self.add_result(character.increase_distaste(other, statblock, amount))

    def sabotage(self, character):
        pass         

    def add_result(self, desc):
        self.desc_result += f"\n{desc}"    

    def results(self):
        return self.desc_result

            


#%%
def run():
    print('running....')