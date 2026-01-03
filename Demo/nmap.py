#!/usr/bin/env python3
"""
Nmap wrapper - passes all arguments directly to wsl nmap
"""
import subprocess
import sys

if __name__ == "__main__":
    # Get all arguments
    args = sys.argv[1:]
    
    if not args:
        print("Usage: python nmap.py <nmap_arguments>")
        print("Example: python nmap.py -sV afot.in")
        sys.exit(1)
    
    try:
        # Execute nmap via WSL Kali distribution
        result = subprocess.run(
            ["wsl", "-d", "kali-linux", "nmap"] + args,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute timeout
        )
        
        # Print output
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        
        sys.exit(result.returncode)
        
    except subprocess.TimeoutExpired:
        print("Error: Scan timeout (10 minutes exceeded)", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
