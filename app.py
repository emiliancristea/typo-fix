import tkinter as tk
from tkinter import Text, messagebox, ttk, simpledialog
import os
import requests
import time  # Added for delays
import pyperclip  # Added for clipboard access
import pyautogui  # Added for simulating key presses
from pynput import keyboard  # Added for global hotkey listening
import threading  # Added for running listener in a separate thread
from screeninfo import get_monitors  # Added for multi-monitor support
import win32gui
import win32con
from ctypes import windll, wintypes, byref
import ctypes
import base64
import pystray
from PIL import Image

class RoundedButton:
    def __init__(self, parent, text, command, bg_color, hover_color, text_color='white', width=80, height=35, corner_radius=8, timer_callback=None):
        self.parent = parent
        self.text = text
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.width = width
        self.height = height
        self.corner_radius = corner_radius
        self.is_hovered = False
        self.timer_callback = timer_callback
        
        # Create high-DPI canvas for better quality
        scale_factor = 2  # 2x resolution for better quality
        self.scale = scale_factor
        canvas_width = (width + 4) * scale_factor
        canvas_height = (height + 4) * scale_factor
        
        self.canvas = tk.Canvas(parent, width=width + 4, height=height + 4, 
                               highlightthickness=0, relief='flat', borderwidth=0)
        # Try to match parent's transparent background
        try:
            self.canvas.configure(bg='black')
        except:
            self.canvas.configure(bg=parent.cget('bg'))
        
        # Draw the button
        self.draw_button()
        
        # Bind events
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<Enter>', self.on_enter)
        self.canvas.bind('<Leave>', self.on_leave)
        
    def draw_button(self):
        self.canvas.delete("all")
        
        # Choose color based on hover state
        current_color = self.hover_color if self.is_hovered else self.bg_color
        
        # Button coordinates (leaving space for shadow)
        x1, y1 = 2, 2
        x2, y2 = self.width, self.height
        r = self.corner_radius
        
        # Draw shadow only when not hovered - make it more subtle
        if not self.is_hovered:
            shadow_offset = 1
            sx1, sy1 = x1 + shadow_offset, y1 + shadow_offset
            sx2, sy2 = x2 + shadow_offset, y2 + shadow_offset
            shadow_color = '#000000'  # Pure black for better contrast
            
            # Shadow rectangles
            self.canvas.create_rectangle(sx1 + r, sy1, sx2 - r, sy2, fill=shadow_color, outline='', width=0)
            self.canvas.create_rectangle(sx1, sy1 + r, sx2, sy2 - r, fill=shadow_color, outline='', width=0)
            
            # Shadow corners - use smaller radius for tighter shadow
            shadow_r = r - 1
            self.canvas.create_oval(sx1, sy1, sx1 + 2*shadow_r, sy1 + 2*shadow_r, fill=shadow_color, outline='', width=0)
            self.canvas.create_oval(sx2 - 2*shadow_r, sy1, sx2, sy1 + 2*shadow_r, fill=shadow_color, outline='', width=0)
            self.canvas.create_oval(sx1, sy2 - 2*shadow_r, sx1 + 2*shadow_r, sy2, fill=shadow_color, outline='', width=0)
            self.canvas.create_oval(sx2 - 2*shadow_r, sy2 - 2*shadow_r, sx2, sy2, fill=shadow_color, outline='', width=0)
        
        # Draw main button with anti-aliasing effect using multiple layers
        # Base layer
        self.canvas.create_rectangle(x1 + r, y1, x2 - r, y2, fill=current_color, outline='', width=0)
        self.canvas.create_rectangle(x1, y1 + r, x2, y2 - r, fill=current_color, outline='', width=0)
        
        # Perfect rounded corners using ovals
        self.canvas.create_oval(x1, y1, x1 + 2*r, y1 + 2*r, fill=current_color, outline='', width=0)
        self.canvas.create_oval(x2 - 2*r, y1, x2, y1 + 2*r, fill=current_color, outline='', width=0)
        self.canvas.create_oval(x1, y2 - 2*r, x1 + 2*r, y2, fill=current_color, outline='', width=0)
        self.canvas.create_oval(x2 - 2*r, y2 - 2*r, x2, y2, fill=current_color, outline='', width=0)
        
        # Add subtle border for definition
        border_color = self._darken_color(current_color, 0.2)
        border_width = 1
        
        # Border rectangles
        self.canvas.create_rectangle(x1 + r, y1, x2 - r, y1 + border_width, fill=border_color, outline='')
        self.canvas.create_rectangle(x1 + r, y2 - border_width, x2 - r, y2, fill=border_color, outline='')
        self.canvas.create_rectangle(x1, y1 + r, x1 + border_width, y2 - r, fill=border_color, outline='')
        self.canvas.create_rectangle(x2 - border_width, y1 + r, x2, y2 - r, fill=border_color, outline='')
        
        # Add text with better positioning
        text_x = (x1 + x2) // 2
        text_y = (y1 + y2) // 2
        
        # Use better font with anti-aliasing
        self.canvas.create_text(text_x, text_y, text=self.text, 
                               fill=self.text_color, font=('Segoe UI', 9, 'bold'), anchor='center')
    
    def _darken_color(self, color, factor):
        """Darken a hex color by a given factor"""
        if color.startswith('#'):
            color = color[1:]
        
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
        
        r = max(0, int(r * (1 - factor)))
        g = max(0, int(g * (1 - factor)))
        b = max(0, int(b * (1 - factor)))
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def on_click(self, event):
        if self.timer_callback:
            self.timer_callback()
        if self.command:
            self.command()
    
    def on_enter(self, event):
        if self.timer_callback:
            self.timer_callback()
        self.is_hovered = True
        self.draw_button()
        self.canvas.configure(cursor='hand2')
    
    def on_leave(self, event):
        self.is_hovered = False
        self.draw_button()
        self.canvas.configure(cursor='')
    
    def pack(self, **kwargs):
        self.canvas.pack(**kwargs)

class TypoFixApp:
    def __init__(self, root):
        self.root = root
        root.title("TypoFix")

        # Embedded API Key (encoded for basic obfuscation)
        self.api_key = self.get_embedded_api_key()

        if not self.api_key:
            print("ERROR: Could not initialize API key.")
            messagebox.showerror("Error", "Failed to initialize TypoFix. Please try running as administrator.")
            self.root.quit()
            return
        else:
            print("TypoFix initialized successfully.")

        # Hide the main window
        root.withdraw()

        # API Configuration
        self.gemini_api_base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        
        # --- Widget and State Management ---
        self.floating_widget = None
        self.text_to_correct_for_widget = None
        self.simulating_paste = False
        self.selection_rect = None
        self.widget_timeout_timer = None
        self.widget_timeout_seconds = 4

        # --- System Tray Setup ---
        self.setup_system_tray()

        # --- Hotkey Setup ---
        self.hotkey_combination = {keyboard.Key.ctrl, keyboard.Key.shift_l}  # Ctrl + Left Shift
        self.current_hotkey_keys = set()
        self.start_hotkey_listener()
        print(f"TypoFix is ready! Highlight text and press CTRL+LEFT SHIFT to correct typos or improve clarity.")

    def get_embedded_api_key(self):
        """Get the embedded API key"""
        try:
            # Embedded API key (base64 encoded for basic obfuscation)
            encoded_key = "QUl6YVN5RE1BYWk5VndoMUpySEZIQXQzWlJoWjM5MHgtM25LRWpJ"  # Your actual encoded key
            
            decoded = base64.b64decode(encoded_key).decode()
            
            # Basic validation
            if len(decoded) > 20 and decoded.startswith("AIza"):
                return decoded
            else:
                # If there's still an issue with the key
                messagebox.showerror("Error", "Failed to initialize TypoFix. Please contact support.")
                return None
                
        except Exception as e:
            print(f"Error decoding API key: {e}")
            messagebox.showerror("Error", "Failed to initialize TypoFix. Please try running as administrator.")
            return None

    def get_text_selection_position(self):
        """Try to get the position of selected text using various Windows APIs"""
        try:
            # Method 1: Try to get selection using UI Automation
            try:
                import comtypes.client
                
                # Initialize COM
                comtypes.CoInitialize()
                
                # Get UI Automation
                uia = comtypes.client.CreateObject("UIAutomation.CUIAutomation")
                
                # Get the focused element
                focused_element = uia.GetFocusedElement()
                
                if focused_element:
                    # Try to get text pattern
                    try:
                        text_pattern = focused_element.GetCurrentPattern(uia.UIA_TextPatternId)
                        if text_pattern:
                            # Get selection
                            selections = text_pattern.GetSelection()
                            if selections.Length > 0:
                                selection = selections.GetElement(0)
                                # Get bounding rectangle
                                rect = selection.GetBoundingRectangles()
                                if len(rect) >= 4:
                                    # Return top-left of selection
                                    return (int(rect[0]), int(rect[1]))
                    except:
                        pass
                    
                    # Fallback: get element's bounding rectangle
                    try:
                        rect = focused_element.CurrentBoundingRectangle
                        # Return center-top of the focused element
                        return (int(rect.left + rect.width/2), int(rect.top))
                    except:
                        pass
                        
            except ImportError:
                print("COM/UI Automation not available, using fallback method")
            except Exception as e:
                print(f"UI Automation error: {e}")
            
            # Method 2: Enhanced caret position detection
            try:
                # Get the foreground window (active window)
                hwnd = win32gui.GetForegroundWindow()
                
                # Try to get caret position
                caret_pos = win32gui.GetCaretPos()
                if caret_pos and caret_pos != (0, 0):
                    # Convert to screen coordinates
                    screen_pos = win32gui.ClientToScreen(hwnd, caret_pos)
                    print(f"Got caret position: {screen_pos}")
                    return screen_pos
                
                # Method 3: Try to get cursor position from focused window
                import ctypes
                from ctypes import wintypes
                
                # Get cursor position in focused window
                class POINT(ctypes.Structure):
                    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
                
                point = POINT()
                if ctypes.windll.user32.GetCursorPos(ctypes.byref(point)):
                    # Check if this is inside the active window
                    window_rect = win32gui.GetWindowRect(hwnd)
                    if (window_rect[0] <= point.x <= window_rect[2] and 
                        window_rect[1] <= point.y <= window_rect[3]):
                        print(f"Using cursor position inside active window: ({point.x}, {point.y})")
                        return (point.x, point.y)
                
                # Method 4: Get approximate position from window center
                rect = win32gui.GetWindowRect(hwnd)
                window_center_x = rect[0] + (rect[2] - rect[0]) // 2
                window_top_area = rect[1] + 100  # Approximate content area
                print(f"Using window-based approximation: ({window_center_x}, {window_top_area})")
                return (window_center_x, window_top_area)
                
            except Exception as e:
                print(f"Enhanced position detection error: {e}")
            
        except Exception as e:
            print(f"Could not get text selection position: {e}")
        
        # Final fallback to mouse position
        mouse_pos = pyautogui.position()
        print(f"Using mouse position as final fallback: {mouse_pos}")
        return mouse_pos

    def start_hotkey_listener(self):
        listener_thread = threading.Thread(target=self._run_listener, daemon=True)
        listener_thread.start()

    def _on_press(self, key):
        try:
            # More robust key detection - ignore all keys when simulating actions
            if hasattr(self, 'simulating_paste') and self.simulating_paste:
                return

            # Handle Ctrl key detection
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r or key == keyboard.Key.ctrl:
                self.current_hotkey_keys.add(keyboard.Key.ctrl)
                print(f"DEBUG: Ctrl key detected and added to set. CurrentSet: {self.current_hotkey_keys}")
            
            # Handle Left Shift key detection
            elif key == keyboard.Key.shift_l:
                self.current_hotkey_keys.add(keyboard.Key.shift_l)
                print(f"DEBUG: Left Shift key detected and added to set. CurrentSet: {self.current_hotkey_keys}")
            
            # Check if we have the complete hotkey combination (Ctrl + Left Shift)
            if self.hotkey_combination.issubset(self.current_hotkey_keys):
                print(f"DEBUG: Hotkey combination DETECTED! CurrentSet: {self.current_hotkey_keys}")
                self._handle_hotkey_action()
                
        except Exception as e:
            print(f"DEBUG: Error in _on_press: {e}")

    def _on_release(self, key):
        try:
            # Ignore all keys when simulating actions
            if hasattr(self, 'simulating_paste') and self.simulating_paste:
                return

            # Handle Ctrl key release
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r or key == keyboard.Key.ctrl:
                try:
                    self.current_hotkey_keys.discard(keyboard.Key.ctrl)
                    print(f"DEBUG: Ctrl key released. CurrentSet: {self.current_hotkey_keys}")
                except:
                    pass
            
            # Handle Left Shift key release
            elif key == keyboard.Key.shift_l:
                try:
                    self.current_hotkey_keys.discard(keyboard.Key.shift_l)
                    print(f"DEBUG: Left Shift key released. CurrentSet: {self.current_hotkey_keys}")
                except:
                    pass
                    
        except Exception as e:
            print(f"DEBUG: Error in _on_release: {e}")

    def _run_listener(self):
        with keyboard.Listener(on_press=self._on_press, on_release=self._on_release) as listener:
            listener.join()

    def _handle_hotkey_action(self):
        print("Ctrl+Left Shift hotkey detected!") 
        if self.floating_widget: # Prevent multiple widgets if one exists
            print("INFO: Widget already exists. Ignoring hotkey.")
            self.current_hotkey_keys.clear()
            return
        
        try:
            # Get text selection position first
            self.selection_rect = self.get_text_selection_position()
            
            # Simulate Ctrl+C to copy any selected text
            print("Simulating Ctrl+C to copy selected text...")
            self.simulating_paste = True  # Prevent our listener from interfering
            pyautogui.hotkey('ctrl', 'c')
            self.simulating_paste = False
            
            # Wait for clipboard to update
            time.sleep(0.3) 
            copied_text = pyperclip.paste()
            
            if copied_text and copied_text.strip():
                print(f"Captured text from clipboard: '{copied_text}'")
                self.text_to_correct_for_widget = copied_text
                self.root.after(0, self._show_floating_correction_widget)
            else:
                print("No text found on clipboard - please highlight text first.")

        except Exception as e:
            print(f"Error in hotkey action: {e}")
        
        self.root.after(50, self.current_hotkey_keys.clear)

    def _show_floating_correction_widget(self):
        print("DEBUG: _show_floating_correction_widget called")
        
        # Destroy any existing widget
        if self.floating_widget and self.floating_widget.winfo_exists():
            self.floating_widget.destroy()
        
        # Create a new Toplevel window (now with 3 buttons)
        self.floating_widget = tk.Toplevel(self.root)
        self.floating_widget.title("")  # No title for minimal look
        
        # Widget dimensions - wider to accommodate 3 buttons
        widget_width = 280  # Wider for three buttons
        widget_height = 50   # Same height
        
        # Use text selection position instead of mouse position
        if self.selection_rect:
            base_x, base_y = self.selection_rect
            print(f"Using detected selection position: ({base_x}, {base_y})")
        else:
            base_x, base_y = pyautogui.position()
            print(f"No selection detected, using mouse position: ({base_x}, {base_y})")
        
        # Position widget above the selected text with better logic
        pos_x = base_x - widget_width // 2  # Center horizontally on selection
        pos_y = base_y - widget_height - 20  # Position above the selection with more space
        
        # Keep widget on screen with improved bounds checking
        monitors = get_monitors()
        active_monitor = monitors[0]  # Default to primary
        for m in monitors:
            if m.x <= base_x < m.x + m.width and m.y <= base_y < m.y + m.height:
                active_monitor = m
                break
        
        print(f"Active monitor: {active_monitor.x}, {active_monitor.y}, {active_monitor.width}x{active_monitor.height}")
        
        # Adjust position to keep widget fully on screen
        if pos_x + widget_width > active_monitor.x + active_monitor.width:
            pos_x = active_monitor.x + active_monitor.width - widget_width - 10
            print("Adjusted X position to fit on screen (right edge)")
        if pos_x < active_monitor.x:
            pos_x = active_monitor.x + 10
            print("Adjusted X position to fit on screen (left edge)")
        
        # For Y position, if there's no room above, show below
        if pos_y < active_monitor.y + 10:
            pos_y = base_y + 25  # Show below selection if no room above
            print("Not enough room above, showing below selection")
        
        # Final bounds check for Y
        if pos_y + widget_height > active_monitor.y + active_monitor.height:
            pos_y = active_monitor.y + active_monitor.height - widget_height - 10
            print("Adjusted Y position to fit on screen (bottom edge)")
        
        self.floating_widget.geometry(f"{widget_width}x{widget_height}+{pos_x}+{pos_y}")
        
        # Minimal widget styling - transparent background
        self.floating_widget.configure(bg='black')  # Will be made transparent
        self.floating_widget.attributes('-topmost', True)  # Keep on top
        self.floating_widget.resizable(False, False)
        self.floating_widget.overrideredirect(True)  # Remove window decorations
        
        # Try to make the background transparent (Windows)
        try:
            self.floating_widget.wm_attributes('-transparentcolor', 'black')
        except:
            # Fallback for other systems - use a very dark color
            self.floating_widget.configure(bg='#1a1a1a')
        
        # Create frame for buttons
        button_frame = tk.Frame(self.floating_widget, bg='black')
        button_frame.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Try to make frame transparent too
        try:
            button_frame.configure(bg='black')
        except:
            button_frame.configure(bg='#1a1a1a')
        
        # Create three high-quality rounded buttons
        self.fix_button = RoundedButton(
            button_frame, 
            text="✓ Fix", 
            command=self._fix_and_paste,
            bg_color='#27ae60',  # Green
            hover_color='#2ecc71',
            text_color='white',
            width=80,
            height=35,
            corner_radius=8,
            timer_callback=self._restart_widget_timer
        )
        self.fix_button.pack(side='left', padx=(0, 3))
        
        self.rewrite_button = RoundedButton(
            button_frame, 
            text="📝 Rewrite", 
            command=self._rewrite_and_paste,
            bg_color='#3498db',  # Blue
            hover_color='#2980b9',
            text_color='white',
            width=80,
            height=35,
            corner_radius=8,
            timer_callback=self._restart_widget_timer
        )
        self.rewrite_button.pack(side='left', padx=(0, 3))
        
        self.cancel_button = RoundedButton(
            button_frame, 
            text="✗ Cancel", 
            command=self._cancel_widget,
            bg_color='#e74c3c',  # Red
            hover_color='#c0392b',
            text_color='white',
            width=80,
            height=35,
            corner_radius=8,
            timer_callback=self._restart_widget_timer
        )
        self.cancel_button.pack(side='left')
        
        print(f"DEBUG: Widget with 3 buttons created at ({pos_x}, {pos_y}) with size ({widget_width}, {widget_height})")
        
        # Bring to front and focus
        self.floating_widget.lift()
        self.floating_widget.focus_force()
        
        # Start the auto-close timer
        self._start_widget_timer()
        
        # Bind mouse events to restart timer on interaction
        self.floating_widget.bind('<Motion>', lambda e: self._restart_widget_timer())
        self.floating_widget.bind('<Button-1>', lambda e: self._restart_widget_timer())
        button_frame.bind('<Motion>', lambda e: self._restart_widget_timer())
        button_frame.bind('<Button-1>', lambda e: self._restart_widget_timer())

    def _fix_and_paste(self):
        """Handle the Fix button click"""
        print("DEBUG: _fix_and_paste() called!")
        text_to_correct = self.text_to_correct_for_widget
        print(f"DEBUG: Text to correct: '{text_to_correct}' (length: {len(text_to_correct) if text_to_correct else 0})")
        
        if not text_to_correct or not text_to_correct.strip():
            print("DEBUG: No text to correct")
            self._cancel_widget()
            return

        print("DEBUG: Processing text correction...")
        
        # Call Gemini API for typo fixing
        corrected_text = self._call_gemini_api_fix(text_to_correct)
        print(f"DEBUG: API returned corrected text: '{corrected_text}'")

        if corrected_text:
            print(f"DEBUG: Corrected text: '{corrected_text}'")
            
            # Test clipboard operations
            old_clipboard = pyperclip.paste()
            print(f"DEBUG: Old clipboard content: '{old_clipboard}'")
            
            pyperclip.copy(corrected_text)
            print("DEBUG: Corrected text copied to clipboard.")
            
            # Verify clipboard
            new_clipboard = pyperclip.paste()
            print(f"DEBUG: New clipboard content: '{new_clipboard}'")
            
            # Close widget and paste
            self._close_and_paste()
        else:
            print("DEBUG: Failed to correct text - API returned None/empty")
            self._cancel_widget()

    def _rewrite_and_paste(self):
        """Handle the Rewrite button click"""
        print("DEBUG: _rewrite_and_paste() called!")
        text_to_rewrite = self.text_to_correct_for_widget
        print(f"DEBUG: Text to rewrite: '{text_to_rewrite}' (length: {len(text_to_rewrite) if text_to_rewrite else 0})")
        
        if not text_to_rewrite or not text_to_rewrite.strip():
            print("DEBUG: No text to rewrite")
            self._cancel_widget()
            return

        print("DEBUG: Processing text rewriting for clarity...")
        
        # Call Gemini API for rewriting
        rewritten_text = self._call_gemini_api_rewrite(text_to_rewrite)
        print(f"DEBUG: API returned rewritten text: '{rewritten_text}'")

        if rewritten_text:
            print(f"DEBUG: Rewritten text: '{rewritten_text}'")
            
            # Test clipboard operations
            old_clipboard = pyperclip.paste()
            print(f"DEBUG: Old clipboard content: '{old_clipboard}'")
            
            pyperclip.copy(rewritten_text)
            print("DEBUG: Rewritten text copied to clipboard.")
            
            # Verify clipboard
            new_clipboard = pyperclip.paste()
            print(f"DEBUG: New clipboard content: '{new_clipboard}'")
            
            # Close widget and paste
            self._close_and_paste()
        else:
            print("DEBUG: Failed to rewrite text - API returned None/empty")
            self._cancel_widget()

    def _close_and_paste(self):
        """Close widget and simulate paste"""
        print("DEBUG: _close_and_paste() called!")
        
        self._stop_widget_timer()
        if self.floating_widget:
            print("DEBUG: Destroying widget")
            self.floating_widget.destroy()
            self.floating_widget = None
        
        # Add a longer delay and better focus handling
        print("DEBUG: Starting paste simulation")
        self.simulating_paste = True
        try:
            print("DEBUG: Waiting 0.3 seconds before paste...")
            time.sleep(0.3)  # Increased delay
            
            # Try to focus back to the original window
            try:
                # Get the foreground window that should receive the paste
                hwnd = win32gui.GetForegroundWindow()
                if hwnd:
                    # Make sure the window is active
                    win32gui.SetForegroundWindow(hwnd)
                    time.sleep(0.1)  # Small delay after focus
            except Exception as e:
                print(f"DEBUG: Could not set foreground window: {e}")
            
            print("DEBUG: Simulating Ctrl+V...")
            pyautogui.hotkey('ctrl', 'v')
            print("DEBUG: Paste action simulated successfully")
            
            # Wait a bit more to ensure paste completes
            time.sleep(0.2)
            
        except Exception as e:
            print(f"DEBUG: Error simulating paste: {e}")
        finally:
            self.simulating_paste = False
            print("DEBUG: Paste simulation completed")

    def _cancel_widget(self):
        """Cancel and close the widget"""
        self._stop_widget_timer()
        if self.floating_widget:
             self.floating_widget.destroy()
        self.floating_widget = None
        print("Widget cancelled")

    def _detect_language(self, text):
        """Detect the language of the input text using Gemini API"""
        print(f"DEBUG: Detecting language for text: '{text[:50]}...'")

        api_url = f"{self.gemini_api_base_url}?key={self.api_key}"
        
        prompt = f"""Detect the language of the following text and respond with ONLY the language name in English (e.g., "Romanian", "English", "Spanish", "French", etc.).

Text: "{text}"

Language:"""
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=15)
            
            if response.status_code != 200:
                print(f"DEBUG: Language detection API error - Status: {response.status_code}")
                return "Unknown"
            
            response_data = response.json()
            if 'candidates' in response_data and len(response_data['candidates']) > 0:
                candidate = response_data['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    parts = candidate['content']['parts']
                    if len(parts) > 0 and 'text' in parts[0]:
                        detected_language = parts[0]['text'].strip()
                        # Clean up the response
                        detected_language = detected_language.replace("Language:", "").strip()
                        if detected_language.startswith('"') and detected_language.endswith('"'):
                            detected_language = detected_language[1:-1]
                        
                        print(f"DEBUG: Detected language: '{detected_language}'")
                        return detected_language
            
            print("DEBUG: Could not detect language, defaulting to Unknown")
            return "Unknown"
            
        except Exception as e:
            print(f"DEBUG: Language detection error: {e}")
            return "Unknown"

    def _call_gemini_api_fix(self, text_to_correct):
        """Calls the Gemini API to fix typos in the provided text."""
        print(f"DEBUG: _call_gemini_api_fix() called with text: '{text_to_correct}'")
        
        # First detect the language
        detected_language = self._detect_language(text_to_correct)
        print(f"DEBUG: Language detected as: {detected_language}")
        
        api_url = f"{self.gemini_api_base_url}?key={self.api_key}"
        
        # Enhanced prompt with language detection
        prompt = f"""The following text is written in {detected_language}. Fix any typos, spelling errors, and grammar mistakes while keeping the text EXACTLY in {detected_language}. 

IMPORTANT REQUIREMENTS:
- Keep the text in {detected_language} language - DO NOT translate to any other language
- Fix only spelling errors, typos, and obvious grammar mistakes
- Preserve the original meaning, style, and tone completely
- Maintain the exact same format (line breaks, paragraphs, etc.)
- Return ONLY the corrected text with no explanations or additional words
- If there are no errors, return the original text exactly as provided

Text to correct: "{text_to_correct}"

Corrected text in {detected_language}:"""
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        print(f"DEBUG: Making API request with language-aware prompt...")
        
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=30)
            print(f"DEBUG: Response status code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"DEBUG: API error - Status: {response.status_code}")
                print(f"DEBUG: API error - Response: {response.text}")
                return None
            
            response.raise_for_status()
            
            response_data = response.json()
            print(f"DEBUG: Response data keys: {list(response_data.keys())}")
            
            if 'candidates' in response_data and len(response_data['candidates']) > 0:
                candidate = response_data['candidates'][0]
                
                if 'content' in candidate and 'parts' in candidate['content']:
                    parts = candidate['content']['parts']
                    
                    if len(parts) > 0 and 'text' in parts[0]:
                        corrected_text = parts[0]['text'].strip()
                        print(f"DEBUG: Raw API response text: '{corrected_text}'")
                        
                        # Clean up the response
                        corrected_text = corrected_text.replace(f"Corrected text in {detected_language}:", "").strip()
                        corrected_text = corrected_text.replace("Corrected text:", "").strip()
                        if corrected_text.startswith('"') and corrected_text.endswith('"'):
                            corrected_text = corrected_text[1:-1]
                        
                        print(f"DEBUG: Final corrected text: '{corrected_text}'")
                        return corrected_text
            
            print("DEBUG: Failed to extract text from Gemini API response")
            return None
            
        except requests.exceptions.Timeout:
            print("DEBUG: API request timed out")
            return None
        except requests.exceptions.ConnectionError:
            print("DEBUG: API connection error")
            return None
        except requests.exceptions.RequestException as e:
            print(f"DEBUG: API request error: {e}")
            return None
        except Exception as e:
            print(f"DEBUG: Unexpected error during API call: {e}")
            return None

    def _call_gemini_api_rewrite(self, text_to_rewrite):
        """Calls the Gemini API to rewrite text for better clarity and logic."""
        print(f"DEBUG: _call_gemini_api_rewrite() called with text: '{text_to_rewrite}'")
        
        # First detect the language
        detected_language = self._detect_language(text_to_rewrite)
        print(f"DEBUG: Language detected as: {detected_language}")
        
        api_url = f"{self.gemini_api_base_url}?key={self.api_key}"
        
        # Enhanced prompt with language detection
        prompt = f"""The following text is written in {detected_language}. Rewrite it to improve word placement, sentence structure, and logical flow while keeping it EXACTLY in {detected_language}.

CRITICAL REQUIREMENTS:
- Keep the text in {detected_language} language - DO NOT translate to any other language
- Preserve ALL original information, facts, and meaning completely
- Maintain the EXACT same format (paragraphs, line breaks, structure)
- Only improve word order, sentence structure, and logical flow
- Do not add or remove any information whatsoever
- Keep the same writing style and tone
- Return ONLY the rewritten text with no explanations or commentary
- If the text is already well-structured, return it with minimal changes

Original text in {detected_language}: "{text_to_rewrite}"

Rewritten text in {detected_language}:"""
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }]
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        print(f"DEBUG: Making rewrite API request with language-aware prompt...")
        
        try:
            response = requests.post(api_url, json=payload, headers=headers, timeout=30)
            print(f"DEBUG: Response status code: {response.status_code}")
            
            if response.status_code != 200:
                print(f"DEBUG: API error - Status: {response.status_code}")
                print(f"DEBUG: API error - Response: {response.text}")
                return None
            
            response.raise_for_status()
            
            response_data = response.json()
            print(f"DEBUG: Response data keys: {list(response_data.keys())}")
            
            if 'candidates' in response_data and len(response_data['candidates']) > 0:
                candidate = response_data['candidates'][0]
                
                if 'content' in candidate and 'parts' in candidate['content']:
                    parts = candidate['content']['parts']
                    
                    if len(parts) > 0 and 'text' in parts[0]:
                        rewritten_text = parts[0]['text'].strip()
                        print(f"DEBUG: Raw API response text: '{rewritten_text}'")
                        
                        # Clean up the response
                        rewritten_text = rewritten_text.replace(f"Rewritten text in {detected_language}:", "").strip()
                        rewritten_text = rewritten_text.replace("Rewritten text:", "").strip()
                        if rewritten_text.startswith('"') and rewritten_text.endswith('"'):
                            rewritten_text = rewritten_text[1:-1]
                        
                        print(f"DEBUG: Final rewritten text: '{rewritten_text}'")
                        return rewritten_text
            
            print("DEBUG: Failed to extract text from Gemini API response")
            return None
            
        except requests.exceptions.Timeout:
            print("DEBUG: API request timed out")
            return None
        except requests.exceptions.ConnectionError:
            print("DEBUG: API connection error")
            return None
        except requests.exceptions.RequestException as e:
            print(f"DEBUG: API request error: {e}")
            return None
        except Exception as e:
            print(f"DEBUG: Unexpected error during API call: {e}")
            return None

    def _start_widget_timer(self):
        """Start or restart the widget timeout timer"""
        self._stop_widget_timer()
        self.widget_timeout_timer = self.root.after(
            self.widget_timeout_seconds * 1000, 
            self._auto_close_widget
        )
        print(f"DEBUG: Widget timer started - will auto-close in {self.widget_timeout_seconds} seconds")

    def _stop_widget_timer(self):
        """Stop the widget timeout timer"""
        if self.widget_timeout_timer:
            self.root.after_cancel(self.widget_timeout_timer)
            self.widget_timeout_timer = None
            print("DEBUG: Widget timer stopped")

    def _restart_widget_timer(self):
        """Restart the widget timeout timer (called on user interaction)"""
        if self.floating_widget and self.floating_widget.winfo_exists():
            self._start_widget_timer()
            print("DEBUG: Widget timer restarted due to user interaction")

    def _auto_close_widget(self):
        """Automatically close the widget after timeout"""
        print("DEBUG: Auto-closing widget due to inactivity timeout")
        if self.floating_widget and self.floating_widget.winfo_exists():
            self.floating_widget.destroy()
            self.floating_widget = None
        self.widget_timeout_timer = None

    def create_tray_icon(self):
        """Create a simple icon for the system tray"""
        # Create a 64x64 icon with a "T" for TypoFix
        size = (64, 64)
        image = Image.new('RGBA', size, (76, 175, 80, 255))  # Green background
        
        # Create a simple "T" text icon
        try:
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(image)
            try:
                # Try to use a system font
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()
            
            # Calculate text position to center the "T"
            text = "T"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (size[0] - text_width) // 2
            y = (size[1] - text_height) // 2
            
            # Draw white "T"
            draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
        except:
            # Fallback if drawing fails
            pass
        
        return image

    def setup_system_tray(self):
        """Setup the system tray icon with context menu"""
        try:
            # Create the tray icon
            icon_image = self.create_tray_icon()
            
            # Create context menu
            menu = pystray.Menu(
                pystray.MenuItem("TypoFix - AI Text Correction", lambda: None, enabled=False),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Status: Running", lambda: None, enabled=False),
                pystray.MenuItem("Usage: Highlight text → Ctrl+Left Shift", lambda: None, enabled=False),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Show Instructions", self.show_instructions),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Exit TypoFix", self.quit_application)
            )
            
            # Create the system tray icon
            self.tray_icon = pystray.Icon(
                "TypoFix",
                icon_image,
                "TypoFix - AI Text Correction Tool\nRunning in background\nHighlight text → Ctrl+Left Shift",
                menu
            )
            
            # Run the tray icon in a separate thread
            tray_thread = threading.Thread(target=self.tray_icon.run, daemon=True)
            tray_thread.start()
            
            print("System tray icon created successfully.")
            
        except Exception as e:
            print(f"Could not create system tray icon: {e}")
            # Continue without tray icon if it fails

    def show_instructions(self):
        """Show usage instructions"""
        instructions = """TypoFix - How to Use:

1. Highlight any text in any application
2. Press CTRL+LEFT SHIFT to activate TypoFix
3. A widget will appear with three buttons:
   • ✓ Fix - Corrects typos and spelling
   • 📝 Rewrite - Improves clarity and logic
   • ✗ Cancel - Dismiss without changes
4. Click your desired action

The app runs in the background and works in:
• Web browsers (Chrome, Firefox, Edge)
• Microsoft Word, Excel, PowerPoint
• Email clients (Outlook, Gmail)
• Text editors and any other application

TypoFix preserves the original language and format 
while improving your text."""

        # Create a simple info dialog
        messagebox.showinfo("TypoFix - Instructions", instructions)

    def quit_application(self):
        """Quit the application completely"""
        try:
            print("Shutting down TypoFix...")
            
            # Stop widget timer
            self._stop_widget_timer()
            
            # Close floating widget if open
            if self.floating_widget:
                self.floating_widget.destroy()
            
            # Stop the tray icon
            if hasattr(self, 'tray_icon'):
                self.tray_icon.stop()
            
            # Quit the main application
            self.root.quit()
            self.root.destroy()
            
        except Exception as e:
            print(f"Error during shutdown: {e}")
        finally:
            # Force exit if normal shutdown fails
            os._exit(0)

if __name__ == "__main__":
    main_root = tk.Tk()
    app = TypoFixApp(main_root)
    main_root.mainloop()
