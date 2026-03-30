# Installation Verification

After installing Personal History in a Python virtual environment, verify everything works correctly.

## Quick Verification

Run the verification script:

```bash
# After activating your virtual environment
python3 verify_installation.py
```

This will test:
1. Module imports
2. Core functionality
3. Schema validation
4. File operations
5. CLI availability

## Manual Verification Steps

### 1. Check Installation
```bash
pip show personal-history
```

Should show:
```
Name: personal-history
Version: 0.1.0
Summary: Personal History Format Implementation
Location: /path/to/your/venv/lib/python3.x/site-packages
```

### 2. Test Imports
```python
python3 -c "
import ph.v001.core
import ph.v001.schema
import ph.v001.cli
print('✅ All modules imported successfully')
"
```

### 3. Test Core Functionality
```python
python3 -c "
from ph.v001.core import PersonalHistoryV001
identity = PersonalHistoryV001.create_identity('Test User')
print(f'✅ Identity created: {identity[\"identity_hash\"][:16]}...')
"
```

### 4. Test CLI
```bash
# Via python -m
python3 -m ph.v001.cli --help

# Or if entry point is installed
ph --help
```

### 5. Run Existing Tests
```bash
# Simple test (no pytest required)
python3 test_simple.py

# Existing test
python3 ph/v001/test_basic.py
```

## Expected Output

Successful installation should show:
```
============================================================
Personal History Installation Verification
============================================================
Python: 3.x.x
Working directory: /path/to/personal_history

============================================================
1. Testing Module Imports
============================================================
✅ ph.v001.core.PersonalHistoryV001
✅ ph.v001.schema.validate_ph_file
✅ ph.v001.cli.main

============================================================
2. Testing Core Functionality
============================================================
✅ Identity created: abc123...
✅ Activity created: work
✅ Day created: 2024-01-01
✅ File created with 1 days

============================================================
3. Testing Schema Validation
============================================================
✅ Minimal file validation passed
✅ Complex file validation passed

============================================================
4. Testing File Operations
============================================================
✅ File saved to: /tmp/test_verification.ph.json
✅ File loaded back

============================================================
5. Testing CLI Availability
============================================================
✅ CLI is available via python -m

============================================================
Verification Summary
============================================================
✅ Module Imports
✅ Core Functionality
✅ Schema Validation
✅ File Operations
✅ CLI Availability

============================================================
🎉 SUCCESS: Personal History is correctly installed!
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'ph'"
**Solution**: Make sure you installed in development mode:
```bash
pip install -e .
```

### Issue: CLI command not found
**Solution**: The entry point might not be registered. Use:
```bash
python3 -m ph.v001.cli --help
```

### Issue: Cryptography library errors
**Solution**: Install system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev

# macOS with Homebrew
brew install openssl

# Then reinstall
pip install --upgrade pip
pip install -e .
```

### Issue: Tests fail with signature errors
**Solution**: Files created by `create_file()` have `signature: None`. Add a dummy signature for testing:
```python
ph_file["signature"] = "a" * 128
```

## Development Verification

For development, also run:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run pytest tests
make test

# Run with coverage
make test-cov
```

## Continuous Integration

The `tests/integration/test_installation.py` file contains automated tests that verify installation works correctly. These tests run in CI environments to ensure the package remains installable.