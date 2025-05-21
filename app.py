import tkinter as tk
from tkinter import Text, messagebox  # Added messagebox for error display
import os
import requests  # Added for API calls
from dotenv import load_dotenv  # Added for .env file

class TypoFixApp:
    def __init__(self, root):
        self.root = root
        root.title("TypoFix")

        # Load API Key
        load_dotenv()  # Load environment variables from .env file
        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            print("CRITICAL: GEMINI_API_KEY not found. Please set it in your .env file.")
            # Optionally, disable API-dependent features or show an error in the UI
        else:
            print("Gemini API Key loaded successfully.")

        # Configure window size and position (optional)
        root.geometry("500x300")  # Width x Height

        # Text input box
        self.text_input = Text(root, wrap=tk.WORD, height=10, width=50)
        self.text_input.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Bind text selection event
        self.text_input.bind("<ButtonRelease-1>", self._on_text_select)
        self.text_input.bind("<FocusOut>", self._on_focus_out)  # Hide widget if text input loses focus

        # Correction Widget (Button) - initially hidden
        self.correction_widget = tk.Button(root, text="Fix Typos", command=self._on_widget_click)

        # API Configuration
        # The base URL for the Gemini API
        self.gemini_api_base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        self.correction_display_window = None  # To keep track of the display window

    def _on_text_select(self, event=None):
        """Handles the event when text is selected."""
        try:
            selected_text = self.text_input.selection_get()
            if selected_text:
                print(f"Selected text: '{selected_text}'")
                self._show_correction_widget()
            else:
                self._hide_correction_widget()
        except tk.TclError:
            self._hide_correction_widget()

    def _on_focus_out(self, event=None):
        """Hides the widget when the text input area loses focus."""
        self.root.after(100, self._check_and_hide_widget)

    def _check_and_hide_widget(self):
        """Hides the widget if the focus is not on the text input or the widget itself."""
        focused_widget = self.root.focus_get()
        if focused_widget != self.text_input and focused_widget != self.correction_widget:
            self._hide_correction_widget()

    def _show_correction_widget(self):
        """Shows the correction widget."""
        self.correction_widget.pack(pady=5, before=None)

    def _hide_correction_widget(self):
        """Hides the correction widget."""
        self.correction_widget.pack_forget()

    def _on_widget_click(self):
        """Handles the click event of the correction widget."""
        if not self.api_key:
            print("Cannot fix typos: API key not configured.")
            messagebox.showerror("API Key Error", "GEMINI_API_KEY not found. Please configure it.")
            return

        try:
            selected_text = self.text_input.selection_get()
            if not selected_text.strip():
                print("Widget clicked, but no actual text selected.")
                self._hide_correction_widget()
                return

            print(f"Attempting to correct text: '{selected_text}'")
            
            api_response_json = self._call_gemini_api(selected_text)
            
            if api_response_json:
                corrected_text = self._parse_gemini_response(api_response_json)
                if corrected_text:
                    print(f"Corrected text: '{corrected_text}'")
                    self._display_corrected_text(corrected_text)
                else:
                    # Error message is shown by _parse_gemini_response
                    print("Could not extract corrected text from API response.")
            else:
                # Error messages are handled within _call_gemini_api or by exceptions
                print("API call did not return a response or failed.")

        except tk.TclError:
            print("Widget clicked, but no text selected (TclError).")
            self._hide_correction_widget()
        except Exception as e:  
            print(f"An unexpected error occurred in _on_widget_click: {e}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def _parse_gemini_response(self, response_json):
        """Parses the JSON response from Gemini API to extract corrected text."""
        try:
            # Accessing the text based on the typical Gemini API structure
            # candidates -> 0 -> content -> parts -> 0 -> text
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
