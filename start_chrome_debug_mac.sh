#!/bin/bash
echo "=========================================="
echo "  Start Chrome Debug Mode"
echo "=========================================="
echo ""
echo " Enter the URL to visit (press Enter for default):"
echo ""
read -p "URL: " target_url

if [ -z "$target_url" ]; then
    target_url="https://smartcourse.hust.edu.cn"
fi

if [[ ! "$target_url" =~ ^http ]]; then
    target_url="https://$target_url"
fi

echo ""
echo "Target: $target_url"
echo ""

pkill -f "Google Chrome" 2>/dev/null

sleep 2

echo "Starting Chrome..."
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
    --remote-debugging-port=9222 \
    --remote-allow-origins=* \
    "$target_url" &

echo ""
echo "=========================================="
echo "  Chrome started!"
echo "  Debug port: 9222"
echo "=========================================="
echo ""
echo " Now run: python3 1.py"
echo ""