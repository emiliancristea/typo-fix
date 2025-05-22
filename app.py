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
            self.floating_widget_label = None  # Clear refs
            self.floating_widget_button = None

        # Get mouse position
        mouse_x, mouse_y = pyautogui.position()

        self.floating_widget = tk.Toplevel(self.root)
        self.floating_widget.overrideredirect(True)  # Frameless window
        self.floating_widget.attributes("-topmost", True)  # Keep on top

        # Basic styling and content
        self.floating_widget.configure(background="lightgrey")
        self.floating_widget_label = tk.Label(self.floating_widget, text="TypoFix", background="lightgrey", foreground="black", padx=5, pady=2)
        self.floating_widget_label.pack(side=tk.LEFT, padx=(5,0))  # Add some padding for the label

        self.floating_widget_button = tk.Button(self.floating_widget, text="Fix & Paste", 
                               command=self._perform_correction_from_widget,
                               relief=tk.FLAT, background="#4CAF50", foreground="white", padx=5, pady=2, borderwidth=0, highlightthickness=0)
        self.floating_widget_button.pack(side=tk.LEFT, padx=5, pady=3)

        # Adjust position slightly to be near cursor but not directly under it
        # Position it slightly offset from the cursor
        widget_width = 150  # Approximate width, adjust as needed
        widget_height = 30  # Approximate height
        
        # Attempt to keep widget on screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        final_x = mouse_x + 15
        final_y = mouse_y + 15

        if final_x + widget_width > screen_width:
            final_x = screen_width - widget_width - 5  # 5px buffer
        if final_y + widget_height > screen_height:
            final_y = screen_height - widget_height - 5  # 5px buffer
        if final_x < 0:
            final_x = 5
        if final_y < 0:
            final_y = 5
            
        self.floating_widget.geometry(f"+{final_x}+{final_y}")
        self.floating_widget.lift()
        self.floating_widget.focus_force()  # Try to give it focus

        # Bind Escape key to close the widget
        self.floating_widget.bind("<Escape>", lambda e: self._destroy_floating_widget())

    def _destroy_floating_widget(self):
        if self.floating_widget and self.floating_widget.winfo_exists():
            self.floating_widget.destroy()
        self.floating_widget = None
        self.floating_widget_label = None
        self.floating_widget_button = None
        self.text_to_correct_for_widget = None  # Also clear text if widget is dismissed manually

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
        corrected_text_to_paste = None

        try:
            if not original_text:
                print("Error: No text stored for correction.")
                return 

            print(f"Attempting to correct: '{original_text}'")
            if self.api_key:
                api_response = self._call_gemini_api(original_text)
                if api_response:
                    corrected_text = self._parse_gemini_response(api_response)
                    if corrected_text:
                        print(f"API Corrected Text: '{corrected_text}'")
                        # Only proceed if correction is different and non-empty
                        if corrected_text.strip() and corrected_text.strip().lower() != original_text.strip().lower():
                            corrected_text_to_paste = corrected_text
                        else:
                            print("No change needed or API returned empty/same text.")
                            if self.floating_widget_label:
                                self.floating_widget_label.config(text="No Change")
                                self.floating_widget.update_idletasks()
                                time.sleep(0.7)  # Brief display
                    else:
                        print("Could not parse corrected text from API.")
                        if self.floating_widget_label:
                           self.floating_widget_label.config(text="Parse Err")
                           self.floating_widget.update_idletasks()
                           time.sleep(0.7)
                else:
                    print("API call failed or returned no response.")
                    if self.floating_widget_label:
                       self.floating_widget_label.config(text="API Err")
                       self.floating_widget.update_idletasks()
                       time.sleep(0.7)
            else:
                print("API key not available for correction.")
                if self.floating_widget_label:
                   self.floating_widget_label.config(text="No Key")
                   self.floating_widget.update_idletasks()
                   time.sleep(0.7)

            if corrected_text_to_paste:
                try:
                    pyperclip.copy(corrected_text_to_paste)
                    print("Corrected text copied to clipboard.")
                    
                    self.simulating_paste = True
                    print("Simulating Ctrl+V (Paste)")
                    time.sleep(0.05)  # Small delay for window focus to potentially revert
                    pyautogui.hotkey('ctrl', 'v')
                    time.sleep(0.1) 
                    self.simulating_paste = False
                    print("Paste simulation finished.")
                except Exception as e:
                    print(f"Error during copy/paste: {e}")
                    messagebox.showerror("Paste Error", f"Could not paste text: {e}") 
                    if self.floating_widget_label:
                       self.floating_widget_label.config(text="Paste Err")
                       self.floating_widget.update_idletasks()
                       time.sleep(0.7)
        finally:
            self._destroy_floating_widget()  # Use the new unified destroy method

    def _parse_gemini_response(self, response_json):
        """Parses the JSON response from Gemini API to extract corrected text."""
        try:
            corrected_text = response_json['candidates'][0]['content']['parts'][0]['text']
            return corrected_text.strip()  # Remove leading/trailing whitespace
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
        
        prompt = f"Correct the following text for typos: \"{text_to_correct}\""
        
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
