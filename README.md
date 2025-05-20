# TypoFix Desktop App

TypoFix is a cross-platform desktop application that helps you correct typos in highlighted text using the Gemini AI API. When you highlight text in the app's input box, a small widget appears. Clicking this widget opens a container displaying the typo-free version of your text.

## Features (Planned)

*   Detects highlighted text in an input box.
*   Displays a clickable widget upon text selection.
*   Corrects typos using Gemini AI when the widget is clicked.
*   Shows corrected text in a separate container.
*   Cross-platform (Windows, macOS, Linux) with easy installation.

## Technology Stack

*   **Python:** Core application logic.
*   **Tkinter:** GUI framework.
*   **Requests:** For Gemini API communication.
*   **PyInstaller:** For packaging into standalone executables.
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
    .venv\Scripts\Activate.ps1
    # On macOS/Linux
    source .venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt 
    ```
    *(Note: `requirements.txt` will be created in a later phase)*
4.  **Set up your Gemini API Key:**
    *   Obtain an API key from Google's AI Platform.
    *   Store it as an environment variable `GEMINI_API_KEY` or create a `.env` file in the root directory with the line:
        ```
        GEMINI_API_KEY=your_api_key_here
        ```
        (The `.env` file is gitignored by default).
5.  **Run the application (once `app.py` is created):**
    ```bash
    python app.py
    ```

## Contributing

Details will be added in `CONTRIBUTING.md`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
