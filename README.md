# Multi-Language Source Code Optimization Tool

A student-level project demonstrating the **Code Optimization** phase of Compiler Design. The tool analyzes C, C++, and Java source code, detects inefficient patterns, applies simple optimizations, and outputs optimized code.

## Supported Languages

- **C**
- **C++**
- **Java**

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python (Flask) |
| Processing | Regex, String manipulation |

## Project Structure

```
phase3/
├── backend/optimizer/
│   ├── app.py              # Flask API
│   ├── analyzer.py         # Code analysis & pattern detection
│   ├── optimizations.py    # Optimization implementations
│   └── language_detector.py# Auto language detection
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── requirements.txt
└── README.md
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server (from project root):
   ```bash
   cd backend/optimizer
   py app.py
   ```

3. Open `http://127.0.0.1:5001` in your browser. The app now serves both the frontend and API.

## Usage

1. Paste C, C++, or Java code in the input area.
2. Select language (Auto-detect, C, C++, or Java).
3. Click **Optimize Code** or press `Ctrl+Enter`.
4. View optimized code, statistics, and analysis report.

## Optimization Techniques

| Technique | Description |
|-----------|-------------|
| Constant Folding | Evaluates expressions like `2+3` → `5` |
| Dead Code Elimination | Removes unreachable code after return/break/continue |
| Redundant Assignment Removal | Removes `x = x;` |
| Expression Simplification | Simplifies `x = x+0` → `x;` and `x = x*1` → `x;` |

## Learning Path

1. **analyzer.py** – Core analysis logic
2. **optimizations.py** – Transformation patterns
3. **language_detector.py** – Language detection
4. **app.py** – API orchestration

## License

Educational use.
