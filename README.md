# Clickr

A Realm Grinder playing bot; for a __super__ old version of realm grinder, from around 10/06/**2015**.

## Getting Started

Uses Python 2.x

```pip install -r requirements.txt```

## Usage
* The grave accent, ``` ` ```, will start/stop clicking
* The minus key, ```-```, will lock the cursor in its position (you do **not** want your cursor clicking wildly as you knock your mouse!)
* The plus key, ```+```, enables/disables spell casting
* The asterisk key, ```*```, will reset the spell casting timer


There are 6 constant variables defined at the top of ```Clicker.py``` which need to be edited for the script to run properly (nobody ever said this was designed to be user friendly...):
* ```SLEEP_TIME``` - Is the time between clicks in seconds, but also controls the tick-rate of the script
* ```REMIND_TIME``` - Is the time between reminders for when the last spell was cast
* ```MANA_RECHARGE``` - Is the amount of mana gained per second, as defined in the game
* ```SPELL_MODE``` - Is how spells will be cast, as defined below
* ```SPELLS_TO_CAST``` - Is a list of the spells to be cast, as defined in ```spelldefinitions.py``` (explained below)
* ```SPELL_DELAY``` - Is the time between casting spells when using either of the delay spellcasting modes

Spells are defined in ```spelldefinitions.py``` as such:
*```num``` - The shortcut key to cast the spell
*```cost``` - The amount of mana needed to cast the spell
*```time``` - The cooldown period of the spell

There are three spellcasting modes; Sycronised, Delay, and DelayedBurst.
* ```Syncronised``` - Casts all selected spells at once
* ```Delay``` - Casts the spells with a delay of ```SPELL_DELAY``` between each
* ```DelayedBurst``` - Casts the first spell in the ```SPELLS_TO_CAST list```, and then wait ```SPELL_DELAY``` before casting the rest


## License

This project is licensed under the GNU General Public - see the [LICENSE.md](LICENSE.md) file for details.