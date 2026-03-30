This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Copyright 2024 William Acevedo


# PERSONAL HISTORY

## Goals
PERSONAL HISTORY is way to quickly and easily journal all personal human activity
that adds verification to all entries.

## Rational
Now you may be wondering, why would anyone ever want to do this.
Other questions and concerns regarding privacy, ethics, and public safty arise. 

Setting these concerns aside for a moment, let me supply some, for what many may
agree is (or should be) a fundamental right of any human being:

* The Right to Free Speach

Many will argue that all speech should not be free, However, there is
particularly one aspect of Free Speech the I would like to focus on:

* That aspect is the Freedom to Share

This Freedom is not being attacted by any government, but by technology.
It is so easy the manipulate video, audio, using modern software, not even 
mentioning text, because mass text manipulation tools have existed not shortly 
after the invention of the microcontroller (not sure, maybe even earlier) but 
now have become even tools a lay person can use.

We now have the technology to map the human face digitally, and use this 
digital information to replicate that person's likeness virtually, on still image and
in video. Grant it, the technology is in its early stages, but with the rise
more powerful machines, and software development, and Artificial Intelligence 
it will no doubt improve exponetially relativly quickly.

There needs to be a quick, effortless, and most importantly, a method 
to what I term "Irrifutable Verification" of tracking aspects of life.

Bind to this need is the Right To Share. 

## The Right To Share

All People like to share. 

How many of us have any sort of social media account?
And even if you don't, have you never shown a photo album of any kind to
another person? Or shared a story? To any other human? Ever?

We all like to share. The motivations behind, or the countless other implications
suggested by this statement aside for a moment, and realize that it is the rare
human who has lived to maturity and never shared a photo, a memory, or story 
or a moment which they found memorable.

Couple with the Right to Free Speech, which includes the right not to be compelled 
to say anything.

## What is Personal History?

The Personal History file is simply a JSON data file where you can quickly record, and
effotlessly save whatever it is you want to share, in a file which you 
completely own. Every set of shared data is then used in conjunction with 
other unique data to generate a hash (the hashin algorithm used is sha256, for reference,
but will will simply be refered to as hash for the remainder of this document)
key that is unique and directly tide to the data you shared.

If the data is changed or manipuated in any way, the generated key will not only 
not match coresponding data, but also compromising the integrity of all data 
entered thereafter.

The goal is to generate a file, which you keep, like a journal, that  
is secure and contains only data you choose to share.

This makes you, the individual, the owner of your data.

There are so many aspects of this, especially with modern Analytics tools, that
compelled me to start this project. However, the one aspect that excites me 
most is the idea that now, you can be the true owner of what your share
you control whatever narative you wish to project to the world, verifiably.

## Personal History Schema

Here is a rough idea of what the Personal History data file would look like:

```
{"profile": {
    "username": "wacevedo",
    "firstname": "William",
    "lastname": "Acevedo",
    "password": "encrypted_password"
  },
  "years": [
    {
      "year": 2023,
      "year_hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
      "months": [
        {
          "month": 12,
          "month_hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
          "days": [
            {
              "date": 09,
              "day_hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
              "habits": {
                "pushups": {
                  "pushups-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "shareable": "true",
                  "completed": "100"
                },
                "pilaties": {
                  "pilaties-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "shareable": "true",
                  "completed": "1"
                },
                "wallsits": {
                  "wallsits-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "shareable": "true",
                  "completed": "1"
                },
                "sqats": {
                  "sqats-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "shareable": "true",
                  "completed": "20"
                },
                "meditation": {
                  "meditation-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "sharable": "true",
                  "completed": "1"
                }
              }
            },
            {
              "date": 08,
              "day_hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
              "habits": {
                "pushups": {
                  "pushups-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "shareable": "true",
                  "completed": "100"
                },
                "pilaties": {
                  "pilaties-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "shareable": "true",
                  "completed": "1"
                },
                "wallsits": {
                  "wallsits-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "shareable": "true",
                  "completed": "1"
                },
                "sqats": {
                  "sqats-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "shareable": "true",
                  "completed": "20"
                },
                "meditation": {
                  "meditation-hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
                  "sharable": "true",
                  "completed": "1"
                }
              }
            }
          ]
        }
      ]
    }
  ]
}
```

## How It works:
Whenever a new Personal History file is created it will generate:
* A data Set containing:
  * First name, Last name, date, and time
  * two hashed values representing two pieces of unique and private Personal identifying information (e.g., taxid, password)

example in python:
```
-- example values:

firstname = "herman", 
lastname = "munster", 
tax_id = "8765309", 
password = "123456789"
```

-- example output of function used to generate desired output:
```
generate_priliminary_hash_values(firstname, lastname, tax_id, password)
```

output:
There are two sets of data created:
..* the date and time this data was created, and the first and last name in clear text.
..* Hashes created from the firstname, lastname
```
[
    {'encoded_creation_time': '1710540432.688816', # epoch time number converts to 15/03/2024 23:07
     'firstname': 'herman',
     'lastname': 'munster'},

    {'hashed_creation_time': '7b6197b0e5f3f29c2a1df1715c287050b91ecfe68e2f04d572c74ead907c16e6',
    'hashed_tax_id': '5cfaae462bf88066c36bed21fb07bbee16acf6b110840f57c7b2a760dbc80919',         
    'hashed_password': '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225',
    'hashed_firstname': '3bf39bf3fe465c0600105b3451f274fa9f05b3c706f022608c0fb28285fe5cbf',
    'hashed_lastname': '7cbd75a33e3f9ceba58eab97dd18cd7866d398f3d56542d64e80a369a36dadab'}
]
```

### to reiterate:
* The data creation time (epoch) is 1710540432.688816, which converts to 15/03/2024 23:07 **equals** 7b6197b0e5f3f29c2a1df1715c287050b91ecfe68e2f04d572c74ead907c16e6
* If any part of the date or time is changed, in any form, the original hash number will not match.
* This process of verification can be done with any, and all forms of data (text, images, video, audio)
    
### This data set is saved within the Personal History File, and then this data is used to generate the file name and used as the first hash which identifies the current year.

## Why is hashing important?
Hashing is "one way", meaning that while the information can be verified with the hash number,
the hash number can not be used to generate, or get the original information, i,e:

your tax ID is: 123456789, and this number is used generate "5cfaae462bf88066c36bed21fb07bbee16acf6b110840f57c7b2a760dbc80919",
however, "5cfaae462bf88066c36bed21fb07bbee16acf6b110840f57c7b2a760dbc80919" can not be used to 
generate your tax ID. This is a common menthod of authentication for websites, meaning this is how 
they verify your password without storing your actual password on their servers.

example in python code using previously generated data:
```
personal_history_userdata01 = [
    {'encoded_creation_time': '1710540432.688816', <- epoch time number converts to 15/03/2024 23:07 ```
     'firstname': 'herman',
     'lastname': 'munster'},
                                                                                                     
    {'hashed_creation_time': '7b6197b0e5f3f29c2a1df1715c287050b91ecfe68e2f04d572c74ead907c16e6',
    'hashed_tax_id': '5cfaae462bf88066c36bed21fb07bbee16acf6b110840f57c7b2a760dbc80919',         
    'hashed_password': '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225',
    'hashed_firstname': '3bf39bf3fe465c0600105b3451f274fa9f05b3c706f022608c0fb28285fe5cbf',
    'hashed_lastname': '7cbd75a33e3f9ceba58eab97dd18cd7866d398f3d56542d64e80a369a36dadab'}
]
```
Using this data, we can now generate the file name and the hash for the current year:

Possible function in Python:
```
create_ph_hashed_day_file_name(personal_history_userdata01)
```
Output:
```
['b8b77a5b311fb3a27b425bcab6a170fc499a2fe68170f50a2baa82bdacc3ea25',
 [{'encoded_creation_time': '1710540432.688816',
   'firstname': 'herman',
   'lastname': 'munster'},
  {'hashed_creation_time': '7b6197b0e5f3f29c2a1df1715c287050b91ecfe68e2f04d572c74ead907c16e6',
   'hashed_tax_id': '5cfaae462bf88066c36bed21fb07bbee16acf6b110840f57c7b2a760dbc80919',
   'hashed_password': '15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225',
   'hashed_firstname': '3bf39bf3fe465c0600105b3451f274fa9f05b3c706f022608c0fb28285fe5cbf',
   'hashed_lastname': '7cbd75a33e3f9ceba58eab97dd18cd7866d398f3d56542d64e80a369a36dadab'}]]
```

The first value in the list provided above:
```
b8b77a5b311fb3a27b425bcab6a170fc499a2fe68170f50a2baa82bdacc3ea25
```
Is a hash value generated from the combination of:
* hashed_creation_time
* hashed_tax_id
* hashed_password
* hashed_firstname
* hashed_lastname

and will be both the primary file name, and the hashed value of the current year.

filename:
```
b8b77a5b311fb3a27b425bcab6a170fc499a2fe68170f50a2baa82bdacc3ea25.ph
```
and contents of file:
```
{"profile": {
    "firstname": "herman",
    "lastname": "munster",
    "creation_date": "1710540432.688816",
    "tax_id": "5cfaae462bf88066c36bed21fb07bbee16acf6b110840f57c7b2a760dbc80919"
    "password": "15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225"
  },
  "years": [
    {
      "year": 2023,
      "year_hash": "7f83b1657ff1fc53b92dc18148a1d65dfc2d4b1fa3d677284addd200126d9069",
```
## Okay, so now what?
Once the year hash has been generated, the content creation flow goes as follows:

#### In essense, each layer of data is created by using a combination of:
* up to the previous 10 hashes.
* and any relavent data needed at that specific current level.

#### The month hash is generated by using a combination of:
* the preceeding hash (in this case, the year hash).
* the Time the Month hash creation takes place.   
*NOTE*: the month container has its own hash for identification, as well as data integrity purposes

#### The Day hash is generated by using a combination of:
* The combined text of both the the month and year hashes
* and the text of the data that is beeing collected.
* and the date and time the data is collected.  

There may be multiple, dozens, multiple data points per day, and each data point will have its own hash, and the day hash will be a combination of all the data point hashes.

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

### 📊 Data Structure

Personal History v0.01 files contain:
- **Identity**: Cryptographic identity with public/private keys
- **Timeline**: Chronological days with activities
- **Activities**: Time-stamped entries with optional data
- **Hashes**: SHA-256 hashes for verification
- **Signatures**: Optional Ed25519 signatures

Each activity includes:
- Type (work, exercise, meal, etc.)
- Duration in minutes
- Optional data (project, distance, people, etc.)
- Shareable flag for privacy control
- Exact timestamps (hidden in commitment)
- Cryptographic commitments for verification

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

### Original Vision → Current Implementation

| Original Concept | Current v0.01 Implementation |
|-----------------|-----------------------------|
| **Philosophical foundation** of "Right to Share" | ✅ Preserved in architecture |
| **JSON data structure** for personal history | ✅ Implemented with schema validation |
| **Hash-based verification** chain | ✅ SHA-256 hashes with cryptographic commitments |
| **Privacy controls** (shareable flags) | ✅ Activity-level privacy controls |
| **Timestamp integrity** | ✅ ISO 8601 timestamps with hidden exact times |
| **Command-line interface** | ✅ Full-featured CLI with 11 commands |
| **Time tracking** | ✅ Start/stop/tasks system with automatic timing |
| **Data analysis** | ✅ Analyze, timestamps, CSV export features |
| **Extensible architecture** | ✅ MVC pattern ready for APIs, web interfaces |

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