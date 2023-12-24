# DBZ_LSW-command_line

DBZ LSW command line demake. 

Everything done through printing special characters (ANSI escape codes) to the command line. 
See : https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
Display could be messy with custom command line settings.
Tested only with Python 3.11.1 on Windows 10.

### Prerequisites

* Python3 : Developped with python 3.11.1 but older versions should work too. 


### Installation

1. Clone the repo :
   ```sh
   git clone https://github.com/Ilmeurtalafin/DBZ_LSW-command_line.git
   ```
   Or download the sources manually.
   
3. Inside the cloned/downloaded folder, create a virtual environment :
   ```sh
   python -m venv myvenv
   ```
4. Activate the virtual environment :
   ```sh
   ./myvenv/Scripts/activate
   ```
5. Install dependencies from requirements.txt :
   ```sh
   pip install -r .\requirements.txt
   ```
6. Run  `main.py` to launch the game
   ```sh
   python ./main.py
   ```
Only steps 4 and 6 are required when re-launching the game

### Commands
- Validate : Enter
- Back : Escape
- Move in menus with arrow keys
