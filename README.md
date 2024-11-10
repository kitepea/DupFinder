## Requirements

- Python 3.x
- `pip`
- `PyInstaller`

### 1. Create a Virtual Environment in VS Code

Press `Ctrl+Shift+P`, type `Python: Create Environment`, and select `venv`.

### 2. Install Dependencies

1. Activate the virtual environment:
   - **Windows:** `.\venv\Scripts\Activate`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Run the Application

```bash
python main.py
```

### 4. Create Standalone Executable

In active virtual environment, run PyInstaller:
   ```bash
   pyinstaller --onefile --noconsole main.py
   ```

### 5. Find the Executable

After PyInstaller runs, the `.exe` (Windows) will be in the `/dist` directory:
```
/dist
    main.exe
```