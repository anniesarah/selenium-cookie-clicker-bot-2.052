# Selenium Cookie Clicker Bot

This is a Python script created by using the Selenium library, specifically for the game [Cookie Clicker](https://orteil.dashnet.org/cookieclicker/).

## Version

The script is made for the 2.052 version of Cookie Clicker.
Last updated: May 6, 2024

## Features

- Auto-click on the main cookie
- Auto-purchase products and upgrades
- Different wait times between purchases based on the game stage
- Convert numbers with different formats (eg. 130,000 or 1.4 million)
- Handle common exceptions

## Requirements

- Python 3.x
- Google Chrome
- `selenium`

## Future upgrades

### 1. Game stages
Currently, the game stages (early, mid, late) are hardcoded, and the cut-off is after only 5 minutes.
I have been experimenting with an algorithm-based timeout increase system with no success.
Ideally, the algorithm should be based on the cookie-per-second of the player.

### 2. Product purchase selection
The product purchase section is quite wordy and could probably be simplified.

### 3. Version updates
The code needs to be updated to suit future versions of the game as they are released.

## Contributions
Contributions are welcome!
