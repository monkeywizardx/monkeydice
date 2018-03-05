'''
A simple and robust dice framework.
Written two years after my first attempt at this.
It provides a general way to make rolls based off of strings.
It has several functions that use "roll strings".
Roll strings are the standard string representation of a die roll in this library.
Roll strings followed the following tokenization process and EBNF:

TOKENS: # Regexes for parsing.
    number = \\d+
    d = (d|D)
    add = \\+
    sub = \\-
EBNF:
    expr: die [{ modifier }]
    die: number d number
    modifier:
            | add number
            | sub number
'''

import random
import re
ROLL_STRING_PATTERN = re.compile(r'\d+(d|D)\d+(( )?((\+|\-)( )?((\d)+)))*')
SPLIT_PATTERN = re.compile(r'[dD+-]')
WHITESPACE = re.compile(r'\w+')
class RollStringException(Exception):
    '''
    Exception raised for invalid roll string.
    '''
    pass

def _roll_die(modifier, sides=6):
    '''
    TAKES:
        modifier: integer. # Dice modifier.
        sides: integer, default = 6. # Sides on the die.
    RETURNS:
        random number between 1 and sides and adds the modifier.
    Rolls a die and adds modifier.
    '''
    return random.randint(1, sides) + int(modifier)

class DiceRoll:
    '''
    If you need to make a roll more than once, this is your class.
    It takes a roll string, by default 1d6, and stores it's AST.
    '''
    def __init__(self, str_="1d6"):
        self.ast = _parse_roll_string(str_)

    def _enumerated_roll(self):
        return _roll_ast(self.ast, enumerate_=True)

    def roll(self):
        '''
        Returns a simple roll based off of the internal AST.
        '''
        return _roll_ast(self.ast)

    def prettify_enumerated_roll(self):
        '''
        Generates a pretty enumeration of all the rolled dice, for debugging or presenting purposes.
        '''
        enumeration = self._enumerated_roll()
        add_string = ""
        for roll in enumeration['dice rolls']:
            if add_string:
                add_string = ' + '.join([add_string, roll])
            else:
                add_string = str(roll)
        return "{}d{}+{} = {} ({})".format(self.ast['number_of_dice'],
                                           self.ast['die_sides'],
                                           self.ast['modifier'],
                                           enumeration['result'],
                                           add_string)

def roll(str_):
    '''
    TAKES:
        str_: str. # A roll string, like 1d4 + 3 or 1d6.
    RETURNS:
        A random number in the described range.
    '''
    return _roll_ast(_parse_roll_string(str_))

def _parse_roll_string(str_):
    '''
    Parse a roll string.
    TAKES:
        str_: str. # A roll string.
    RETURNS:
        a dict describing the dice roll to be passed to _roll_ast.
    '''
    if not ROLL_STRING_PATTERN.match(str_):
        raise RollStringException('Invalid roll string')
    dice_str = WHITESPACE.sub(str_, '') # Strip WHITESPACE
    tokens = [int(token) if token.is_digit() else token for token in SPLIT_PATTERN.split(dice_str)]
    ast = {
        'number_of_dice': tokens[0], # Grab the first number.
        'die_sides': tokens[2] # Skip past the D.
    }
    tokens = tokens[2::] # Pop off the dice descriptor
    mod_number = 0
    while tokens:
        token = tokens.pop(0)
        if token == '+':
            mod_number += token.pop(0)
        elif token == '-':
            mod_number -= token.pop(0)
    ast['modifier'] = mod_number
    return ast

def _roll_ast(ast, enumerate_=False):
    '''
    Generates a call to _roll based off of an ast.
    '''
    number_of_dice = ast['number']
    die_sides = ast['sides']
    modifier = ast['modifier']
    return _roll(number_of_dice, die_sides, modifier, enumerate_)

def _roll(number_of_dice, sides, modifier, enumerate_):
    '''
    TAKES:
        number_of_dice: integer. # Number of dice to roll.
        sides: integer. # Number of sides on the die.
        modifier: integer. # Modifier to the die.
        enumerate_: boolean = False.
    RETURN:
        if enumerate_:
            returns a dict enumerating every die roll with the modifier, and result.
        else:
            returns result.
    '''
    if enumerate_:
        result = {'result': 0, 'dice rolls': []}
    else:
        result = 0
    for dummy in range(number_of_dice):
        roll = _roll_die(modifier, sides)
        if enumerate_:
            result['dice rolls'].append(roll)
    return result
