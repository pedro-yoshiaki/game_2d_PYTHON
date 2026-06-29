# Arena Survival: The Golden Knight

**Arena Survival** is a 2D top-down survival game built with Python and Pygame. Step into the armor of the Golden Knight and face endless hordes of enraged Mages. Your goal is simple but challenging: survive the magical onslaught until the time runs out!

---

## 📖 The Lore & Objective

You play as the **Golden Knight**, trapped in an enclosed arena. Enraged Mages are spawning from all directions, relentlessly firing magic projectiles at you. 

**Your objective:** Survive for **40 seconds** without losing all your lives.

### Enemies
* **Red Mages:** Fast and dangerous. They have **2 HP** (requires 2 sword hits to defeat).
* **Purple Mages:** Tough and relentless. They have **3 HP** (requires 3 sword hits to defeat).

### The Sword Mechanic (Offense & Defense)
Your sword is your only weapon and your greatest shield. When you press the attack button, the Golden Knight performs a **360-degree circular slash**. 
* **Offense:** Instantly damages any mage or projectile caught in the radius.
* **Defense:** While the sword slash is active, the Knight becomes temporarily **invincible**, allowing you to dash through enemy fire or escape tight corners unharmed.

---

## 🎮 Controls

The game features intuitive controls and supports both WASD and Arrow keys.

| Action | Key |
| :--- | :--- |
| **Move Up** | `W` or `Up Arrow` |
| **Move Down** | `S` or `Down Arrow` |
| **Move Left** | `A` or `Left Arrow` |
| **Move Right** | `D` or `Right Arrow` |
| **Attack / Defend**| `SPACE` |
| **Select (Menu)** | `ENTER` |
| **Exit Game** | `ESC` (in menu) |

---

## 🛠️ Technical Architecture

This project was developed as an academic assignment for the Applied Programming Language course. It was built focusing on clean code and robust Software Engineering principles:

* **Engine:** Python 3 + Pygame.
* **Factory Pattern:** Centralized creation of entities (Player, Mages) via an `EntityFactory` to ensure scalable object instantiation.
* **Mediator Pattern:** Complex collision logic (Sword vs. Enemy, Enemy vs. Player) is handled by an `EntityMediator`, keeping entity classes fully decoupled.
* **Parallax UI:** The main menu features a dynamic, multi-layered parallax scrolling background.
* **Data-Driven Design:** Entity attributes (HP, Speed, Damage, Paths) are isolated in a centralized `Const.py` file for easy game balancing.

---

## 🚀 How to Run (Source Code)

If you want to run the game from the source code instead of the compiled `.exe`:

1. Ensure you have **Python 3.12+** installed on your machine.
2. Clone this repository or extract the project folder.
3. (Optional but recommended) Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: .\venv\Scripts\activate

   
   
   Install the required dependencies and run the main script:
    ```bash
   pip install pygame

   python main.py

