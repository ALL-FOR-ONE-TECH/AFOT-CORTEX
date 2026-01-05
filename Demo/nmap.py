#!/usr/bin/env python3
"""
Self-contained nmap wrapper with built-in environment checks.
Works across Windows (WSL), Linux, and macOS.
"""
import os
import sys
import subprocess
import platform
import shutil

def check_environment():
    """Check if nmap is available in the environment"""
    
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ ERROR: Python 3.6+ required")
        print(f"   Current: Python {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)
    
    system = platform.system()
    
    # Try to find nmap
    nmap_cmd = None
    
    if system == "Windows":
        # On Windows, try WSL first
        if shutil.which("wsl"):
            # Check if nmap exists in WSL
            try:
                result = subprocess.run(
                    ["wsl", "which", "nmap"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    nmap_cmd = ["wsl", "nmap"]
            except:
                pass
        
        # Try native Windows nmap
        if not nmap_cmd and shutil.which("nmap"):
            nmap_cmd = ["nmap"]
    
    else:
        # Linux/Mac - direct nmap
        if shutil.which("nmap"):
            nmap_cmd = ["nmap"]
    
    if not nmap_cmd:
        print("❌ ERROR: nmap not found in environment")
        print("")
        print("INSTALLATION REQUIRED:")
        if system == "Windows":
            print("  Option 1 (WSL): wsl -d kali-linux sudo apt install nmap")
            print("  Option 2 (Native): Download from https://nmap.org/download.html")
        elif system == "Linux":
            print("  Ubuntu/Debian: sudo apt install nmap")
            print("  Fedora/RHEL: sudo dnf install nmap")
            print("  Arch: sudo pacman -S nmap")
        elif system == "Darwin":
            print("  Homebrew: brew install nmap")
            print("  MacPorts: sudo port install nmap")
        print("")
        sys.exit(1)
    
    return nmap_cmd

def run_nmap(args):
    """
    Execute nmap with given arguments
    
    Args:
        args (str): Nmap arguments (e.g., '-sV -p 80,443 192.168.1.1')
        
    Returns:
        dict: Result with success status and output
    """
    try:
        # Get nmap command
        nmap_cmd = check_environment()
        
        # Parse arguments
        arg_list = args.split() if isinstance(args, str) else args
        
        # Build full command
        full_cmd = nmap_cmd + arg_list
        
        # Execute nmap
        result = subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        # Combine stdout and stderr
        output = result.stdout
        if result.stderr:
            output += "\n" + result.stderr
        
        return {
            "success": result.returncode == 0,
            "output": output,
            "return_code": result.returncode
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "❌ ERROR: Nmap scan timed out (10 min limit)",
            "return_code": -1
        }
    except Exception as e:
        return {
            "success": False,
            "output": f"❌ ERROR: {str(e)}",
            "return_code": -1
        }

def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("❌ ERROR: Missing nmap arguments")
        print("Usage: python nmap.py '<nmap args>'")
        print("Example: python nmap.py '-sV scanme.nmap.org'")
        sys.exit(1)
    
    # Join all arguments (in case spaces aren't properly quoted)
    args = ' '.join(sys.argv[1:])
    
    # Run nmap
    result = run_nmap(args)
    
    # Print output
    print(result["output"])
    
    # Exit with nmap's return code
    sys.exit(result["return_code"])

if __name__ == "__main__":
    main()
