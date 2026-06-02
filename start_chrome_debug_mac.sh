#!/bin/bash
echo "=========================================="
echo "  HUST Auto Course - Browser Launcher"
echo "=========================================="
echo ""
echo " Enter the URL you want to visit:"
echo " (Press Enter for HUST default)"
echo ""
read -p "URL: " target_url

if [ -z "$target_url" ]; then
    target_url="https://smartcourse.hust.edu.cn"
fi

# 添加https前缀
if [[ ! "$target_url" =~ ^http ]]; then
    target_url="https://$target_url"
fi

echo ""
echo "Starting Chrome Debug Mode..."
echo "Target: $target_url"
echo ""

# Close existing Chrome
pkill -f "Google Chrome" 2>/dev/null

# Wait 3 seconds
sleep 3

# Start Chrome with debug port
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
    --remote-debugging-port=9222 \
    --remote-allow-origins=* \
    --user-data-dir="$HOME/chrome_debug_temp" \
    "$target_url" &

echo ""
echo "=========================================="
echo "  Chrome started successfully!"
echo "  Debug port: 9222"
echo "=========================================="
echo ""
echo " Please login and open course page"
echo " Then run: python3 semi_auto_course_v6_hybrid.py"
echo ""