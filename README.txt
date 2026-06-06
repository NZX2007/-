Auto Course Player - User Guide
==========================================

Files:
==========
1. start_edge_debug.bat    - Start browser (Windows)
2. start_chrome_debug_mac.sh - Start browser (Mac)
3. 1.py                     - Main script

==========================================

Windows Usage:
==========

Step 1: Start Browser
----------------
Double click: start_edge_debug.bat

Step 2: Run Script
----------------
Open CMD (Win+R, type cmd, enter):
cd C:\Users\23327\Desktop\auto_course_player
py 1.py

Step 3: Type y to confirm

Step 4: Position Mouse
----------------
During 10 seconds countdown, move mouse to video center

Step 5: Auto Play
----------------
Script will auto play, monitor, and switch to next section

==========================================

Mac Usage:
==========

Open Terminal:
cd ~/Desktop/auto_course_player
chmod +x start_chrome_debug_mac.sh
./start_chrome_debug_mac.sh

python3 1.py

==========================================

Important:
==========
- Do NOT resize browser window after starting!
- Do NOT minimize browser window!
- Mouse can move freely during playback
- Browser will auto come to front when switching

==========================================

Stop:
==========
Press ESC key

==========================================

Features:
==========
- Auto detect video
- Auto click play
- Auto switch to next section
- Auto handle quiz pages
- Auto install dependencies

==========================================