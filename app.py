import tkinter as tk
from tkinter import Text, messagebox
import os
import requests
from dotenv import load_dotenv
import time  # Added for delays
import pyperclip  # Added for clipboard access
import pyautogui  # Added for simulating key presses
from pynput import keyboard  # Added for global hotkey listening
import threading  # Added for running listener in a separate thread
from screeninfo import get_monitors  # Added for multi-monitor support

class TypoFixApp:
    def __init__(self, root):
        self.root = root
        root.title("TypoFix Listener")  # Changed title

        # Load API Key
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            print("CRITICAL: GEMINI_API_KEY not found. Please set it in your .env file.")
        else:
            print("Gemini API Key loaded successfully.")

        # Hide the main window for now, as interaction is via hotkey
        root.withdraw()

        # API Configuration
        self.gemini_api_base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        self.correction_display_window = None  # For the Toplevel window displaying correction

        # --- Widget and State Management ---
        self.floating_widget = None
        self.text_to_correct_for_widget = None
        self.simulating_paste = False  # Flag to prevent hotkey re-trigger during paste
        self.floating_widget_label = None
        self.floating_widget_button = None

        # --- Hotkey Setup ---
        self.hotkey_combination = {keyboard.Key.ctrl, keyboard.KeyCode.from_char('c')} # Changed to Ctrl+C
        self.current_hotkey_keys = set()
        self.start_hotkey_listener()
        print(f"Hotkey listener started for Ctrl+C. Press the hotkey after highlighting text in any app.")

    def _normalize_key(self, key):
        """Normalizes modifier keys to their canonical form."""
        if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            return keyboard.Key.ctrl
        if key in (keyboard.Key.shift_l, keyboard.Key.shift_r):
            return keyboard.Key.shift
        if key in (keyboard.Key.alt_l, keyboard.Key.alt_r, keyboard.Key.alt_gr):
            return keyboard.Key.alt
        return key

    def start_hotkey_listener(self):
        listener_thread = threading.Thread(target=self._run_listener, daemon=True)
        listener_thread.start()

    def _on_press(self, key):
        original_raw_key = key
        normalized_modifier_key = self._normalize_key(original_raw_key)

        # Determine the canonical key form
        canonical_key_form = None
        if normalized_modifier_key == keyboard.Key.ctrl:
            canonical_key_form = keyboard.Key.ctrl
        elif isinstance(normalized_modifier_key, keyboard.KeyCode):
            if normalized_modifier_key.char == 'c':
                canonical_key_form = keyboard.KeyCode.from_char('c')
            elif normalized_modifier_key.char == '\x03':  # If KeyCode's char is ETX
                canonical_key_form = keyboard.KeyCode.from_char('c')
        elif isinstance(normalized_modifier_key, str) and normalized_modifier_key == '\x03':  # Fallback for raw string
            canonical_key_form = keyboard.KeyCode.from_char('c')

        # Only log if the key is part of our hotkey combination
        if canonical_key_form and canonical_key_form in self.hotkey_combination:
            print(f"DEBUG: _on_press: Raw: {original_raw_key}, NormalizedMod: {normalized_modifier_key}, Canonical: {canonical_key_form}, CurrentSet: {self.current_hotkey_keys}")

            if hasattr(self, 'simulating_paste') and self.simulating_paste:
                return

            self.current_hotkey_keys.add(canonical_key_form)
            print(f"DEBUG: _on_press: Added {canonical_key_form} to set. CurrentSet: {self.current_hotkey_keys}")
            
            if self.hotkey_combination.issubset(self.current_hotkey_keys):
                print(f"DEBUG: _on_press: Hotkey combination {self.hotkey_combination} DETECTED!")
                self._handle_hotkey_action()

    def _on_release(self, key):
        original_raw_key = key
        normalized_modifier_key = self._normalize_key(original_raw_key)

        # Determine the canonical key form
        canonical_key_form = None
        if normalized_modifier_key == keyboard.Key.ctrl:
            canonical_key_form = keyboard.Key.ctrl
        elif isinstance(normalized_modifier_key, keyboard.KeyCode):
            if normalized_modifier_key.char == 'c':
                canonical_key_form = keyboard.KeyCode.from_char('c')
            elif normalized_modifier_key.char == '\x03':  # If KeyCode's char is ETX
                canonical_key_form = keyboard.KeyCode.from_char('c')
        elif isinstance(normalized_modifier_key, str) and normalized_modifier_key == '\x03':  # Fallback for raw string
            canonical_key_form = keyboard.KeyCode.from_char('c')

        # Only log if the key is part of our hotkey combination
        if canonical_key_form and canonical_key_form in self.hotkey_combination:
            print(f"DEBUG: _on_release: Raw: {original_raw_key}, NormalizedMod: {normalized_modifier_key}, Canonical: {canonical_key_form}, CurrentSet: {self.current_hotkey_keys}")

            if hasattr(self, 'simulating_paste') and self.simulating_paste:
                return

            try:
                self.current_hotkey_keys.remove(canonical_key_form)
                print(f"DEBUG: _on_release: Removed {canonical_key_form} from set. CurrentSet: {self.current_hotkey_keys}")
            except KeyError:
                print(f"DEBUG: _on_release: Attempted to remove {canonical_key_form} but it was not in the set (possibly cleared by hotkey action).")
                pass

    def _run_listener(self):
        with keyboard.Listener(on_press=self._on_press, on_release=self._on_release) as listener:
            listener.join()

    def _handle_hotkey_action(self):
        print("Ctrl+C hotkey detected!") 
        try:
            time.sleep(0.2) 
            copied_text = pyperclip.paste()
            
            if copied_text:
                print(f"Captured text from clipboard: '{copied_text}'")
                self.text_to_correct_for_widget = copied_text  # Store for the widget
                self._show_floating_correction_widget()  # Show the widget instead of direct API call
            else:
                print("No text found on clipboard after copy attempt.")

        except Exception as e:
            print(f"Error in hotkey action: {e}")
        
        # Reset current keys to allow re-triggering
        # Important: Clear after a short delay to avoid re-triggering if keys are held
        self.root.after(50, self.current_hotkey_keys.clear)

    def _show_floating_correction_widget(self):
        if self.floating_widget and self.floating_widget.winfo_exists():
            self.floating_widget.destroy()
            self.floating_widget_label = None
            self.floating_widget_button = None

        mouse_x, mouse_y = pyautogui.position()
        active_monitor = None
        for m in get_monitors():
            if m.x <= mouse_x < m.x + m.width and m.y <= mouse_y < m.y + m.height:
                active_monitor = m
                break
        if active_monitor is None:
            active_monitor = get_monitors()[0]

        self.floating_widget = tk.Toplevel(self.root)
        self.floating_widget.overrideredirect(True)
        self.floating_widget.attributes("-topmost", True)

        canvas_width = 170  # Adjusted for more space
        canvas_height = 40 # Adjusted
        radius = 10
        padding = 8 # General padding for content
        bg_color = "lightgrey"
        button_color = "#4CAF50"
        font_family = "Arial"
        font_size = 9

        canvas = tk.Canvas(self.floating_widget, width=canvas_width, height=canvas_height,
                           background=bg_color, # Explicitly set canvas background
                           highlightthickness=0, bd=0)
        canvas.pack()

        def _create_rounded_rectangle(cv, x1, y1, x2, y2, r, **kwargs):
            cv.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r,
                          start=90, extent=90, smooth=True, **kwargs)
            cv.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r,
                          start=0, extent=90, smooth=True, **kwargs)
            cv.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2,
                          start=180, extent=90, smooth=True, **kwargs)
            cv.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2,
                          start=270, extent=90, smooth=True, **kwargs)
            cv.create_rectangle(x1 + r, y1, x2 - r, y1 + r, **kwargs)
            cv.create_rectangle(x1 + r, y2 - r, x2 - r, y2, **kwargs)
            cv.create_rectangle(x1, y1 + r, x1 + r, y2 - r, **kwargs)
            cv.create_rectangle(x2 - r, y1 + r, x2, y2 - r, **kwargs)
            cv.create_rectangle(x1 + r, y1 + r, x2 - r, y2 - r, **kwargs)

        _create_rounded_rectangle(canvas, 0, 0, canvas_width, canvas_height, radius, 
                                  fill=bg_color, outline=bg_color)

        self.floating_widget_label = tk.Label(canvas, text="TypoFix",  # Parent changed to canvas
                                              background=bg_color, foreground="black",
                                              font=(font_family, font_size))
        self.floating_widget_label.update_idletasks()
        label_req_width = self.floating_widget_label.winfo_reqwidth()
        label_req_height = self.floating_widget_label.winfo_reqheight()

        self.floating_widget_button = tk.Button(canvas, text="Fix & Paste",  # Parent changed to canvas
                                                command=self._perform_correction_from_widget,
                                                relief=tk.FLAT, background=button_color, foreground="white",
                                                font=(font_family, font_size, "bold"),
                                                padx=6, pady=0, # pady adjusted for vertical centering
                                                borderwidth=0, highlightthickness=0, activebackground="#45a049")
        self.floating_widget_button.update_idletasks()
        
        # Calculate positions
        content_total_height = max(label_req_height, button_req_height)
        y_center_offset = (canvas_height - content_total_height) / 2

        label_x = padding
        label_y = y_center_offset
        canvas.create_window(label_x, label_y, window=self.floating_widget_label, anchor=tk.NW)

        button_x = label_x + label_req_width + padding # Spacing
        button_y = y_center_offset 
        # Adjust button y if its height is different to align baselines or centers
        if label_req_height != button_req_height: # Basic vertical centering for button
             button_y = (canvas_height - button_req_height) / 2
        canvas.create_window(button_x, button_y, window=self.floating_widget_button, anchor=tk.NW)
        
        # Positioning the Toplevel window
        screen_width = active_monitor.width
        screen_height = active_monitor.height
        screen_x_offset = active_monitor.x
        screen_y_offset = active_monitor.y

        relative_mouse_x = mouse_x - screen_x_offset
        relative_mouse_y = mouse_y - screen_y_offset

        final_x = screen_x_offset + relative_mouse_x + 15
        final_y = screen_y_offset + relative_mouse_y + 15

        if relative_mouse_x + 15 + canvas_width > screen_width:
            final_x = screen_x_offset + screen_width - canvas_width - 5
        if relative_mouse_y + 15 + canvas_height > screen_height:
            final_y = screen_y_offset + screen_height - canvas_height - 5
        
        if final_x < screen_x_offset:
            final_x = screen_x_offset + 5
        if final_y < screen_y_offset:
            final_y = screen_y_offset + 5
            
        self.floating_widget.geometry(f"+{final_x}+{final_y}")
        self.floating_widget.lift()
        self.floating_widget.focus_force()
        self.floating_widget.bind("<Escape>", lambda e: self._destroy_floating_widget())

    def _destroy_floating_widget(self):
        if self.floating_widget and self.floating_widget.winfo_exists():
            self.floating_widget.destroy()
        self.floating_widget = None
        self.floating_widget_label = None
        self.floating_widget_button = None
        self.text_to_correct_for_widget = None  # Also clear text if widget is dismissed manually

    def _update_widget_label_and_close(self, message, delay_seconds):
        """Helper to update widget label, wait, and then destroy."""
        if self.floating_widget and self.floating_widget.winfo_exists():
            if self.floating_widget_label:
                self.floating_widget_label.config(text=message)
            self.floating_widget.update_idletasks()
            # Use root.after to schedule the destruction, allowing UI to update
            self.root.after(int(delay_seconds * 1000), self._destroy_floating_widget)
        else:
            # If widget somehow already gone or never created, ensure state is clean
            self._destroy_floating_widget()

    def _perform_correction_from_widget(self):
        if not self.floating_widget or not self.floating_widget.winfo_exists():
            self.text_to_correct_for_widget = None  # Ensure cleanup if called unexpectedly
            return

        # Update button state for visual feedback
        if self.floating_widget_button:
            self.floating_widget_button.config(text="Fixing...", state=tk.DISABLED)
        if self.floating_widget_label:  # Optionally update label too
            self.floating_widget_label.config(text="Processing...")
        
        # Ensure UI updates before blocking call
        self.floating_widget.update_idletasks()

        original_text = self.text_to_correct_for_widget
        corrected_text_content = None # To store the text from API

        # --- Step 1: Call API and Parse ---
        try:
            if not original_text:
                print("Error: No text stored for correction.")
                self._update_widget_label_and_close("No Text", 0.7)
                return 

            print(f"Attempting to correct: '{original_text}'")
            if not self.api_key:
                print("API key not available for correction.")
                self._update_widget_label_and_close("No Key", 0.7)
                return

            api_response = self._call_gemini_api(original_text)
            if not api_response: # _call_gemini_api handles messagebox for its errors
                print("API call failed or returned no response.")
                self._update_widget_label_and_close("API Err", 0.7)
                return

            parsed_text = self._parse_gemini_response(api_response) # _parse_gemini_response handles messagebox
            if not parsed_text:
                print("Could not parse corrected text from API.")
                self._update_widget_label_and_close("Parse Err", 0.7)
                return
            
            corrected_text_content = parsed_text
            print(f"API Corrected Text: '{corrected_text_content}'")

        except Exception as e: # Catch any unexpected error during API/parsing stages
            print(f"Unexpected error during correction processing: {e}")
            self._update_widget_label_and_close("Internal Err", 0.7)
            return

        # --- Step 2: Decide if pasting, then act ---
        if corrected_text_content and corrected_text_content.strip().lower() != original_text.strip().lower():
            # Text has changed and is not empty, proceed with paste
            self._destroy_floating_widget()  # Destroy widget *before* paste
            time.sleep(0.15)  # Increased delay for OS to return focus to the previous app

            try:
                pyperclip.copy(corrected_text_content)
                print("Corrected text copied to clipboard.")
                
                self.simulating_paste = True
                print("Simulating Ctrl+V (Paste)")
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.05) # Small delay after paste
                self.simulating_paste = False
                print("Paste simulation finished.")
            except Exception as e:
                print(f"Error during copy/paste: {e}")
                # Widget is already destroyed, so we can only show a messagebox
                messagebox.showerror("Paste Error", f"Could not paste text: {e}")
        else:
            # No change needed or API returned empty/same text as original
            print("No change needed or API returned empty/same text.")
            self._update_widget_label_and_close("No Change", 0.7)

    def _parse_gemini_response(self, response_json):
        """Parses the JSON response from Gemini API to extract corrected text."""
        try:
            corrected_text = response_json['candidates'][0]['content']['parts'][0]['text']
            stripped_text = corrected_text.strip()  # Strip here
            if not stripped_text:  # Check if the text is effectively empty after stripping
                print("API returned empty or whitespace-only text.")
                messagebox.showerror("API Response Error", "API returned empty or effectively empty text.")
                return None 
            return stripped_text  # Return the stripped text
        except (KeyError, IndexError, TypeError) as e:
            error_msg = f"Error parsing Gemini API response: {e}. Expected structure not found."
            print(error_msg)
            print("Full API Response for debugging:", response_json)
            messagebox.showerror("API Response Error", f"{error_msg}\nCheck console for details.")
            return None

    def _call_gemini_api(self, text_to_correct):
        """Calls the Gemini API to correct the provided text."""
        if not self.api_key:
            messagebox.showerror("API Error", "Gemini API key is not configured.")
            return None

        api_url = f"{self.gemini_api_base_url}?key={self.api_key}"
        
        # Modified prompt to ask for original text if no typos are found
        prompt = f"Correct the following text for typos. If no typos are found, return the original text verbatim. Text: \"{text_to_correct}\""
        
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
            response = requests.post(api_url, json=payload, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            error_message = f"HTTP error occurred: {http_err} - {response.text}"
            print(error_message)
            messagebox.showerror("API Error", f"HTTP error: {http_err}\nResponse: {response.text}")
            return None
        except requests.exceptions.ConnectionError as conn_err:
            error_message = f"Connection error occurred: {conn_err}"
            print(error_message)
            messagebox.showerror("API Error", f"Connection error: {conn_err}")
            return None
        except requests.exceptions.Timeout as timeout_err:
            error_message = f"Timeout error occurred: {timeout_err}"
            print(error_message)
            messagebox.showerror("API Error", f"Timeout error: {timeout_err}")
            return None
        except requests.exceptions.RequestException as req_err:
            error_message = f"An unexpected error occurred with the API request: {req_err}"
            print(error_message)
            messagebox.showerror("API Error", f"Request error: {req_err}")
            return None
        except Exception as e:
            error_message = f"An unexpected error occurred during API call: {e}"
            print(error_message)
            messagebox.showerror("Error", f"An unexpected error: {e}")
            return None

    def _display_corrected_text(self, corrected_text):
        """Displays the corrected text in a Toplevel window."""
        if self.correction_display_window and self.correction_display_window.winfo_exists():
            self.correction_display_window.destroy()  # Close existing window if open

        self.correction_display_window = tk.Toplevel(self.root)
        self.correction_display_window.title("Corrected Text")

        # Position the window at the top of the main window
        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_width = self.root.winfo_width()
        
        # Set a fixed width for the Toplevel, height will adjust or be fixed
        display_width = main_width - 40  # Slightly less than main window width

        # Center the Toplevel window horizontally above the main window
        self.correction_display_window.geometry(f"{display_width}x100+{main_x + 20}+{main_y + 20}") 

        # Use a Text widget for display, allowing for multi-line and potential copying
        text_area = Text(self.correction_display_window, wrap=tk.WORD, height=5, relief=tk.FLAT, background=self.correction_display_window.cget('bg'))
        text_area.insert(tk.END, corrected_text)
        text_area.config(state=tk.DISABLED)  # Make it read-only
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Make the window non-resizable for now, or allow as needed
        self.correction_display_window.resizable(False, False)

        # Bring the window to the front
        self.correction_display_window.lift()
        self.correction_display_window.focus_set()

        # Optional: Add a close button
        close_button = tk.Button(self.correction_display_window, text="Close", command=self.correction_display_window.destroy)
        close_button.pack(pady=5)

if __name__ == "__main__":
    main_root = tk.Tk()
    app = TypoFixApp(main_root)
    main_root.mainloop()
