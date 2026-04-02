# Personal History - Virtual Environment Installation

## Automatic Installation with Virtual Environment

Personal History now includes automatic virtual environment creation to ensure all dependencies (including cryptography) are installed correctly.

### Quick Start (Recommended)

#### On Linux/macOS:
```bash
# Make install.sh executable
chmod +x install.sh

# Run installation
./install.sh
```

#### On Windows:
```bash
# Run Python installer
python install.py
```

#### Using Make:
```bash
make install-venv
```

### What the Installer Does

1. **Checks Python version** (requires 3.8+)
2. **Creates virtual environment** (`.venv` directory)
3. **Installs package** in development mode with all dependencies
4. **Verifies installation**
5. **Creates activation scripts** for easy use

### Manual Virtual Environment Setup

If you prefer manual setup:

```bash
# 1. Create virtual environment
python3 -m venv .venv

# 2. Activate it
# Linux/macOS:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate.bat

# 3. Install package
pip install -e .

# 4. Verify
ph --help
```

### Using Personal History After Installation

#### Activate Virtual Environment:
```bash
# Using provided script
source activate.sh

# Or manually
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate.bat  # Windows
```

#### Use Personal History Commands:
```bash
ph --help                 # Show all commands
ph demo                   # Run demonstration
ph init                   # Create identity
ph add "Worked on project" --duration 90  # Add activity
```

#### Deactivate When Done:
```bash
deactivate
```

### Why Virtual Environment?

1. **Isolation**: Keeps Personal History dependencies separate from system Python
2. **Consistency**: Ensures correct versions of all dependencies
3. **Cryptography**: Automatically installs the cryptography library
4. **Cleanup**: Easy to remove (just delete `.venv` directory)

### Troubleshooting

#### "Command not found: ph"
- Make sure virtual environment is activated
- Run `source activate.sh` or `source .venv/bin/activate`

#### Installation fails
- Check Python version: `python3 --version` (needs 3.8+)
- Ensure you have write permissions in the directory
- Try manual setup: `python3 -m venv .venv && source .venv/bin/activate && pip install -e .`

#### Cryptography not installed
- The installer should install it automatically
- Manual fix: `pip install cryptography>=42.0.0`

### Development

For development work, install additional dependencies:

```bash
# Activate virtual environment first
source activate.sh

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

### Files Created by Installer

- `.venv/` - Virtual environment directory
- `activate.sh` - Activation script (Linux/macOS)
- `activate.bat` - Activation script (Windows)
- `INSTALLATION_USAGE.md` - Usage instructions

### Cleaning Up

To remove the virtual environment and all installed files:

```bash
make clean-venv
```

Or manually:
```bash
rm -rf .venv activate.sh activate.bat INSTALLATION_USAGE.md
```