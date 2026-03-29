# Personal History v0.01 - Quick Start

## 🚀 Get Started in 5 Minutes

### 1. Get the Code
```bash
# On your laptop, in your personal_history directory:
git pull origin main
# OR if conflicts, just copy the new files manually
```

### 2. Install
```bash
cd personal_history
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -e .
```

### 3. Test
```bash
ph --help
ph demo
```

### 4. Start Using
```bash
ph init --name "William"
ph add work --duration 120 --project "testing"
ph pending
ph sync --yes
ph analyze ~/.personal_history/history.ph.json
```

## 📁 What's New

### Complete v0.01 Implementation:
- `ph/v001/core.py` - All cryptographic operations
- `ph/v001/cli.py` - Full command line interface
- `setup.py` - Proper package installation
- `dev_setup.py` - Development helper

### Key Features Working:
- ✅ Forward-secure hash chain
- ✅ Hidden exact timestamps
- ✅ Ed25519 signatures
- ✅ CLI for daily use
- ✅ Time analysis
- ✅ Shareable export

## 🔧 Fix for Your Installation Issue

**Problem:** `ModuleNotFoundError: No module named 'personal_history'`

**Cause:** Installed from `ph/v001/` instead of root.

**Fix:**
```bash
# Install from ROOT directory
cd /path/to/personal_history  # This directory!
pip install -e .
```

## 📝 Next Steps

1. **Test the system** yourself for a few days
2. **Identify pain points** and improvements
3. **Decide next phase**: Web dashboard or mobile app
4. **Share feedback** for v0.02 planning

## 💡 Pro Tip

Use the development helper:
```bash
python3 dev_setup.py
# Automatically finds root and installs
```

## 🆘 Need Help?

Check:
- `ph/v001/README.md` - Detailed documentation
- `ph/v001/example_usage.py` - Working examples
- `PULL_AND_PUSH.md` - Git instructions

**v0.01 is complete and ready for real usage!** 🎉