# Auto Course Player

A Python script that automatically plays video courses, monitors playback progress, and switches to the next section.

## Features

- Auto detect and play videos
- **NEW: Auto detect multiple videos on same page** - plays all videos before moving to next section
- **NEW: Auto scroll to video** - scrolls page to bring video into view before playing
- **NEW: Dynamic mouse click** - calculates correct click position for each video
- Auto monitor playback progress
- Auto click "Next Section" button
- Auto handle quiz/answer pages
- Mouse is free to move during playback
- Browser auto comes to front when switching sections
- Auto install dependencies

## File Structure

```
auto_course_player/
├── 1.py                    - Main script
├── start_edge_debug.bat    - Start browser (Windows)
├── start_chrome_debug_mac.sh - Start browser (Mac)
└── README.md               - This file
```

## Windows Usage

### Step 1: Start Browser

1. Double click `start_edge_debug.bat`
2. Enter the URL you want to visit (or press Enter for default: `https://smartcourse.hust.edu.cn`)
3. Edge browser will open in debug mode

**Note:** The CMD window will stay open. Do NOT close it until you finish using the script.

### Step 2: Login and Navigate

1. Login to your course platform
2. Navigate to the course learning page (where videos are displayed)
3. Make sure you can see:
   - The **video player**
   - The **"Next Section" button** (or similar text like "下一节", "下一课", "继续学习")

### Step 3: Run the Script

Open a **new CMD window** (Win+R, type `cmd`, press Enter):

```cmd
cd C:\Users\23327\Desktop\auto_course_player
py 1.py
```

### Step 4: Confirm Ready

When prompted:
```
是否已经打开了课程学习页面？
准备好后输入 y
```
Type `y` and press Enter.

### Step 5: Position Your Mouse (IMPORTANT!)

During the **10 seconds countdown**:
```
还有 10 秒将开始自动刷课...
还有 9 秒将开始自动刷课...
...
```

**Do the following:**

1. Move your mouse to the **center of the video player**
2. This position will be recorded as a fallback for clicking
3. Keep the mouse there until countdown finishes

**Note:** The script now dynamically calculates click positions for each video, but the initial position is still used as a fallback.

### Step 6: Script Runs Automatically

After countdown finishes, the script will:
1. Inject mouse-detection bypass scripts
2. Detect all videos on the page
3. Auto scroll to each video
4. Auto-click to play
5. Monitor playback progress
6. When a video ends, check for more videos on same page
7. If more videos found, scroll and play them
8. When all videos on page are done, click "Next Section"

**During playback:**
- Your mouse is **FREE to move** (you can do other things)
- The script uses JavaScript injection to bypass mouse detection
- Browser can be in background (but NOT minimized)

**When switching videos:**
- Script will auto scroll to the next video
- Mouse click position is calculated dynamically
- Browser will **automatically come to front** when switching sections

### Step 7: Stop the Script

Press **ESC key** at any time to stop.

## Mac Usage

Open Terminal:
```bash
cd ~/Desktop/auto_course_player
chmod +x start_chrome_debug_mac.sh
./start_chrome_debug_mac.sh

python3 1.py
```

Follow the same steps as Windows (Steps 4-7).

## Important Notes

### DO NOT:
- ❌ Resize browser window after starting
- ❌ Minimize browser window
- ❌ Close the CMD window that started Edge

### DO:
- ✅ Position mouse correctly during countdown (fallback)
- ✅ Make sure "Next Section" button is visible
- ✅ Let script run uninterrupted
- ✅ Press ESC to stop when needed

### Multi-Video Detection:

If a page has multiple videos, the script will:
1. Detect how many videos are on the page
2. Play them one by one
3. Auto scroll to each video before playing
4. Only click "Next Section" after ALL videos are done

## Troubleshooting

### "Browser not running" error:
- Make sure you ran `start_edge_debug.bat`
- Check if Edge is actually open (look at taskbar)

### "Auto play failed":
- The script now uses multiple methods to click (JS + real mouse click)
- Try clicking manually once, script will continue

### "Video not found":
- Make sure you're on a video learning page
- Wait a few seconds for page to load

### Script plays only one video when there are multiple:
- This issue has been fixed
- Script now properly detects and plays all videos on the page

### Script stops unexpectedly:
- Pressed ESC accidentally
- Browser window was resized/minimized

## Dependencies

The script auto-installs these:
- websocket-client
- requests
- pynput
- pyautogui
- pywin32 (Windows only)

## License

MIT License - Free to use and modify.

## Author

Created for automated course learning (HUST).

## Changelog

### Latest Version
- Added: Multi-video detection on same page
- Added: Auto scroll to video before playing
- Added: Dynamic mouse click position calculation
- Fixed: Script now plays all videos before moving to next section
