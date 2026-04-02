#!/bin/bash
# Personal History Installation Script
# Creates virtual environment and installs package automatically

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
VENV_NAME=".venv"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="$PROJECT_ROOT/$VENV_NAME"

# Functions
print_header() {
    echo -e "${BLUE}=================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}=================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}➤ $1${NC}"
}

# Check Python version
check_python_version() {
    print_header "Checking Python Version"
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 not found. Please install Python 3.8+"
        return 1
    fi
    
    PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')")
    PYTHON_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
    PYTHON_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")
    
    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
        print_error "Python 3.8+ required, found $PYTHON_VERSION"
        return 1
    fi
    
    print_success "Python $PYTHON_VERSION detected"
    return 0
}

# Create virtual environment
create_venv() {
    print_header "Creating Virtual Environment"
    
    if [ -d "$VENV_PATH" ]; then
        print_info "Virtual environment already exists at $VENV_PATH"
        read -p "Recreate? [y/N]: " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Removing existing virtual environment..."
            rm -rf "$VENV_PATH"
        else
            print_info "Using existing virtual environment"
            return 0
        fi
    fi
    
    print_info "Creating virtual environment at: $VENV_PATH"
    
    if python3 -m venv "$VENV_PATH" --prompt="personal-history"; then
        print_success "Virtual environment created"
        return 0
    else
        print_error "Failed to create virtual environment"
        return 1
    fi
}

# Install package
install_package() {
    print_header "Installing Personal History"
    
    VENV_PYTHON="$VENV_PATH/bin/python"
    VENV_PIP="$VENV_PATH/bin/pip"
    
    if [ ! -f "$VENV_PYTHON" ]; then
        print_error "Python not found in virtual environment"
        return 1
    fi
    
    # Upgrade pip first
    print_info "Upgrading pip..."
    if "$VENV_PIP" install --upgrade pip; then
        print_success "pip upgraded"
    else
        print_error "Failed to upgrade pip"
        return 1
    fi
    
    # Install package in development mode
    print_info "Installing Personal History package..."
    if "$VENV_PIP" install -e .; then
        print_success "Package installed successfully"
    else
        print_error "Package installation failed"
        return 1
    fi
    
    # Check if cryptography was installed
    print_info "Checking dependencies..."
    if "$VENV_PIP" show cryptography &> /dev/null; then
        CRYPTO_VERSION=$("$VENV_PIP" show cryptography | grep Version | cut -d: -f2 | xargs)
        print_success "cryptography $CRYPTO_VERSION installed"
    else
        print_error "cryptography not installed - something went wrong"
        return 1
    fi
    
    return 0
}

# Create activation script
create_activation_script() {
    print_header "Creating Activation Scripts"
    
    # Create activate.sh
    cat > "$PROJECT_ROOT/activate.sh" << EOF
#!/bin/bash
# Activate Personal History virtual environment
source "$VENV_PATH/bin/activate"
echo "Virtual environment activated. Run 'ph --help' to get started."
EOF
    
    chmod +x "$PROJECT_ROOT/activate.sh"
    print_success "Created: activate.sh"
    
    # Create usage instructions
    cat > "$PROJECT_ROOT/INSTALLATION_USAGE.md" << EOF
# Personal History - Installation Complete

## Virtual Environment Created
Location: \`$VENV_PATH\`

## How to Use

### Activate virtual environment:
\`\`\`bash
source activate.sh

# Or manually:
source $VENV_PATH/bin/activate
\`\`\`

### Use Personal History:
\`\`\`bash
ph --help
\`\`\`

### Deactivate:
\`\`\`bash
deactivate
\`\`\`

## Package Information
- Installed in development mode (\`-e .\`)
- All dependencies installed (including cryptography)
- \`ph\` command available in virtual environment

## Development
To install development dependencies:
\`\`\`bash
pip install -r requirements-dev.txt
\`\`\`
EOF
    
    print_success "Created: INSTALLATION_USAGE.md"
}

# Verify installation
verify_installation() {
    print_header "Verifying Installation"
    
    VENV_PYTHON="$VENV_PATH/bin/python"
    
    if [ -f "$PROJECT_ROOT/verify_installation.py" ]; then
        print_info "Running verification script..."
        if "$VENV_PYTHON" "$PROJECT_ROOT/verify_installation.py"; then
            print_success "Installation verified"
        else
            print_error "Verification failed"
            return 1
        fi
    else
        print_info "Verification script not found, running basic test..."
        
        # Basic test: try to import the package
        if "$VENV_PYTHON" -c "import personal_history; print('Import successful')"; then
            print_success "Basic import test passed"
        else
            print_error "Basic import test failed"
            return 1
        fi
    fi
    
    return 0
}

# Print summary
print_summary() {
    print_header "INSTALLATION COMPLETE"
    
    echo -e "${GREEN}Virtual environment:${NC} $VENV_PATH"
    echo -e "${GREEN}Python:${NC} $VENV_PATH/bin/python"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Activate the virtual environment:"
    echo "   source activate.sh"
    echo ""
    echo "2. Test the installation:"
    echo "   ph --help"
    echo ""
    echo "3. Run verification:"
    echo "   $VENV_PATH/bin/python verify_installation.py"
    echo ""
    echo -e "${BLUE}=================================================${NC}"
}

# Main installation process
main() {
    print_header "Personal History Installer"
    
    # Check Python version
    if ! check_python_version; then
        exit 1
    fi
    
    # Create virtual environment
    if ! create_venv; then
        exit 1
    fi
    
    # Install package
    if ! install_package; then
        exit 1
    fi
    
    # Verify installation
    if ! verify_installation; then
        print_error "Installation verification failed"
        exit 1
    fi
    
    # Create activation script
    create_activation_script
    
    # Print summary
    print_summary
    
    print_success "Installation completed successfully!"
}

# Run main function
main "$@"