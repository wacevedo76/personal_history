# Personal History Project

## Quick Start

### 1. Navigate to this directory
```bash
cd /path/to/personal_history
```

### 2. Create and activate virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```

### 3. Install the package
```bash
pip install -e .
```

### 4. Test installation
```bash
ph --help
ph demo
```

## Project Structure

```
personal_history/
├── setup.py              # Install from HERE
├── dev_setup.py          # Development helper script
├── README.md             # This file
└── ph/
    └── v001/             # Version 0.01 implementation
        ├── core.py       # Core functionality
        ├── cli.py        # Command line interface
        ├── example_usage.py
        └── README.md     # Detailed documentation
```

## Development

### Install for Development
```bash
# From the root directory (this one)
pip install -e .

# OR use the helper script from anywhere in the project
python3 dev_setup.py
```

### Why Install from Root?
Python packaging expects the top-level package (`personal_history`) to be the root. Installing from `ph/v001/` causes import errors.

### Editable Install (-e)
The `-e` flag means:
- Changes to source code are immediately available
- No need to reinstall after edits
- Perfect for development

## Troubleshooting

### "ModuleNotFoundError: No module named 'personal_history'"
You installed from the wrong directory. Fix:
```bash
cd /path/to/personal_history  # This directory!
pip install -e .
```

### "ph command not found"
Make sure:
1. Virtual environment is activated (`source venv/bin/activate`)
2. Installation succeeded (`pip list | grep personal-history`)
3. `~/.local/bin` or `venv/bin` is in your PATH

### Want to start over?
```bash
# Remove everything
deactivate
rm -rf venv/
pip uninstall personal-history

# Fresh start
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Usage

See `ph/v001/README.md` for detailed usage instructions.

Basic commands:
```bash
ph init --name "Your Name"
ph add work --duration 120 --project "test"
ph pending
ph sync --yes
ph analyze ~/.personal_history/history.ph.json
```