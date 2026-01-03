#!/usr/bin/env python3
"""
Folder Creator Tool for CORTEX
Creates folders on the file system with proper error handling
"""
import os
import sys
import json
from pathlib import Path

def create_folder(folder_path):
    """
    Create a folder at the specified path
    
    Args:
        folder_path (str): Path where folder should be created
        
    Returns:
        dict: Result with success status, path, and message
    """
    try:
        # Convert to Path object for better handling
        path = Path(folder_path)
        
        # Create the folder (including parent directories if needed)
        path.mkdir(parents=True, exist_ok=True)
        
        return {
            "success": True,
            "path": str(path.absolute()),
            "message": f"Folder created successfully: {path.absolute()}"
        }
        
    except PermissionError:
        return {
            "success": False,
            "path": folder_path,
            "message": f"Permission denied: Cannot create folder at {folder_path}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "path": folder_path,
            "message": f"Error creating folder: {str(e)}"
        }

def main():
    """
    CLI interface for folder creator
    """
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "message": "Usage: python folder_creator.py <folder_path>"
        }))
        sys.exit(1)
    
    folder_path = sys.argv[1]
    result = create_folder(folder_path)
    
    # Print result as JSON
    print(json.dumps(result, indent=2))
    
    # Exit with appropriate code
    sys.exit(0 if result["success"] else 1)

if __name__ == "__main__":
    main()
