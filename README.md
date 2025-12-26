# File System Dungeon 

**Trun your file system into a dungeon crawler RPG!**

File System Dungeon is a terminal-based RPG where your folders are rooms, files are enemies, and your hard drive is the world map. Explore your computer, battle "Constructs" (code), "Illusions" (images), and "Bosses" (executables), and loot them for XP and glory.

<img width="747" height="631" alt="Screenshot 2025-12-17 005455" src="https://github.com/user-attachments/assets/ff68092d-a26d-477a-b391-f55e5a555025" />

<img width="455" height="572" alt="Screenshot 2025-12-17 005429" src="https://github.com/user-attachments/assets/e40270ce-3397-4524-a1f6-20253dcbc923" />



## Features

*   **Explore Real Directories**: Navigate your actual file system as a dungeon map.
*   **Turn-Based Combat**: Fight files based on their size and type.
*   **RPG Progression**: gain XP, level up, and increase your HP.
*   **Inventory System**: Loot the essence of defeated files.
*   **Lore System**: Read text files to gain "Ancient Knowledge" (XP).
*   **Safe**: Defeated files are marked in the save files, **NOT** deleted from your disk.

## Installation

1.  **Prerequisites**: Python 3.10+
2.  **Clone the Repository**:
    ```bash
    git clone https://github.com/maverickkamal/File-System-Dungeon.git
    cd File-System-Dungeon
    ```
3.  **Set up a Virtual Environment** (Recommended):
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # macOS/Linux
    source .venv/bin/activate
    ```
4.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    (Main dependencies: `textual`, `rich`)

## How to Run the Game

Start the game from the root directory:
```bash
python main.py
```

See [GAMEPLAY.md](GAMEPLAY.md) for detailed controls and mechanics.

