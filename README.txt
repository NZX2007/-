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
(This is now a fallback - script calculates positions dynamically)

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

NEW Features (Multi-Video Support):
==========
- Auto detect multiple videos on same page
- Auto scroll to each video before playing
- Play all videos before moving to next section
- Dynamic click position calculation for each video

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
- Auto detect video (single or multiple)
- Auto scroll to video
- Auto click play
- Auto switch to next video on same page
- Auto switch to next section
- Auto handle quiz pages
- Auto install dependencies

==========================================

Troubleshooting:
==========
If only one video plays when there are multiple:
- This issue has been fixed in the latest version
- Script now properly detects and plays all videos

If video doesn't auto-play:
- Script uses multiple methods (JS + real click)
- Try manual click once, script will continue

==========================================
