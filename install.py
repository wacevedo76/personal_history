#!/usr/bin/env python3
"""
Personal History Installation Script
Automatically creates a virtual environment and installs the package.
"""

import os
import sys
import subprocess
import venv
import shutil
from pathlib import Path
import platform

class PersonalHistoryInstaller:
    """Install Personal History with virtual environment"""
    
    def __init__(self, venv_name=".venv", install_dev=False):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / venv_name
        self.install_dev = install_dev
        self.is_windows = platform.system() == "Windows"
        
    def check_python_version(self):
        """Check Python version compatibility"""
        import sys
        if sys.version_info < (3, 8):
            print(f"❌ Python 3.8+ required, found {sys.version}")
            return False
        print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        return True
    
    def create_venv(self):
        """Create virtual environment"""
        print(f"\nCreating virtual environment at: {self.venv_path}")
        
        if self.venv_path.exists():
            print(f"Virtual environment already exists at {self.venv_path}")
            response = input("Recreate? [y/N]: ").strip().lower()
            if response == 'y':
                print("Removing existing virtual environment...")
                shutil.rmtree(self.venv_path)
            else:
                print("Using existing virtual environment")
                return True
        
        try:
            # Create virtual environment
            builder = venv.EnvBuilder(
                with_pip=True,
                symlinks=not self.is_windows,
                upgrade=False
            )
            builder.create(self.venv_path)
            print("✓ Virtual environment created")
            return True
        except Exception as e:
            print(f"❌ Failed to create virtual environment: {e}")
            return False
    
    def get_venv_python(self):
        """Get path to virtual environment Python executable"""
        if self.is_windows:
            python_exe = self.venv_path / "Scripts" / "python.exe"
        else:
            python_exe = self.venv_path / "bin" / "python"
        
        if not python_exe.exists():
            # Try alternative naming
            if self.is_windows:
                python_exe = self.venv_path / "Scripts" / "python3.exe"
            else:
                python_exe = self.venv_path / "bin" / "python3"
        
        return python_exe
    
    def get_venv_pip(self):
        """Get path to virtual environment pip"""
        if self.is_windows:
            pip_exe = self.venv_path / "Scripts" / "pip.exe"
        else:
            pip_exe = self.venv_path / "bin" / "pip"
        
        if not pip_exe.exists():
            # Try alternative naming
            if self.is_windows:
                pip_exe = self.venv_path / "Scripts" / "pip3.exe"
            else:
                pip_exe = self.venv_path / "bin" / "pip3"
        
        return pip_exe
    
    def install_package(self):
        """Install Personal History package in virtual environment"""
        python_exe = self.get_venv_python()
        pip_exe = self.get_venv_pip()
        
        if not python_exe.exists():
            print(f"❌ Python executable not found at: {python_exe}")
            return False
        
        print(f"\nInstalling Personal History in virtual environment...")
        
        try:
            # Install the package in development mode
            cmd = [str(python_exe), "-m", "pip", "install", "-e", "."]
            print(f"Running: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            
            print("✓ Package installed successfully")
            
            # Install development dependencies if requested
            if self.install_dev:
                print("\nInstalling development dependencies...")
                cmd = [str(python_exe), "-m", "pip", "install", "-r", "requirements-dev.txt"]
                subprocess.run(cmd, cwd=self.project_root, check=True)
                print("✓ Development dependencies installed")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation failed:")
            print(f"  stdout: {e.stdout}")
            print(f"  stderr: {e.stderr}")
            return False
        except Exception as e:
            print(f"❌ Installation error: {e}")
            return False
    
    def verify_installation(self):
        """Verify the installation"""
        python_exe = self.get_venv_python()
        
        print(f"\nVerifying installation...")
        
        try:
            # Run verification script
            verify_script = self.project_root / "verify_installation.py"
            if verify_script.exists():
                cmd = [str(python_exe), str(verify_script)]
                result = subprocess.run(
                    cmd,
                    cwd=self.project_root,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print("✓ Installation verified successfully")
                    return True
                else:
                    print("⚠️  Verification had issues:")
                    print(result.stdout)
                    if result.stderr:
                        print(f"Stderr: {result.stderr}")
                    return False
            else:
                print("⚠️  Verification script not found")
                return True  # Not critical
                
        except Exception as e:
            print(f"⚠️  Verification error: {e}")
            return True  # Not critical
    
    def create_activation_script(self):
        """Create activation helper scripts"""
        print(f"\nCreating activation helpers...")
        
        # Create activate.sh for Unix
        if not self.is_windows:
            activate_sh = self.project_root / "activate.sh"
            with open(activate_sh, 'w') as f:
                f.write(f'''#!/bin/bash
# Activate Personal History virtual environment
source "{self.venv_path}/bin/activate"
echo "Virtual environment activated. Run 'ph --help' to get started."
''')
            os.chmod(activate_sh, 0o755)
            print(f"✓ Created: {activate_sh}")
        
        # Create activate.bat for Windows
        activate_bat = self.project_root / "activate.bat"
        with open(activate_bat, 'w') as f:
            f.write(f'''@echo off
REM Activate Personal History virtual environment
call "{self.venv_path}\\Scripts\\activate.bat"
echo Virtual environment activated. Run 'ph --help' to get started.
''')
        print(f"✓ Created: {activate_bat}")
        
        # Create usage instructions
        readme = self.project_root / "INSTALLATION_USAGE.md"
        with open(readme, 'w') as f:
            f.write(f'''# Personal History - Installation Complete

## Virtual Environment Created
Location: `{self.venv_path}`

## How to Use

### On Linux/macOS:
```bash
# Activate virtual environment
source activate.sh

# Or manually:
source {self.venv_path}/bin/activate

# Use Personal History
ph --help
```

### On Windows:
```batch
# Activate virtual environment
activate.bat

# Or manually:
{self.venv_path}\\Scripts\\activate.bat

# Use Personal History
ph --help
```

## Deactivate
When done, run:
```bash
deactivate
```

## Package Information
- Installed in development mode (`-e .`)
- All dependencies installed (including cryptography)
- `ph` command available in virtual environment

## Development
To install development dependencies:
```bash
pip install -r requirements-dev.txt
```
''')
        print(f"✓ Created: {readme}")
    
    def print_summary(self):
        """Print installation summary"""
        python_exe = self.get_venv_python()
        
        print(f"\n{'='*60}")
        print("INSTALLATION COMPLETE")
        print(f"{'='*60}")
        print(f"Virtual environment: {self.venv_path}")
        print(f"Python: {python_exe}")
        print(f"\nNext steps:")
        print(f"1. Activate the virtual environment:")
        
        if self.is_windows:
            print(f"   activate.bat")
            print(f"   OR")
            print(f'   "{self.venv_path}\\Scripts\\activate.bat"')
        else:
            print(f"   source activate.sh")
            print(f"   OR")
            print(f'   source "{self.venv_path}/bin/activate"')
        
        print(f"\n2. Test the installation:")
        print(f"   ph --help")
        print(f"\n3. Run verification:")
        print(f'   "{python_exe}" verify_installation.py')
        print(f"\n{'='*60}")
    
    def run(self):
        """Run the complete installation process"""
        print(f"{'='*60}")
        print("Personal History Installer")
        print(f"{'='*60}")
        
        # Check Python version
        if not self.check_python_version():
            return False
        
        # Create virtual environment
        if not self.create_venv():
            return False
        
        # Install package
        if not self.install_package():
            return False
        
        # Verify installation
        self.verify_installation()
        
        # Create activation helpers
        self.create_activation_script()
        
        # Print summary
        self.print_summary()
        
        return True

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Install Personal History with virtual environment")
    parser.add_argument("--venv", default=".venv", help="Virtual environment name (default: .venv)")
    parser.add_argument("--dev", action="store_true", help="Install development dependencies")
    
    args = parser.parse_args()
    
    installer = PersonalHistoryInstaller(
        venv_name=args.venv,
        install_dev=args.dev
    )
    
    try:
        success = installer.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()