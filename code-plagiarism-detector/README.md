# Code Plagiarism Detector

A web-based application built with Flask to detect plagiarism in source code. It allows users to compare two snippets of code and calculates a similarity score using a combination of textual, token-based, and AST (Abstract Syntax Tree) algorithms. The system also visually highlights plagiarized lines.

## Features

- **User Authentication**: Secure signup and login system using SQLite3 and password hashing.
- **Multiple Similarity Algorithms**:
  - **AST-based Comparison**: Analyzes the structural logic of the Python code using Abstract Syntax Trees (`ast`), ignoring variable name changes and formatting.
  - **Machine Learning (TF-IDF)**: Uses `scikit-learn` to calculate the cosine similarity between tokenized code strings.
  - **Text & Token Similarity**: Employs structural matching using `difflib.SequenceMatcher` for fine-grained text and token comparisons.
- **Code Highlighting**: Visually highlights lines in both code snippets that have high similarity (>60% text match).
- **Code Preprocessing**: Strips out comments, empty lines, and trailing spaces prior to analysis for better accuracy.
- **Responsive Web UI**: Modern interface with dedicated landing, signup, login, and detector views.

## Project Structure

```text
code-plagiarism-detector/
├── app.py                # Main Flask application and routing
├── database.db           # SQLite database for storing user accounts
├── requirements.txt      # Python dependencies
├── plagiarism/           # Core plagiarism detection logic
│   ├── ast_logic.py      # Abstract Syntax Tree structural comparison
│   ├── preprocess.py     # Code cleaning (removes comments, whitespace)
│   └── similarity.py     # TF-IDF, Token, and Text similarity + highlighting logic
├── templates/            # HTML templates for the UI
│   ├── landing.html
│   ├── login.html
│   ├── signup.html
│   └── detector.html     # Main detector interface
└── static/               # CSS and JS files
    └── style.css         # Styling and custom background clip fixes
```

## Setup & Installation

1. **Clone the repository** (or navigate to the project folder):
   ```bash
   cd e:\pythonProjects\code-plagiarism-detector
   ```

2. **Install requirements**:
   Ensure you have Python installed, then install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure you run this within your configured virtual environment if applicable).*

3. **Run the Application**:
   Start the Flask development server:
   ```bash
   python app.py
   ```

4. **Access the Web Interface**:
   Open your browser and navigate to `http://127.0.0.1:5000`.

## How It Works

1. **Register/Login**: Users explicitly need to successfully log in to access the detector dashboard.
2. **Submit Code**: Users paste two code snippets in the detector. You can optionally toggle "Use AST for structural comparison".
3. **Detection Process**:
    - **Preprocessing**: Code comments and empty lines are removed to leave only functional code.
    - **AST Check** (if enabled): Parses the logic visually using the structure. Fallbacks to hybrid algorithm if a syntax error occurs or code is unparseable.
    - **Hybrid Matcher**: Calculates a weighted similarity score using `scikit-learn` Cosine Similarity (40%), Token Matcher (40%), and Text Sequence Matcher (20%).
4. **Final Result**: Displays the calculated plagiarism severity (High, Moderate, Low), and highlights identical logic.
