# Personal History Format v0.01 - Python Implementation

## Overview

This is the Python implementation of the Personal History Format v0.01 specification. It provides:

1. **Core library** (`core.py`) - File format and cryptographic operations
2. **CLI tool** (`cli.py`) - Command line interface for daily use
3. **Example files** - Sample .ph.json files and usage examples

## Installation

### Option 1: Install locally
```bash
cd personal_history/ph/v001
pip install -e .  # Or: python3 setup.py develop
```

### Option 2: Use directly (no installation)
```bash
cd personal_history/ph/v001
python3 -m cli [command]
```

### Dependencies
```bash
pip install cryptography  # For real cryptographic operations
# Or use simulated mode (no installation needed)
```

## Quick Start

### 1. Initialize your identity
```bash
ph init --name "Your Name"
# Creates: ~/.personal_history/identity.json
```

### 2. Add activities throughout the day
```bash
# Add work activity
ph add work --duration 120 --project "personal_history"

# Add family activity  
ph add family --duration 45 --with-people "wife,son" --meal "dinner"

# Add exercise
ph add exercise --duration 30 --distance 5.2
```

### 3. Check pending activities
```bash
ph pending
# Shows activities waiting to be synced
```

### 4. Sync to your history file
```bash
ph sync
# Reviews, commits, and signs activities
# Creates: ~/.personal_history/history.ph.json
```

### 5. Analyze your time
```bash
ph analyze ~/.personal_history/history.ph.json
# Shows time distribution by activity type
```

## Architecture

### File Structure
```
~/.personal_history/
├── identity.json          # Your cryptographic identity
├── pending.json          # Activities waiting to sync
└── history.ph.json       # Your canonical history file
```

### Data Flow
1. **Quick Entry** → `ph add` → Stores in `pending.json`
2. **Review & Commit** → `ph sync` → Moves to `history.ph.json`
3. **Analysis** → `ph analyze` → Reads from `history.ph.json`

### Privacy Model
- **Duration visible**: "Work: 2 hours"
- **Exact times hidden**: "9:00-11:00" hidden in cryptographic commitment
- **Selective disclosure**: Can reveal exact times later if needed

## Core Features

### ✅ Implemented in v0.01:
- Forward-secure hash chain (can't forge past)
- Hidden exact timestamps with commitments
- Ed25519 signatures for file authenticity
- Basic time analysis
- Shareable/non-shareable activities
- CLI for daily use

### 🔜 Planned for future versions:
- Multimedia evidence support
- Advanced permissions system
- Chapter organization
- Mobile app interface
- Social sharing features

## API Reference

### Core Library (`core.py`)

```python
from personal_history.ph.v001.core import PersonalHistoryV001

# Create identity
identity = PersonalHistoryV001.create_identity(name="Your Name")

# Create activity (exact times hidden)
activity = PersonalHistoryV001.create_activity(
    type="work",
    data={"project": "x"},
    duration=120,  # minutes
    shareable=True
)

# Create day with forward-secure hash
day = PersonalHistoryV001.create_day(
    date="2024-01-01",
    activities=[activity],
    note="Daily note"
)

# Create and sign file
ph_file = PersonalHistoryV001.create_file(identity, [day])
signature = PersonalHistoryV001.sign_file(ph_file, identity["private_key"])
ph_file["signature"] = signature

# Save to file
PersonalHistoryV001.save_file(ph_file, "my_history.ph.json")

# Analyze time
analysis = PersonalHistoryV001.analyze_time(ph_file)
```

### CLI Commands

| Command | Description |
|---------|-------------|
| `ph init [--name NAME]` | Initialize new identity |
| `ph add TYPE [options]` | Add activity to pending |
| `ph pending` | Show pending activities |
| `ph sync [--yes]` | Sync pending to history file |
| `ph verify FILE.ph.json` | Verify file integrity |
| `ph analyze FILE.ph.json` | Analyze time distribution |
| `ph demo` | Run demonstration |

## Example .ph.json File

```json
{
  "version": "0.01.0",
  "identity": {
    "hash": "a1b2c3d4...",
    "name": "William Acevedo"
  },
  "timeline": [
    {
      "date": "2024-01-01",
      "timestamp": {
        "commitment": "b2c3d4e5..."
      },
      "activities": [
        {
          "type": "work",
          "data": {"project": "personal_history"},
          "duration": 120,
          "timestamp": {
            "commitment": "c3d4e5f6..."
          },
          "shareable": true,
          "hash": "d4e5f6a7..."
        }
      ],
      "hash": "e5f6a7b8...",
      "note": "Good start to the year"
    }
  ],
  "signature": "f6a7b8c9..."
}
```

## Development

### Running Tests
```bash
cd personal_history/ph/v001
python3 test_basic.py
```

### Project Structure
```
personal_history/ph/v001/
├── __init__.py          # Package definition
├── core.py              # Core implementation
├── cli.py               # Command line interface
├── setup.py             # Installation script
├── test_basic.py        # Basic tests
└── README.md            # This file
```

### Adding Features
1. Extend `core.py` with new functionality
2. Add corresponding CLI command in `cli.py`
3. Update tests in `test_basic.py`
4. Update documentation in `README.md`

## Next Steps

### Phase 1 (Week 1-2): Python Core ✓
- [x] Core file format implementation
- [x] Basic CLI tool
- [x] Cryptographic operations
- [x] Example files

### Phase 2 (Month 1): Web Dashboard
- [ ] React/Next.js web interface
- [ ] Time visualization
- [ ] File upload/download
- [ ] Social sharing previews

### Phase 3 (Month 2+): Mobile App
- [ ] React Native or Flutter app
- [ ] Offline sync
- [ ] Notifications
- [ ] Camera integration

## License

MIT License - See LICENSE file for details.

## Contributing

This is the reference implementation of the Personal History Format v0.01 specification. The format itself is open for anyone to implement in any language.

For the Python implementation:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request