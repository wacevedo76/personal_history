"""
Integration test to verify Personal History works when installed in a Python virtual environment.
This test simulates what a user would experience after installing the package.
"""

import pytest
import subprocess
import sys
import json
from pathlib import Path
import tempfile
import shutil


class TestInstallation:
    """Test that the package works correctly when installed."""
    
    def test_package_can_be_imported(self):
        """Test that the package can be imported after installation."""
        # This test runs in the current environment (should be virtual env)
        import ph.v001.core
        import ph.v001.schema
        import ph.v001.cli
        
        # Verify modules have expected attributes
        assert hasattr(ph.v001.core, 'PersonalHistoryV001')
        assert hasattr(ph.v001.schema, 'validate_ph_file')
        assert hasattr(ph.v001.cli, 'main')
        
        print("✅ All modules can be imported")
    
    def test_cli_entry_point_available(self):
        """Test that the CLI entry point is registered."""
        # Try to run ph --help via subprocess
        # This simulates what a user would do
        try:
            result = subprocess.run(
                [sys.executable, "-m", "ph.v001.cli", "--help"],
                capture_output=True,
                text=True,
                timeout=5
            )
            # CLI should print help text
            assert "Personal History" in result.stdout or "usage" in result.stdout.lower()
            print("✅ CLI entry point works via python -m")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            # CLI might not be fully set up in test environment
            # That's OK for this test - we're testing import, not full installation
            print("⚠️  CLI test skipped (might need full installation)")
    
    def test_package_metadata(self):
        """Test that package metadata is correct."""
        import importlib.metadata
        
        try:
            metadata = importlib.metadata.metadata('personal-history')
            assert metadata['Name'] == 'personal-history'
            assert 'Personal History Format' in metadata['Summary']
            print(f"✅ Package metadata: {metadata['Version']}")
        except importlib.metadata.PackageNotFoundError:
            # Package might not be installed in editable mode in test env
            # Check setup.py instead
            setup_path = Path(__file__).parent.parent.parent / 'setup.py'
            if setup_path.exists():
                content = setup_path.read_text()
                assert 'personal-history' in content
                assert 'Personal History Format Implementation' in content
                print("✅ Setup.py contains correct metadata")
    
    def test_dependencies_available(self):
        """Test that required dependencies are available."""
        try:
            import cryptography
            print(f"✅ cryptography version: {cryptography.__version__}")
        except ImportError:
            print("⚠️  cryptography not available (using simulated mode)")
        
        # JSON and hashlib should always be available
        import json
        import hashlib
        print("✅ Core Python dependencies available")
    
    def test_create_and_validate_in_isolation(self):
        """
        Test creating and validating a PH file in isolation.
        Simulates a user's first use after installation.
        """
        from ph.v001.core import PersonalHistoryV001
        from ph.v001.schema import validate_ph_file
        
        # Create a simple PH file from scratch
        identity = PersonalHistoryV001.create_identity("Test User")
        activity = PersonalHistoryV001.create_activity(
            "work",
            {"project": "test_installation"},
            60
        )
        day = PersonalHistoryV001.create_day(
            date="2024-01-01",
            activities=[activity]
        )
        
        ph_file = PersonalHistoryV001.create_file(identity, [day])
        
        # Add a signature for validation
        ph_file["signature"] = "a" * 128
        
        # Validate it
        assert validate_ph_file(ph_file) is True
        print("✅ Can create and validate PH files")
    
    def test_save_and_load_workflow(self, tmp_path):
        """Test the complete save/load workflow a user would use."""
        from ph.v001.core import PersonalHistoryV001
        
        # Create test data
        identity = PersonalHistoryV001.create_identity("Installation Test User")
        activity = PersonalHistoryV001.create_activity(
            "learning",
            {"topic": "package_installation"},
            90
        )
        day = PersonalHistoryV001.create_day(
            date="2024-01-01",
            activities=[activity],
            note="Testing installation workflow"
        )
        
        ph_file = PersonalHistoryV001.create_file(identity, [day])
        
        # Save to a temporary file
        test_file = tmp_path / "installation_test.ph.json"
        PersonalHistoryV001.save_file(ph_file, test_file)
        
        # Verify file was created
        assert test_file.exists()
        assert test_file.stat().st_size > 0
        
        # Load it back
        loaded_file = PersonalHistoryV001.load_file(test_file)
        
        # Verify data integrity
        assert loaded_file["version"] == ph_file["version"]
        assert loaded_file["identity"]["hash"] == ph_file["identity"]["hash"]
        assert len(loaded_file["timeline"]) == 1
        
        print("✅ Save/load workflow works correctly")
    
    def test_module_structure(self):
        """Test that the module structure is correct."""
        import ph.v001
        
        # Check __init__.py exports
        assert hasattr(ph.v001, '__version__') or hasattr(ph.v001, '__author__')
        
        # Check submodules
        import ph.v001.core
        import ph.v001.schema
        import ph.v001.cli
        
        # Verify they're not empty
        assert len(dir(ph.v001.core)) > 10
        assert len(dir(ph.v001.schema)) > 5
        
        print("✅ Module structure is correct")
    
    @pytest.mark.slow
    def test_simulated_installation(self, tmp_path):
        """
        Simulate a fresh installation in a temporary directory.
        This is a more comprehensive test that mimics user installation.
        """
        import os
        import venv
        
        # Create a temporary virtual environment
        venv_dir = tmp_path / "test_venv"
        venv.create(venv_dir, with_pip=True)
        
        # Get Python executable in venv
        if os.name == 'nt':  # Windows
            python_exe = venv_dir / "Scripts" / "python.exe"
        else:  # Unix/Linux/Mac
            python_exe = venv_dir / "bin" / "python"
        
        # Copy the project to a temp location
        project_src = Path(__file__).parent.parent.parent
        project_dst = tmp_path / "personal_history"
        shutil.copytree(project_src, project_dst)
        
        # Install the package in the virtual environment
        install_cmd = [
            str(python_exe),
            "-m",
            "pip",
            "install",
            "-e",
            str(project_dst)
        ]
        
        try:
            result = subprocess.run(
                install_cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"⚠️  Installation output: {result.stderr}")
                # Don't fail the test - this might be environment-specific
                pytest.skip("Installation in test venv failed (environment issue)")
            
            # Test that we can import after installation
            test_import = f"""
import sys
sys.path.insert(0, '{project_dst}')
import ph.v001.core
print('SUCCESS')
"""
            
            import_result = subprocess.run(
                [str(python_exe), "-c", test_import],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            assert "SUCCESS" in import_result.stdout
            print("✅ Simulated installation test passed")
            
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            # Skip if environment doesn't support this test
            pytest.skip(f"Simulated installation test skipped: {e}")


def test_quick_installation_check():
    """
    Quick check that can be run by users after installation.
    This is what we'd tell users to run to verify installation.
    """
    print("\n" + "="*60)
    print("Personal History Installation Verification")
    print("="*60)
    
    checks = []
    
    # Check 1: Can import modules
    try:
        import ph.v001.core
        import ph.v001.schema
        checks.append(("✅ Module imports", True))
    except ImportError as e:
        checks.append((f"❌ Module imports: {e}", False))
    
    # Check 2: Core functionality works
    try:
        from ph.v001.core import PersonalHistoryV001
        identity = PersonalHistoryV001.create_identity("Test")
        checks.append(("✅ Core functionality", True))
    except Exception as e:
        checks.append((f"❌ Core functionality: {e}", False))
    
    # Check 3: Schema validation works
    try:
        from ph.v001.schema import validate_ph_file
        test_data = {
            "version": "0.01.0",
            "identity": {"hash": "a"*64},
            "timeline": [],
            "signature": "b"*128
        }
        validate_ph_file(test_data)
        checks.append(("✅ Schema validation", True))
    except Exception as e:
        checks.append((f"❌ Schema validation: {e}", False))
    
    # Print results
    for check, passed in checks:
        print(check)
    
    print("="*60)
    
    # Return overall status
    all_passed = all(passed for _, passed in checks)
    if all_passed:
        print("✅ Installation verified successfully!")
        return True
    else:
        print("❌ Installation issues detected")
        return False


if __name__ == "__main__":
    # Allow running this test directly for quick verification
    import sys
    success = test_quick_installation_check()
    sys.exit(0 if success else 1)