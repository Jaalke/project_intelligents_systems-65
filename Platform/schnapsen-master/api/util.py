"""
General utility functions
"""

import math, sys, os, inspect
import traceback
import importlib
from api import Deck


def other(
        player_id # type: int
        ):
    # type: () -> int
    """
    Returns the index of the opposite player to the one given: ie. 1 if the argument is 2 and 2 if the argument is 1.
    :param player:
    :return:
    """
    return 1 if player_id == 2 else 2 # type: int

def get_suit(card_index):
    """
    Returns the suit of a card
    :param card_index:
    :return:
    """
    return Deck.get_suit(card_index)

def get_rank(card_index):
    """
    Returns the rank of a card
    :param card_index:
    :return:
    """
    return Deck.get_rank(card_index)

def get_card_name(card_index):
    # type: () -> int
    """
    Returns the rank and the suit of a card. Maps card indices as stored in memory to actual cards
    :param card_index:
    :return:
    """
    return get_rank(card_index), get_suit(card_index)


class BotFactory:
    """
    This factory can create newly instantiated bts each time it is called. The class is loaded and checked once. 
    """
    def __init__(self, playerName, className="Bot"):
        """
        Create a new BotFactory for a bot with the given name.
        If the name is 'random', this factory will load the file 
        ./bots/random/random.py and instantiate the class "Bot" from that file.
        """
        self.cls = load_player_class(playerName, className)
        self.botname = playerName

    def create_player(self):
        """
        Instantiate a new bot
        """
        # Get a reference to the class
        try:
            player = self.cls() # Instantiate the class
            player.__init__()
            return player
        except:
            print('ERROR: Could not load the class "Bot" {} from file {}.'.format(classname, path))
            traceback.print_exc()
            sys.exit()
    def get_player_name(self):
        return self.botname

def load_player(name, classname='Bot'):
    #
    """
    Accepts a string representing a bot and returns an instance of that bot. If the name is 'random'
    this function will load the file ./bots/random/random.py and instantiate the class "Bot"
    from that file.

    :param name: The name of a bot
    :return: An instantiated Bot
    """
    cls = load_player_class(name, classname=classname)

    # Get a reference to the class
    try:
        player = cls() # Instantiate the class
        player.__init__()
        return player
    except:
        # print('ERROR: Could not load the class "Bot" {} from file {}.'.format(classname, path))
        traceback.print_exc()
        sys.exit()


def load_player_class(name, classname='Bot'):
    #
    """
    Accepts a string representing a bot and returns an instance of that bot. If the name is 'random'
    this function will load the file ./bots/random/random.py and instantiate the class "Bot"
    from that file.

    :param name: The name of a bot
    :return: An instantiated Bot
    """
    if not name.islower():
        print(''' WARNING: You provided a botname with capital letters in it. 
        The system will lowercase that to ensure compatibility with Windsows!.''')
        name = name.lower()
    path = './bots/{}/{}.py'.format(name, name)
    # Load the python file (making it a _module_)
    try:
        module = importlib.import_module('bots.{}.{}'.format(name, name))
    except:
        print('ERROR: Could not load the python file {}, for player with name {}. Are you sure your Bot has the right '
              'filename in the right place? Does your python file have any syntax errors?'.format(path, name))
        traceback.print_exc()
        sys.exit(1)

    # Check whter the class has the right methods
    try:
        cls = getattr(module, classname)
        initParams = inspect.signature(cls.__init__).parameters
        for ((par, parspec), index) in zip(initParams.items(), range(len(initParams))):
            if index == 0:
                # this is the self parameter
                continue
            else:
                if parspec.default == inspect.Parameter.empty:
                    raise Exception("The botclass " + name + "could not be loaded because its contruction requires non default parameters") 
        return cls
    except:
        
        print('ERROR: Could not load the class "Bot" {} from file {}.'.format(classname, path))
        traceback.print_exc()
        sys.exit()



def ratio_points(state, player):
	if state.get_points(player) + state.get_points(other(player)) != 0:
		return state.get_points(player) / float((state.get_points(player) + state.get_points(other(player))))
	return 0

def difference_points(state, player):
    return state.get_points(player) - state.get_points(other(player))
