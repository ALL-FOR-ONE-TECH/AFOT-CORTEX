#!/usr/bin/env python3
"""
Self-contained folder creator with built-in environment checks.
No external dependencies needed.
"""
import os
import sys
from pathlib import Path

def check_environment():
    """Verify environment is ready"""
    # Check Python version
    if sys.version_info < (3, 6):
        print("❌ ERROR: Python 3.6+ required")
        print(f"   Current: Python {sys.version_info.major}.{sys.version_info.minor}")
        print("   Install: https://www.python.org/downloads/")
        sys.exit(1)
    
    # Check we can write to temp (basic permission test)
    try:
        test_dir = Path.home() / ".cortex_test"
        test_dir.mkdir(exist_ok=True)
        test_dir.rmdir()
    except Exception as e:
        print(f"❌ ERROR: Cannot write to home directory: {e}")
        sys.exit(1)
    
    return True

def create_folder(folder_path):
    """
    Create a folder at the specified path
    
    Args:
        folder_path (str): Path where folder should be created
        
    Returns:
        dict: Result with success status, path, and message
    """
    try:
        # Convert to Path object for cross-platform compatibility
        path = Path(folder_path).expanduser().resolve()
        
        # Create the folder (including parent directories)
        path.mkdir(parents=True, exist_ok=True)
        
        # Verify it was created
        if not path.exists():
            return {
                "success": False,
                "path": str(path),
                "message": f"Failed to create folder: {path}"
            }
        
        return {
            "success": True,
            "path": str(path),
            "message": f"✅ Folder created successfully: {path}"
        }
        
    except PermissionError:
        return {
            "success": False,
            "path": folder_path,
            "message": f"❌ Permission denied: Cannot create folder at {folder_path}"
        }
    except OSError as e:
        return {
            "success": False,
            "path": folder_path,
            "message": f"❌ OS Error: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "path": folder_path,
            "message": f"❌ Unexpected error: {str(e)}"
        }

def main():
    """CLI interface"""
    # Check environment first
    check_environment()
    
    if len(sys.argv) < 2:
        print("❌ ERROR: Missing folder path argument")
        print("Usage: python folder_creator.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    result = create_folder(folder_path)
    
    # Print result
    print(result["message"])
    
    # Exit with appropriate code
    sys.exit(0 if result["success"] else 1)

if __name__ == "__main__":
    main()
