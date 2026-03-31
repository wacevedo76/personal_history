This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Copyright 2024 William Acevedo


# PERSONAL HISTORY

## Goals
PERSONAL HISTORY is a way to quickly and easily journal all personal human activity
that adds verification to all entries.

## Rationale
Now you may be wondering, why would anyone ever want to do this.
Other questions and concerns regarding privacy, ethics, and public safety arise. 

Setting these concerns aside for a moment, let me supply some reasons for what many may
agree is (or should be) a fundamental right of any human being:

* The Right to Free Speech

Many will argue that all speech should not be free. However, there is
particularly one aspect of Free Speech that I would like to focus on:

* That aspect is the Freedom to Share

This Freedom is not being attacked by any government, but by technology.
It is so easy to manipulate video and audio using modern software, not even 
mentioning text, because mass text manipulation tools have existed since shortly 
after the invention of the microcontroller (not sure, maybe even earlier) but 
now have become tools that even a lay person can use.

We now have the technology to map the human face digitally, and use this 
digital information to replicate that person's likeness virtually, in still images and
in video. Granted, the technology is in its early stages, but with the rise
of more powerful machines, software development, and Artificial Intelligence,
it will no doubt improve exponentially relatively quickly.

There needs to be a quick, effortless, and most importantly, a method 
to what I term "Irrefutable Verification" of tracking aspects of life.

Bound to this need is the Right To Share. 

## The Right To Share

All people like to share. 

How many of us have any sort of social media account?
And even if you don't, have you never shown a photo album of any kind to
another person? Or shared a story? With any other human? Ever?

We all like to share. The motivations behind, or the countless other implications
suggested by this statement set aside for a moment, and realize that it is the rare
human who has lived to maturity and never shared a photo, a memory, a story,
or a moment which they found memorable.

Coupled with the Right to Free Speech, which includes the right not to be compelled 
to say anything.

## What is Personal History?

The Personal History file is simply a JSON data file where you can quickly record, and
effortlessly save whatever it is you want to share, in a file which you 
completely own. Every set of shared data is then used in conjunction with 
other unique data to generate a hash (the hashing algorithm used is SHA-256, for reference,
but we will simply refer to it as hash for the remainder of this document)
key that is unique and directly tied to the data you shared.

If the data is changed or manipulated in any way, the generated key will not only 
not match corresponding data, but also compromise the integrity of all data 
entered thereafter.

The goal is to generate a file, which you keep, like a journal, that  
is secure and contains only data you choose to share.

This makes you, the individual, the owner of your data.

There are so many aspects of this, especially with modern Analytics tools, that
compelled me to start this project. However, the one aspect that excites me 
most is the idea that now, you can be the true owner of what you share,
you control whatever narrative you wish to project to the world, verifiably.

## Personal History Schema (v0.01)

Here is the actual schema for Personal History v0.01 files:

```json
{
  "version": "0.01.0",
  "identity": {
    "hash": "ef80b785e912a38d1ceb69f904e6421d170af9242644d9e397b7a3faf5cc4eb4",
    "name": "William"
  },
  "timeline": [
    {
      "date": "2024-03-30",
      "timestamp": {
        "commitment": "2e837676ffac7007790e77786bc9886fea1f75daa84518c53c175ca5d774efe5"
      },
      "activities": [
        {
          "type": "work",
          "data": {
            "project": "Personal History Development"
          },
          "duration": 120,
          "timestamp": {
            "commitment": "a7288cb555fbc77598a95e7bc5012f04a7fe82bcffe00fc2189a28c96af1df7d"
          },
          "shareable": true,
          "hash": "58ae00e2c2e31017bf8d79b45e7384e2f6219e400005fd2036eadd43a2ecc65f"
        },
        {
          "type": "exercise",
          "data": {
            "distance_km": 5.0
          },
          "duration": 45,
          "timestamp": {
            "commitment": "b8397cb555fbc77598a95e7bc5012f04a7fe82bcffe00fc2189a28c96af1df8e"
          },
          "shareable": true,
          "hash": "68bf11f3d3e42128cf9e8ac56e8495f3f732af511116fe3147fbde54b3fdd76g"
        },
        {
          "type": "family",
          "data": {
            "meal": "dinner",
            "with": ["spouse", "children"]
          },
          "duration": 90,
          "timestamp": {
            "commitment": "c9408dc666gcd886a9ba6f8cd6123g15b8gf93cdggf11gd329b39d07cbf2eg79f"
          },
          "shareable": false,
          "hash": "79cg22g4e4f53239dg0f9bd67f95a6g4g843bg622227gf4258cgef64c4gee87h"
        }
      ],
      "hash": "6b16dc99c18a266dd77448a4204ab28b99033dd20cf0040e1488054a9ff31d3b"
    },
    {
      "date": "2024-03-29",
      "timestamp": {
        "commitment": "3f948787ggbd81188a1f88897cd0997gfb2g86ebb95629d64d286db6e885gfc6"
      },
      "activities": [
        {
          "type": "learning",
          "data": {
            "topic": "Python MVC Architecture"
          },
          "duration": 180,
          "timestamp": {
            "commitment": "d0519ed777hde997bacb7g9de7234h26c9hg4dehhg22he43c4ae18dch3fh8ag0"
          },
          "shareable": true,
          "hash": "8adh33h5f5g6434ae1g0ace8g06b7h5h954ch733338hg5369dhfg75d5hff98i"
        }
      ],
      "hash": "7c27edaa29b377ee887559b531bc39ca0a144ee31dg1151f2599166b0gg42e4c"
    }
  ],
  "signature": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8"
}
```

### Schema Components

#### 1. **Root Level**
- `version`: Always "0.01.0" for v0.01
- `identity`: Cryptographic identity information
- `timeline`: Chronological list of days
- `signature`: Optional Ed25519 signature (128 hex characters)

#### 2. **Identity Object**
- `hash`: SHA-256 hash of the identity (64 hex characters)
- `name`: Optional human-readable name

#### 3. **Day Object** (in timeline)
- `date`: ISO 8601 date (YYYY-MM-DD)
- `timestamp.commitment`: Hash commitment for the day
- `activities`: List of activities for that day
- `hash`: SHA-256 hash of the day (64 hex characters)

#### 4. **Activity Object**
- `type`: Activity category (work, exercise, family, learning, planning, health, social)
- `data`: Optional activity-specific data (project, distance_km, meal, with people, etc.)
- `duration`: Duration in minutes (integer)
- `timestamp.commitment`: Hash commitment hiding exact start/end times
- `shareable`: Boolean indicating if activity can be shared publicly
- `hash`: SHA-256 hash of the activity (64 hex characters)

#### 5. **Hash Chain Verification**
- Each activity hash is computed from its content
- Day hash is computed from date + sorted activity hashes
- File can be signed with Ed25519 for cryptographic verification
- Changing any data breaks the hash chain

## How It Works (v0.01 Implementation)

Personal History v0.01 uses a modern cryptographic approach for identity and verification:

### 1. **Identity Creation**
When you run `ph init`, the system generates:
- **Ed25519 key pair** (public/private keys) for cryptographic signatures
- **Identity hash** derived from public key + salt + optional name
- **Salt** for additional security

Example identity creation:
```python
from ph.v001.models.identity import Identity

# Create and generate identity
identity = Identity(name="William")
identity.generate()

print(f"Identity Hash: {identity.identity_hash}")
print(f"Public Key: {identity.public_key[:32]}...")
print(f"Created: {identity.created_at}")
```

### 2. **Activity Creation with Timestamp Commitments**
Each activity includes exact timestamps that are cryptographically hidden:

```python
from ph.v001.models.activity import Activity
from datetime import datetime, timedelta

# Create an activity with exact timestamps
activity = Activity(
    activity_type="work",
    data={"project": "Personal History"},
    duration=120,  # 2 hours in minutes
    exact_start="2024-03-30T09:00:00Z",
    exact_end="2024-03-30T11:00:00Z",
    shareable=True
)

# The exact timestamps are hidden in a commitment
print(f"Activity Hash: {activity.hash}")
print(f"Timestamp Commitment: {activity.commitment}")
print(f"Shareable: {activity.shareable}")
```

### 3. **Hash Chain Verification**
The system creates a verifiable chain of hashes:

1. **Activity Hash**: SHA-256 of activity data + timestamps
2. **Day Hash**: SHA-256 of date + sorted activity hashes  
3. **File Hash**: SHA-256 of version + identity + sorted day hashes
4. **Signature**: Optional Ed25519 signature of file hash

### 4. **Timestamp Privacy**
Exact start/end times are stored in the `_private` field but hidden from the public file:
- `exact_start`: ISO 8601 timestamp when activity began
- `exact_end`: ISO 8601 timestamp when activity ended  
- `nonce`: Random value to prevent timing attacks
- `commitment`: SHA-256 hash of `exact_start + exact_end + nonce`

This allows verification that timestamps haven't been altered without revealing exact times.

### 5. **File Structure**
```
personal_history.ph.json
├── version: "0.01.0"
├── identity: {hash, name}
├── timeline: [
│   ├── day1: {date, hash, activities: [...]}
│   ├── day2: {date, hash, activities: [...]}
│   └── ...
│   ]
└── signature: "ed25519_signature_here" (optional)
```

## Why Cryptography Matters

### **Hash Functions (SHA-256)**
- **One-way**: Easy to compute hash, impossible to reverse
- **Deterministic**: Same input always produces same hash
- **Avalanche effect**: Tiny change produces completely different hash
- **Collision resistant**: Extremely unlikely two inputs produce same hash

Example:
```python
import hashlib

data = "Personal History Activity"
hash_result = hashlib.sha256(data.encode()).hexdigest()
# Result: "a1b2c3d4..." (64 hex characters)
# Change one character → completely different hash
```

### **Digital Signatures (Ed25519)**
- **Identity proof**: Proves file was created by identity owner
- **Integrity proof**: Proves file hasn't been altered
- **Non-repudiation**: Creator cannot deny creating the file

### **Timestamp Commitments**
- **Privacy**: Exact times hidden but verifiable
- **Integrity**: Can prove timestamps haven't changed
- **Selective disclosure**: Can reveal exact times later if needed

## Verification Process

Anyone can verify a Personal History file:

1. **Check hashes**: Recompute activity → day → file hashes
2. **Verify signature**: Validate Ed25519 signature if present  
3. **Check commitments**: Verify timestamp commitments match
4. **Validate schema**: Ensure JSON structure follows v0.01 spec

This creates what you termed "Irrefutable Verification" - cryptographic proof that the data is authentic and unaltered.

## Current Implementation (v0.01)

The project has evolved into a practical Python implementation with a command-line interface featuring:

### 🚀 Key Features

#### **Time Tracking System**
- `ph start <activity>` - Start timing any activity
- `ph stop <activity>` - Stop timing and calculate elapsed time
- `ph tasks` - View active timers and pending activities
- Automatic duration calculation (real elapsed time, not future time)

#### **Smart Duration Parsing**
- Multiple time formats: `"90"`, `"1h30"`, `"2h"`, `"45m"`, `"1.5h"`, `"1:30"`
- Case-insensitive, handles spaces
- Integrated with both manual entry and time tracking

#### **Data Analysis**
- `ph analyze` - Analyze time from history files (default file support)
- `ph timestamps` - Extract and analyze exact timestamps
- CSV export for spreadsheet analysis
- Time pattern analysis and reporting

#### **Verification & Integrity**
- Cryptographic identity generation (Ed25519)
- Hash chain verification for data integrity
- Timestamp commitments for privacy
- File signature validation

#### **MVC Architecture**
- Clean separation of models, controllers, and views
- Ready for multiple interfaces (CLI, API, Web, etc.)
- Backward compatible with existing code
- Extensible for future features

### 📊 v0.01 Data Structure

Personal History v0.01 implements a practical, cryptographically-verifiable format:

#### **Core Components**
- **Identity**: Ed25519 key pair + identity hash (not personal info like tax ID)
- **Timeline**: Simple chronological list of days (not nested years/months)
- **Activities**: Flexible entries with type, duration, and optional data
- **Hashes**: SHA-256 chain for verification (activity → day → file)
- **Signatures**: Optional Ed25519 signatures for cryptographic proof

#### **Activity Types (v0.01)**
- `work` - Professional activities (with optional `project` field)
- `family` - Family time (with optional `meal`, `with` people)
- `exercise` - Physical activity (with optional `distance_km`)
- `learning` - Educational activities (with optional `topic`)
- `planning` - Planning/organization activities
- `health` - Health/wellness activities
- `social` - Social interactions

#### **Privacy Controls**
- `shareable: true/false` - Per-activity privacy setting
- Timestamp commitments - Hide exact times while allowing verification
- No personal identifiers in public files - Only cryptographic hashes

#### **Compared to Original Vision**
The v0.01 implementation evolved from the original concept:
- **Simpler structure**: Timeline instead of nested years/months
- **Better cryptography**: Ed25519 signatures instead of password/tax ID hashes
- **Practical privacy**: Shareable flags instead of all-or-nothing
- **Extensible data**: Flexible activity data instead of fixed "habits"
- **Real-world usability**: CLI with time tracking instead of just file format

### Quick Start

#### 1. Navigate to this directory
```bash
cd /path/to/personal_history
```

#### 2. Create and activate virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```

#### 3. Install the package
```bash
pip install -e .
```

#### 4. Test installation
```bash
ph --help
ph demo
```

### Project Structure

```
personal_history/
├── setup.py              # Install from HERE
├── dev_setup.py          # Development helper script
├── README.md             # This file
└── ph/
    └── v001/             # Version 0.01 implementation
        ├── core.py       # Core functionality (legacy API)
        ├── cli.py        # Command line interface
        ├── schema.py     # JSON schema validation
        ├── timestamps.py # Timestamp utilities
        ├── models/       # Data models (MVC)
        ├── controllers/  # Business logic (MVC)
        ├── views/        # Presentation layers (MVC)
        ├── utils/        # Utilities
        ├── services/     # Shared services
        └── README.md     # Detailed technical documentation
```

### Complete Command Reference

#### Identity Management
```bash
# Initialize your identity
ph init --name "Your Name"

# Verify your identity file
ph verify ~/.personal_history/identity.json
```

#### Activity Management
```bash
# Add activities with smart duration parsing
ph add work --duration "1h30" --project "Personal History"
ph add exercise --duration "45m" --distance 5
ph add reading --duration "1.5h"
ph add cooking --meal "dinner" --with-people "family"
ph add meeting --duration "1:30" --project "team" --private

# Smart duration formats supported:
# - "90" (minutes)
# - "1h30" or "1hr30" (1 hour 30 minutes)
# - "2h" (2 hours)
# - "45m" (45 minutes)
# - "1.5h" (1.5 hours)
# - "1:30" (1 hour 30 minutes)
```

#### Time Tracking (New!)
```bash
# Start timing an activity
ph start "writing documentation" --type work --project "Personal History"
ph start "morning workout" --type exercise
ph start "cooking dinner" --type cooking --meal "pasta"

# Check active timers and pending activities
ph tasks

# Stop timing and calculate elapsed time
ph stop "writing documentation" --auto-add  # Auto-adds to pending
ph stop "morning workout"                   # Asks for confirmation

# View pending activities
ph pending
```

#### File Operations
```bash
# Sync pending activities to history file
ph sync

# Verify Personal History file
ph verify personal_history.ph.json

# Analyze time from history file (default: ~/personal_history.ph.json)
ph analyze
ph analyze --export-shareable  # Export shareable activities

# Extract and analyze timestamps
ph timestamps --summary        # Human-readable summary
ph timestamps --analyze        # JSON analysis of time patterns
ph timestamps --export-csv     # Export to CSV for spreadsheets
```

#### Demonstration
```bash
# Run a complete demonstration of all features
ph demo
```

### Example Workflows

#### Daily Time Tracking
```bash
# Morning routine
ph start "morning meditation" --type wellness
ph stop "morning meditation" --auto-add

ph start "breakfast" --type meal --meal "oatmeal"
ph stop "breakfast" --auto-add

# Work session
ph start "coding session" --type work --project "API Development"
# ... work for a while ...
ph stop "coding session" --auto-add

# Check what's pending
ph tasks
ph pending

# End of day sync
ph sync
```

#### Weekly Review
```bash
# Analyze your week
ph analyze

# Export timestamps for spreadsheet analysis
ph timestamps --export-csv

# Check file integrity
ph verify ~/personal_history.ph.json
```

#### Project Tracking
```bash
# Track time on specific projects
ph start "feature development" --type work --project "User Authentication"
ph start "bug fixing" --type work --project "API Performance"

# See active project work
ph tasks

# Stop and record
ph stop "feature development" --auto-add
ph stop "bug fixing" --auto-add

# Sync and analyze project time
ph sync
ph analyze
```

### Development

#### Git Branch Strategy
```
main    - Stable, production-ready releases
dev     - Development integration (current)
feature/* - Feature branches off dev
```

**Current branch:** `dev` (v0.01 implementation with MVC architecture)

#### Install for Development
```bash
# From the root directory (this one)
pip install -e .

# OR use the helper script from anywhere in the project
python3 dev_setup.py
```

#### Why Install from Root?
Python packaging expects the top-level package (`personal_history`) to be the root. Installing from `ph/v001/` causes import errors.

#### Editable Install (-e)
The `-e` flag means:
- Changes to source code are immediately available
- No need to reinstall after edits
- Perfect for development

### Troubleshooting

#### "ModuleNotFoundError: No module named 'personal_history'"
You installed from the wrong directory. Fix:
```bash
cd /path/to/personal_history  # This directory!
pip install -e .
```

#### "ph command not found"
Make sure:
1. Virtual environment is activated (`source venv/bin/activate`)
2. Installation succeeded (`pip list | grep personal-history`)
3. `~/.local/bin` or `venv/bin` is in your PATH

#### Want to start over?
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

## From Vision to Reality

### Evolution: Original Vision → v0.01 Implementation

| Original Concept | v0.01 Implementation | Notes |
|-----------------|---------------------|-------|
| **Nested structure** (years/months/days) | **Flat timeline** with days | Simplified for usability |
| **Personal identifiers** (tax ID, password) | **Cryptographic identity** (Ed25519 keys) | Better privacy & security |
| **Fixed "habits" structure** | **Flexible activity types** with optional data | More practical for real use |
| **All-or-nothing sharing** | **Per-activity `shareable` flag** | Granular privacy control |
| **Conceptual file format** | **Working CLI with 11 commands** | Actually usable tool |
| **Manual time entry** | **Smart duration parsing + time tracking** | `ph start/stop/tasks` commands |
| **Basic hash verification** | **Full hash chain + Ed25519 signatures** | Cryptographic proof |
| **Theoretical timestamp hiding** | **Actual timestamp commitments** | Hidden exact times, verifiable |
| **Static data structure** | **MVC architecture** | Ready for APIs, web interfaces |
| **Philosophical "Right to Share"** | **Practical implementation** | Vision realized in working code |

### What Makes Personal History Unique

1. **You Own Your Data** - Files are stored locally, not in the cloud
2. **Verifiable Integrity** - Cryptographic hashes prove data hasn't been altered
3. **Privacy by Design** - Share only what you want, keep private what you don't
4. **Effortless Tracking** - Smart duration parsing and automatic time tracking
5. **Future-Proof** - MVC architecture ready for new interfaces and features

## Getting Help

### Common Issues
```bash
# Command not found after install
source venv/bin/activate  # Make sure venv is activated
pip install -e .          # Reinstall if needed

# Import errors
cd /path/to/personal_history  # Install from root directory
pip uninstall personal-history -y && pip install -e .

# Testing features
ph demo  # Run the demonstration
ph --help  # See all commands
```

### Need More Help?
- Check `ph/v001/README.md` for technical details
- Run `ph <command> --help` for command-specific help
- Use `ph demo` to see all features in action

## Development

### Logging Module

Personal History includes a comprehensive logging module for development and debugging. The logging system tracks command execution, operations, errors, performance metrics, and user interactions.

#### Features
- **Multi-level logging**: Command, operation, error, performance, and user interaction logging
- **Multiple output formats**: Human-readable logs + structured JSON logs
- **Easy integration**: Decorators, context managers, and wrapper classes
- **Log analysis**: Built-in tools for analyzing and exporting logs

#### Quick Start

```python
# Basic logging usage
from ph.logging_module import get_logger

logger = get_logger()
logger.log_command("add", {"type": "work", "duration": "60"}, user="developer")
```

#### Integration Options

1. **Quick Patch** (Minimal changes):
```python
from ph.logging_integration import patch_existing_cli
patch_existing_cli()
# Existing CLI now logs everything
```

2. **New Entry Point** (Recommended):
```python
# ph_logged.py
from ph.logging_integration import LoggingCLIEntryPoint
LoggingCLIEntryPoint.main()
```

3. **Selective Integration**:
```python
from ph.logging_module import log_operation

@log_operation("create_activity", get_logger())
def create_activity(...):
    # Your code
```

#### Log Files
Logs are stored in `~/.personal_history/logs/`:
- `ph_YYYYMM.log` - Human-readable logs (monthly rotation)
- `ph_structured_YYYYMM.log` - JSON structured logs (monthly rotation)

#### Testing
Run the logging test suite:
```bash
python test_logging.py
```

#### Example
See `examples/logging_example.py` for a complete demonstration of all logging features.

For detailed documentation, see [LOGGING_MODULE.md](LOGGING_MODULE.md) and [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md).

### Running Tests
The project includes comprehensive test suites:

```bash
# Basic functionality tests
python test_simple.py

# Installation verification
python verify_installation.py

# Complete workflow test
python simple_ph_test.py

# Logging module tests
python test_logging.py
```

### Development Setup
1. Create virtual environment: `python3 -m venv venv`
2. Activate: `source venv/bin/activate`
3. Install in development mode: `pip install -e .`
4. Run tests to verify installation

## Contributing

The project uses a clean git workflow:
- `main` branch: Stable releases
- `dev` branch: Current development (you're here!)
- `feature/*` branches: Individual features

To contribute:
1. Fork the repository
2. Create a feature branch from `dev`
3. Make your changes
4. Submit a pull request to `dev`

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Copyright 2024 William Acevedo