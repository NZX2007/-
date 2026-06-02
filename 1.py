# 自动安装依赖
import subprocess
import sys
import platform

def install_dependencies():
    packages = ['websocket-client', 'requests', 'pynput', 'pyautogui']
    # Windows需要pywin32
    if platform.system() == 'Windows':
        packages.append('pywin32')
    for package in packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            print(f"正在安装 {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '-q'])

install_dependencies()

import json
import requests
import websocket
import time
import pyautogui
from pynput import keyboard

is_windows = platform.system() == 'Windows'

pyautogui.FAILSAFE = True
running = True

def on_release(key):
    global running
    if key == keyboard.Key.esc:
        print("\n\n*** 用户按ESC停止 ***")
        running = False
        return False

listener = keyboard.Listener(on_release=on_release)
listener.start()

print("=" * 60)
print("  视频课程自动刷课脚本（华中大特供）")
print("  按 ESC 键停止")
print("=" * 60)

try:
    pages = requests.get('http://localhost:9222/json', timeout=5).json()
except:
    print("\n错误：浏览器未运行，请先运行 start_edge_debug.bat！")
    listener.stop()
    sys.exit(1)

all_pages = [p for p in pages if p.get('type') == 'page']
if not all_pages:
    print("错误：未找到页面")
    listener.stop()
    sys.exit(1)

page = all_pages[0]
ws_url = page['webSocketDebuggerUrl']
current_url = page.get('url', '')
print(f"\n当前页面: {current_url[:60]}...")

ws = websocket.create_connection(ws_url)
msg_id = 1
video_count = 0
total_time = 0
video_center_x = None
video_center_y = None
window_id = None  # 保存窗口ID

def send_cmd(method, params=None):
    global msg_id
    cmd = {"id": msg_id, "method": method}
    if params:
        cmd["params"] = params
    ws.send(json.dumps(cmd))
    msg_id += 1
    while True:
        result = json.loads(ws.recv())
        if result.get('id') == msg_id - 1:
            return result

def format_time(seconds):
    if not seconds or seconds <= 0:
        return "??:??"
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m}:{s:02d}"

def bring_browser_to_front():
    """把浏览器窗口置顶"""
    try:
        if is_windows:
            # Windows: 使用win32gui
            import win32gui
            import win32con

            def callback(hwnd, hwnds):
                if win32gui.IsWindowVisible(hwnd):
                    title = win32gui.GetWindowText(hwnd)
                    # 清理特殊字符后匹配
                    clean_title = title.replace('​', '')
                    if 'Edge' in clean_title or 'Chrome' in clean_title:
                        hwnds.append((hwnd, clean_title))
                return True

            hwnds = []
            win32gui.EnumWindows(callback, hwnds)

            if hwnds:
                hwnd, title = hwnds[0]
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)
                print(f"  已切换到浏览器")
            else:
                print("  未找到浏览器窗口")
        else:
            # Mac: 使用AppleScript
            import os
            os.system('''osascript -e 'tell application "Google Chrome" to activate' ''')
            print("  已切换到浏览器")
    except Exception as e:
        print(f"  切换失败: {e}")

print("\n" + "-" * 60)
print(" 是否已经打开了课程学习页面？")
print(" 准备好后输入 y")
print("-" * 60)
user_input = input("\n输入 y 开始: ").strip().lower()
if user_input != 'y':
    print("已取消。")
    listener.stop()
    ws.close()
    sys.exit(0)

print("\n" + "-" * 60)
print(" 请将鼠标移动至视频的中心位置！")
print(" 脚本将记录此位置用于自动点击播放")
print("-" * 60)
for i in range(10, 0, -1):
    print(f"\r  还有 {i} 秒将开始自动刷课...  ", end="", flush=True)
    time.sleep(1)

video_center_x, video_center_y = pyautogui.position()
print(f"\n\n鼠标位置已记录: ({video_center_x}, {video_center_y})")

print("\n*** 重要提示：开始之后请不要调整浏览器窗口大小！***")
print("*** 不要最小化浏览器窗口！否则点击位置会偏移！***")

send_cmd("Page.enable")
send_cmd("Runtime.enable")
send_cmd("Input.enable")

def deep_inject():
    send_cmd("Runtime.evaluate", {
        "expression": """
        (function() {
            function injectDeep(win, depth) {
                if (depth > 5) return;
                try {
                    const doc = win.document;
                    ['mouseleave', 'mouseout', 'pointerleave', 'pointerout', 'visibilitychange', 'blur'].forEach(e => {
                        doc.addEventListener(e, ev => { ev.stopImmediatePropagation(); ev.preventDefault(); }, true);
                    });
                    const videos = doc.querySelectorAll('video');
                    videos.forEach(v => {
                        v.setAttribute('data-mouse-over', 'true');
                        setInterval(() => {
                            const rect = v.getBoundingClientRect();
                            v.dispatchEvent(new MouseEvent('mouseenter', {bubbles:true, cancelable:true, view:win, clientX:rect.x+rect.width/2, clientY:rect.y+rect.height/2}));
                        }, 1000);
                        v.addEventListener('mouseleave', e => e.stopImmediatePropagation(), true);
                        v.addEventListener('mouseout', e => e.stopImmediatePropagation(), true);
                    });
                    if (win.frames) for (let i = 0; i < win.frames.length; i++) {
                        try { injectDeep(win.frames[i], depth+1); } catch(e) {}
                    }
                } catch(e) {}
            }
            injectDeep(window, 0);
            return "OK";
        })()
        """
    })

def get_video_status():
    result = send_cmd("Runtime.evaluate", {
        "expression": """
        (function() {
            function findVideo(win) {
                try {
                    let videos = win.document.querySelectorAll('video');
                    for (let v of videos) {
                        return {
                            found: true,
                            paused: v.paused,
                            currentTime: v.currentTime,
                            duration: v.duration,
                            ended: v.ended
                        };
                    }
                    if (win.frames) for (let i = 0; i < win.frames.length; i++) {
                        try {
                            let r = findVideo(win.frames[i]);
                            if (r) return r;
                        } catch(e) {}
                    }
                } catch(e) {}
                return null;
            }
            return JSON.stringify(findVideo(window) || {found: false});
        })()
        """
    })
    return json.loads(result['result']['result'].get('value', '{}'))

def click_video_real():
    global video_center_x, video_center_y
    if video_center_x and video_center_y:
        pyautogui.click(video_center_x, video_center_y)
        return True
    return False

def play_video_js():
    send_cmd("Runtime.evaluate", {
        "expression": """
        (function() {
            function playVid(win) {
                try {
                    let videos = win.document.querySelectorAll('video');
                    for (let v of videos) { v.play().catch(()=>{}); }
                    if (win.frames) for (let f of win.frames) playVid(f);
                } catch(e) {}
            }
            playVid(window);
        })()
        """
    })

def click_next_video():
    result = send_cmd("Runtime.evaluate", {
        "expression": """
        (function() {
            const nextTexts = ['下一节', '下一课', '下一集', '下一P', '下一个', 'next', 'Next', '继续', '继续学习'];
            function findAndClick(win) {
                try {
                    for (let sel of ['button', 'a', 'div', 'span', 'li']) {
                        for (let el of win.document.querySelectorAll(sel)) {
                            let text = (el.innerText || el.textContent || '').trim();
                            for (let n of nextTexts) {
                                if (text === n && el.offsetWidth > 0) { el.click(); return {found: true, text: text}; }
                            }
                        }
                    }
                    if (win.frames) for (let i = 0; i < win.frames.length; i++) {
                        try {
                            let iframe = win.document.querySelectorAll('iframe')[i];
                            if (iframe) {
                                let r = findAndClick(win.frames[i]);
                                if (r) return r;
                            }
                        } catch(e) {}
                    }
                } catch(e) {}
                return null;
            }
            return JSON.stringify(findAndClick(window) || {found: false});
        })()
        """
    })
    return json.loads(result['result']['result'].get('value', '{}'))

def scroll_to_bottom():
    send_cmd("Runtime.evaluate", {"expression": "for(let w=window;w;w=w.frames[0]){try{w.scrollTo(0,w.document.body.scrollHeight);}catch(e){}}"})
    time.sleep(0.5)

print("\n注入鼠标防暂停脚本...")
deep_inject()
time.sleep(1)
print("准备就绪！")
print("\n*** 开始自动刷课！按 ESC 键停止 ***")
print("*** 鼠标在播放期间可以自由移动 ***\n")

try:
    while running:
        video_count += 1
        print(f"\n{'='*50}")
        print(f" 视频 #{video_count}")
        print(f"{'='*50}")

        # ===== 搜索视频并播放 =====
        print("\n正在搜索视频...")
        waited = 0
        click_attempts = 0
        max_click_attempts = 5

        while waited < 60 and running:
            time.sleep(1)
            waited += 1

            if waited % 10 == 0:
                deep_inject()

            status = get_video_status()

            if not status.get('found'):
                print(f"\r  未找到视频... {waited}秒  ", end="", flush=True)
                continue

            current = status.get('currentTime') or 0
            paused = status.get('paused', True)
            duration = status.get('duration') or 0

            # 已在播放（必须确认不是暂停状态）
            if not paused and current > 0:
                print(f"\n  视频正在播放！{format_time(current)}/{format_time(duration)}")
                break

            # 视频暂停或没进度，尝试点击播放
            if click_attempts < max_click_attempts:
                click_attempts += 1
                status_text = f"时长 {format_time(duration)}" if duration > 0 else "加载中"
                print(f"\r  检测到视频（{status_text}），点击播放... 第 #{click_attempts} 次  ", end="", flush=True)

                # JS播放
                play_video_js()
                time.sleep(0.2)

                # 单击
                click_video_real()
                time.sleep(0.8)

                # 检查是否成功
                s2 = get_video_status()
                if s2.get('found') and not s2.get('paused', True) and s2.get('currentTime', 0) > 0:
                    print(f"\n  自动播放成功！{format_time(s2.get('currentTime', 0))}/{format_time(s2.get('duration', 0))}")
                    break

                # 单击不行，双击试试
                click_video_real()
                time.sleep(0.1)
                click_video_real()
                time.sleep(1)
            else:
                print(f"\n\n  *** 请手动点击视频播放！***")
                while running:
                    time.sleep(1)
                    s = get_video_status()
                    if s.get('found') and (s.get('currentTime', 0) > 0 or not s.get('paused', True)):
                        print("  视频已开始！")
                        break
                break

        if not running:
            break
        if waited >= 60:
            print("\n  等待超时")
            break

        # ===== 监控播放 =====
        print("\n监控播放进度...")
        last_time = 0
        stuck_count = 0

        while running:
            time.sleep(1)
            status = get_video_status()

            if status.get('found'):
                current = status.get('currentTime') or 0
                duration = status.get('duration') or 0
                paused = status.get('paused', True)
                ended = status.get('ended', False)

                if duration > 0:
                    progress = current / duration * 100
                    bar = "=" * int(progress/100*30) + "-" * (30-int(progress/100*30))
                    print(f"\r  [{bar}] {format_time(current)}/{format_time(duration)} ({progress:.0f}%) {'暂停' if paused else '播放中'}  ", end="", flush=True)

                    if paused and current < duration - 2:
                        print("\n  视频暂停，尝试恢复...")
                        play_video_js()
                        time.sleep(0.2)
                        click_video_real()
                        time.sleep(0.3)
                        click_video_real()
                        time.sleep(1)

                if abs(current - last_time) < 0.5 and not paused:
                    stuck_count += 1
                    if stuck_count >= 10:
                        click_video_real()
                        stuck_count = 0
                else:
                    stuck_count = 0
                last_time = current

                if ended or (duration > 0 and current >= duration - 1):
                    print(f"\n\n  ✓ 视频播放完成！")
                    total_time += duration
                    break

        if not running:
            break

        # ===== 点击下一节 =====
        print("\n正在查找下一节...")

        # 先把浏览器置顶，确保点击位置正确
        bring_browser_to_front()
        time.sleep(1)

        next_result = click_next_video()
        if next_result.get('found'):
            print(f"  已点击 '{next_result.get('text')}'")
            time.sleep(3)
            deep_inject()

            print("  检查下一页...")
            time.sleep(2)
            status = get_video_status()

            if status.get('found'):
                print("  ✓ 下一页有视频")
                # 再次置顶，确保点击播放时位置正确
                bring_browser_to_front()
            else:
                print("  下一页没有视频（答题区），滚动...")
                scroll_to_bottom()
                time.sleep(1)
                next_result2 = click_next_video()
                if next_result2.get('found'):
                    print(f"  再次点击 '{next_result2.get('text')}'")
                    time.sleep(3)
                    deep_inject()
                else:
                    print("  课程结束！")
                    break
        else:
            print("  课程结束！")
            break

except KeyboardInterrupt:
    print("\n\n已中断")

finally:
    listener.stop()
    ws.close()

print(f"\n{'='*50}")
print(f" 完成视频: {video_count} 个  总时长: {format_time(total_time)}")
print(f"{'='*50}")