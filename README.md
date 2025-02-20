# Snake Game

This project was my final year Computer Science specialization project in Terminale (equivalent to A-level in the UK). It is a modern implementation of the classic Snake game developed in Python using the Pygame library.

## The Snake Game

Snake is a classic arcade game where the player controls a snake that continuously moves around the screen. The goal is to guide the snake to eat food (apples), which causes it to grow longer. The challenge is to avoid colliding with the screen boundaries or the snake's own body. As the snake grows, the game becomes progressively more difficult.

## Why Pygame?

I chose to use the **Pygame** library for several reasons:
- **Beginner-Friendly:** Pygame is well-documented and accessible, making it an ideal choice for educational projects.
- **2D Game Development:** It offers robust functionality for handling graphics, user input, and sound, which is perfect for creating a 2D game like Snake.
- **Community and Resources:** Pygame has a large community and plenty of tutorials, which helped me learn and troubleshoot during development.

## Key Features

- **Modern Aesthetic:**  
  The game features a contemporary design with a dark background and flat UI elements. Instead of using images, the snake and apple are rendered using geometric shapes:
  - The snake is drawn as a series of circles, with the head featuring simple eyes.
  - The apple is represented by a red circle with a small green leaf.
  
- **Customizable Options:**  
  An options menu allows the player to customize:
  - The color of the snake.
  - The color of the apple.
  - The game speed (with choices like Slow, Normal, and Fast).
  
  The options menu supports navigation via arrow keys and mouse clicks, with the current selection highlighted for clarity.

- **Pause Functionality:**  
  During gameplay, pressing the **Escape** key toggles the pause state, displaying a "Paused" message without interrupting the game flow.

- **Responsive Menus:**  
  Both the main menu and options menu feature modern design elements with smooth navigation and clear visual feedback, ensuring an intuitive user experience.

- **Game Over Screen:**  
  When the snake collides with the boundaries or itself, a Game Over screen is displayed for 750 milliseconds before returning to the main menu.

## Installation and Usage

1. **Installation:**  
   Ensure you have Python (version 3.7 min) installed on your machine. Pygame can be installed via pip:
   ```bash
   pip install pygame
   
2. **Running the Game:**
Download or clone the project repository and run the main script:
   ``` bash
   python snake_game.py

3. **Navigation:**

Use the arrow keys to control the snake.
Press Escape to pause or resume the game.
Navigate the menus using the arrow keys or your mouse, and press Enter to confirm your selection.
