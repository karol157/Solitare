# Solitaire (Terminal Edition)

A terminal-based **Solitaire (Klondike)** card game built with [Textual](https://github.com/Textualize/textual).  
Experience a rich, animated terminal UI with keyboard and mouse support, undo functionality, auto-win mode, music, and multi-language options.

---

## Features

- Classic **Klondike Solitaire** gameplay  
- Keyboard and mouse controls  
- Undo your last moves  
- Auto-win mode for effortless game completion  
- Configurable settings (music, language, difficulty, etc.)  
- English and Polish translations  
- Animated card rendering directly in the terminal  
- Sound and music playback with WAV files  
- Persistent settings saved as JSON  
- Modular, clean, and well-documented codebase  

---

## Controls

| Key / Action       | Description                   |
|--------------------|-------------------------------|
| **Tab / Mouse**    | Select cards                   |
| **Enter / Click**  | Select or move card            |
| **R**              | Reset the game                 |
| **U**              | Undo last move                 |
| **Escape**         | Return to menu or exit         |
| **Auto Win**       | Automatically complete game if possible |

---

## Installation

### Requirements

- Python 3.9 or newer  
- [Textual](https://github.com/Textualize/textual)  
- [simpleaudio](https://github.com/hamiltron/py-simple-audio)  
- See `requirements.txt` for full dependency list  

### Setup

1. Install dependencies:  

   **Automatic (Linux):**  
   ```bash
   python lucher.py
   ```

   **Automatic (Windows):**
  
   ```cmd
   py lucher.py
   ```
  
   **Manual installation:**
  
   ```bash
   pip install -r requirements.txt
   ```

2. Run the game:

   ```bash
   python luncher.py
   ```
   ```cmd
   py luncher.py
   ```

---

## Project Structure

```
game/
├── Board.py             # Main game board and screen
├── card/                # Card widgets, models, rendering, validation, movement
├── menu/                # Main menu, settings, instructions screens
├── Information.py       # Timer and score display
├── Settings.py          # Persistent settings manager
├── music.py             # Music playback
├── translator.py        # Localization and translations
├── undo.py              # Undo functionality
└── win.py               # Win screen

src/
└── *.tcss               # Theming and style files

locales/
└── en.json, pl.json     # Translation files

musics/
└── *.wav                # Music files for menu and gameplay
```

---

## Configuration

Settings are stored in `game/config/settings.json` and can be changed through the in-game settings menu.

---

## Credits

* Built with [Textual](https://github.com/Textualize/textual)
* Card rendering and logic by the project author
* Music playback via [simpleaudio](https://github.com/hamiltron/py-simple-audio)

---



