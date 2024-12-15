# Save them all
Simple text roguelike game. </br>
Player tries to save the main character's brother from a dungeon full of monsters. </br>
You choose the strategy - attack or negotiate. 

## Launch game
### Prerequisites
You need docker to run the game. </br>
Follow these steps to choose platform and install - https://docs.docker.com/engine/install/ 

### Run commands
Build application image locally
```commandline
docker build . -t sta:v0.0.1
```

Run container with the game
```commandline
docker run --rm -it sta:v0.0.1
```

Exit game
```commandline
CTRL + C
```
or
```commandline
4 - exit
```

## Gameplay
To find your brother you need to move through dungeon rooms full of unknown danger and treasures. </br>
Player choose action from list to progress. Choose wisely, since each monster have its weak and strong sides. </br>

### Actions list
**Attack** - try to beat a monster with your **ATK**. If foe has more **HP** than your attack it will counter-attack. </br>
**Negotiate** - try to pay off the foe with your **Gold**. **CHA** affects price of payoff </br>
**Use potion** - heal using a potion if you have one. Maximum is 1 potion, which can be found in rooms. </br>

### Upgrades
Character will become stronger as well as monsters, so choose upgrades based on your resources. </br>
You can choose between **+2 HP**, **+1 ATK** and **+1 CHA**.
