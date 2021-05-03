# Monopoly 
## You V. Machine

> ### The Game

![](https://www.worldofmonopoly.com/northamerica/usa/country/info/images/rules/1940/1940-star.jpg)

> Starting the Game

- Run GameWindow.py

# Interacting with the Game UI

> Select Token and Start Game
- Starting the game will bring to you an initial screen where you will be prompted to select a token. Click on the token you wish to play. This action will start the game
    

> Game Buttons (*Every Turn*)
- Roll 
    - Click this button to roll the dice. You may only do this once per turn. Your token will be advanced automatically and your dice roll will be display on the board visually with tow dice.
- Build 
    - Click this button to launch a window that displays a drop down of buildable properties. If a property is buildable select it from the drop down and push the select button. This will close the window and build a house/hotel on the selected property if sufficient funds exist.
- Mortgage 
    - Click this button to launch a window that diplays player properties that can either be mortgaged or un-mortgaged. Select desired property from dropdown and push the select button. This will mortgage-un-mortgage the selected property  
- End Turn
    - Click this button to end player turn. You will not be able to use this button if you have not rolled, paid tax due, paid rent due, or played chance or community chest card.

> Game Buttons (*Turn Specific*)

- Purchase
    - If a property is purchasable this button will be displayed. Click this button to acquire the property, if you have sufficient funds the property will be added to your inventory
- Pay Rent
    - If you land on a property owned by the machine you will need to pay them rent. Click this tile to pay rent. If you do not have sufficient funds to pay rent in your wallet you will be prompted to go bankrupt. You may not end your turn until you have paid rent
- Pay Tax
    - If you land on a tax tile this button will be displayed. Click this button to pay tax due. If you do not have sufficient funds to pay tax in your wallet you will be prompted to go bankrupt. You may not end your turn until tax is paid. 
- Play Card
    - If you have landed on a Community Chest or Chance tile this button will be displayed. Click this button to display card and play the action on it. You cannot end your turn until you have played the card.
- Pay Bail (*optional* & *required*)
    - If you are in jail you have the option to pay bail. If you have exhausted your rolls to roll your way out of jail it is required that you pay bail. You can choose to pay bail optionally rather than rolling your way to freedom
- Jail Card (*optional* & *required*)
    - If you are in jail and possess a get out of jail free card you may choose to play it. After you have exhausted all of your rolls to roll your way out of jail the button will display required rather than optional
- Go To Jail
    - If you land on the Go to Jail Tile this button will appear. Clicking it will transport you to the In Jail tile. You cannot end your turn until you have clicked this button.
- Go Bankrupt
    - If you try to pay rent, pay tax, or pay bail and do not have sufficient funds in your account this button will appear. Clicking it will end the game for you. You may be able to mortgage properties to stay in the game.

> Other Features (*Always Available*)
    
- Player Icon 
    - Clicking on a player's icon will display a window with the players inventory sorted by color. If the player has a get out of jail free card this will also be displayed here. Additionally the players walled will be displayed in this window. You can click on your icon as well as the machines.
    
- Sound Control
    - Clicking the speaker icon in the upper right corner will mute/un-mute all game sounds
   
> Non Features

- Trading 
    - For this iteration of the game trading has not been implemented
- Auction 
    - For this iteration of the game auctioning properties has not been implemented
- Selling Houses 
    -  For this iteration of the game selling houses has not been implemented
> Acknowledgements

- Buttons
    - https://www.youtube.com/watch?v=4_9twnEduFA

- Tokens and Icons    
    - <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

- Sounds
    - <a href="https://freesound.org/people/Jofae/" target="_top">Button Sound</a>
    - <a href="https://freesound.org/people/kiddpark/sounds/201159/" target="_top">Cash Register</a>
    - <a href="https://freesound.org/people/Migfus20/sounds/567112/" target="_top">Game Soundtrack</a>
    - <a href="https://freesound.org/people/nettimato/sounds/353975/" target="_top">Dice Roll</a>
    
- *Initial* CSV Files
  - <a href="https://github.com/hitchhiker744/monopoly_math/blob/main/chance_cards.csv" target="_top">CSV: Tiles & Cards</a>
