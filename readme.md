# MonkeyDice
### A Python Dice library.

MonkeyDice is a simple python library meant to make RPG-style dice rolling easy.

### Examples
1. Rolling a die
  ```python
  import monkeydice as dice
  dice.roll('1d6') # Returns number between 1 and 6
  ```
2. Adding a modifier to a die
  ```python
  import monkeydice as dice
  dice.roll('1d6 + 3') # Returns a number between 1 and 6 plus 3.
  ```
3. Rolling multiple dice.
  ```python
  import monkeydice as dice
  dice.roll('2d6 + 1')
  ```
4. Multiple modifiers.
  ```python
  import monkeydice as dice
  dice.roll('2d6 + 8 - 2')
  ```
5. Repeating a dice roll
```python
import monkeydice as dice
roll = dice.DiceRoll('2d6 + 3')
roll.roll() # Equivalent to dice.roll('2d6 + 3')
```
