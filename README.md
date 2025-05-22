# TypoFix Desktop App

TypoFix is a system-wide utility for Windows that helps you correct typos in highlighted text using the Gemini AI API. After highlighting text in any application and pressing Ctrl+C, a small, clickable, floating widget appears near your mouse cursor. Clicking the "Fix & Paste" button on this widget sends the captured text to the Gemini API for typo correction. The corrected text (or the original, if no typos are found) is then placed on your system clipboard, and a paste action (Ctrl+V) is simulated to replace the original highlighted text in the source application.

## Features

*   **System-Wide Operation:** Works in any application on Windows.
*   **Global Hotkey:** Detects Ctrl+C after text is highlighted.
*   **Floating Widget:** A small, clickable widget with rounded corners appears near the mouse cursor.
*   **AI-Powered Correction:** Uses the Gemini API to correct typos.
*   **Smart Pasting:** Replaces the original highlighted text with the corrected version.
*   **Feedback:** The widget provides feedback for various states (e.g., "Processing...", "No Change", "API Err").
*   **Automatic Closing:** The widget closes automatically after processing or on error.
*   **Escape to Close:** Pressing the Escape key closes the widget.

## Technology Stack

*   **Python:** Core application logic.
*   **Tkinter:** GUI framework for the floating widget.
*   **Pynput:** For global hotkey listening.
*   **Pyperclip:** For clipboard operations.
*   **PyAutoGUI:** For simulating paste (Ctrl+V).
*   **Screeninfo:** For multi-monitor support to position the widget correctly.
*   **Requests:** For Gemini API communication.
*   **Dotenv:** For managing environment variables (API key).
*   **PyInstaller (Planned):** For packaging into a standalone executable.
*   **Gemini API:** For text correction.

## Getting Started (Development)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/emiliancristea/typo-fix.git
    cd typo-fix
    ```
2.  **Set up a virtual environment:**
    ```bash
    python -m venv .venv
    # On Windows (PowerShell)
    .venv\\Scripts\\Activate.ps1
    # On macOS/Linux (Note: Currently Windows-only, but for general Python dev)
    # source .venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up your Gemini API Key:**
    *   Obtain an API key from Google AI Studio (or your relevant Gemini provider).
    *   Create a `.env` file in the root directory of the project (`c:\\Dev\\typo-fix\\.env`) with the following content:
        ```
        GEMINI_API_KEY=your_api_key_here
        ```
        (The `.env` file is gitignored by default).
5.  **Run the application:**
    ```bash
    python app.py
    ```
    The application runs in the background. To use it:
    *   Highlight text in any application.
    *   Press Ctrl+C.
    *   The TypoFix widget should appear. Click "Fix & Paste".

## How it Works

1.  The application listens for a global Ctrl+C key combination.
2.  When Ctrl+C is detected after text has likely been highlighted (by virtue of being copied), the application captures the text from the clipboard.
3.  A small, floating Tkinter widget is displayed near the mouse cursor.
4.  If the "Fix & Paste" button on the widget is clicked:
    a.  The widget updates to show a "Processing..." message.
    b.  The captured text is sent to the Gemini API with a prompt to correct typos. The API is instructed to return the original text if no typos are found.
    c.  The API's response is parsed.
    d.  If successful, the corrected (or original) text is copied to the system clipboard.
    e.  The widget is destroyed.
    f.  A Ctrl+V (paste) command is simulated to paste the text into the source application.
    g.  If there are API errors, parsing errors, or no changes were made by the API, the widget displays an appropriate message for a short duration before closing.
5.  Pressing the Escape key while the widget is visible will close it.

## Contributing

Details will be added in `CONTRIBUTING.md`. For now, feel free to open issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
