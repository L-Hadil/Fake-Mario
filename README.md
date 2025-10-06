# Fake Mario Game

## How to Run

Run the game with:
```bash
python3 main.py
```

## Controls

- **Arrow keys**: Move player (in game), navigate menu options (in menu/game over).
- **Enter**: Select menu or game over options.

## Gameplay

- Collectibles appear randomly. Move the player to pick them up.
- Each collectible gives **+10 points**.
- Avoid enemies! Colliding with an enemy ends the game.

## Game Over

- When you collide with an enemy, the game ends.
- The final score is displayed.
- You can **Restart** or **Quit** from the Game Over screen.

## Assets

- All sprites and sounds are auto-generated as placeholders.
- No manual setup required.

## Structure

- `main.py`: Entry point, menu, game loop, transitions.
- `src/player.py`: Player movement and drawing.
- `collectible.py`: Collectible logic.
- `sprites/`: Placeholder images for player, enemy, collectible, background.
- `sounds/`: Placeholder sound effects and music.

Enjoy!