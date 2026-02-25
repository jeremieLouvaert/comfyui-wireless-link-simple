# MANUAL INSTALLATION GUIDE

## What You're Installing

A simple wireless link system for ComfyUI with just 2 nodes:
- 📤 Wireless Send - Stores data to a named channel
- 📥 Wireless Get - Retrieves data from a named channel

---

## Installation Steps

### Step 1: Locate Your ComfyUI Installation

Find your ComfyUI folder. It should look like this:

```
ComfyUI/
├── models/
├── output/
├── custom_nodes/  ← You need this folder
├── main.py
└── ...
```

Common locations:
- Windows: `C:\Users\YourName\ComfyUI\` or `F:\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\`
- Mac: `/Users/YourName/ComfyUI/`
- Linux: `/home/yourname/ComfyUI/`

### Step 2: Navigate to custom_nodes

Open your file browser and go to:
```
ComfyUI/custom_nodes/
```

If this folder doesn't exist, create it.

### Step 3: Create the Plugin Folder

Inside `custom_nodes/`, create a new folder called:
```
comfyui_wireless_link_simple
```

Your structure should now look like:
```
ComfyUI/
└── custom_nodes/
    └── comfyui_wireless_link_simple/  ← New folder
```

### Step 4: Copy the Files

Copy these 3 files into the `comfyui_wireless_link_simple` folder:

1. **__init__.py**
2. **wireless_simple.py**
3. **README.md** (optional, for reference)

Final structure:
```
ComfyUI/
└── custom_nodes/
    └── comfyui_wireless_link_simple/
        ├── __init__.py
        ├── wireless_simple.py
        ├── README.md
        └── QUICKSTART.md (optional)
```

### Step 5: Verify File Contents

#### Check __init__.py:
Open `__init__.py` in a text editor. It should contain exactly this:

```python
from .wireless_simple import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
```

#### Check wireless_simple.py:
Open `wireless_simple.py` and verify it starts with:

```python
"""
Simple Wireless Link Node for ComfyUI
Minimal implementation - just store and retrieve
"""

# Global storage dictionary
WIRELESS_STORAGE = {}
...
```

If the files look different, you may have copied them incorrectly.

### Step 6: Restart ComfyUI

**IMPORTANT:** You must completely restart ComfyUI, not just refresh the browser.

#### If running from command line:
1. Press `Ctrl+C` in the terminal to stop ComfyUI
2. Run the start command again (e.g., `python main.py`)

#### If running as a standalone application:
1. Close the ComfyUI window completely
2. Reopen the ComfyUI application

#### If using a batch file:
1. Close the command window
2. Double-click the batch file again

### Step 7: Verify Installation

1. Open ComfyUI in your browser
2. Right-click anywhere on the canvas
3. Select "Add Node"
4. Look for a category called "wireless"
5. You should see:
   - 📤 Wireless Send
   - 📥 Wireless Get

If you see these nodes, installation was successful! 🎉

---

## Troubleshooting Installation

### Problem: Nodes don't appear in the menu

#### Check 1: File Location
Verify files are in the correct location:
```
ComfyUI/custom_nodes/comfyui_wireless_link_simple/__init__.py
ComfyUI/custom_nodes/comfyui_wireless_link_simple/wireless_simple.py
```

Use your file browser to navigate there and confirm the files exist.

#### Check 2: File Names
Make sure the files are named exactly:
- `__init__.py` (with double underscores)
- `wireless_simple.py` (not wireless_simple.txt or wireless_simple.py.txt)

On Windows, you may need to:
1. Open File Explorer
2. Click "View" → Check "File name extensions"
3. Verify files don't have hidden `.txt` extensions

#### Check 3: File Contents
Open `__init__.py` and verify it contains the import statement (see Step 5 above).

#### Check 4: Python Errors
When you start ComfyUI, check the console/terminal for error messages.

Look for lines like:
```
Error loading custom node comfyui_wireless_link_simple
```

If you see errors, there may be:
- Syntax errors in the Python files
- Incorrect file encoding
- Missing files

#### Check 5: Restart Method
Make sure you're doing a COMPLETE restart:
- ❌ Just refreshing the browser → Won't work
- ❌ Clicking "Reload" in ComfyUI → Won't work
- ✅ Closing and reopening the ComfyUI process → Will work

### Problem: Import errors in console

If you see:
```
ModuleNotFoundError: No module named 'wireless_simple'
```

This means `__init__.py` is incorrect or in the wrong location.

**Fix:**
1. Check that `__init__.py` is in the same folder as `wireless_simple.py`
2. Verify `__init__.py` contains the correct import statement
3. Make sure the folder is named `comfyui_wireless_link_simple` (or update the path)

### Problem: Nodes appear but don't work

If the nodes appear in the menu but give errors when used:
1. Check the console for Python error messages
2. Verify `wireless_simple.py` was copied completely (not truncated)
3. Try deleting and reinstalling the files

---

## Alternative Installation Methods

### Method 1: Download from Web

If you received these files as a ZIP:
1. Extract the ZIP file
2. Copy the extracted folder to `ComfyUI/custom_nodes/`
3. Restart ComfyUI

### Method 2: Git Clone (Advanced)

If this is hosted on GitHub:
```bash
cd ComfyUI/custom_nodes/
git clone [repository-url] comfyui_wireless_link_simple
```

Then restart ComfyUI.

### Method 3: ComfyUI Manager (If Available)

If you have ComfyUI Manager installed:
1. Open ComfyUI Manager
2. Search for "wireless link"
3. Click Install
4. Restart ComfyUI

---

## Uninstallation

To remove the nodes:

1. Close ComfyUI
2. Delete the folder:
   ```
   ComfyUI/custom_nodes/comfyui_wireless_link_simple/
   ```
3. Restart ComfyUI

The nodes will no longer appear in the menu.

---

## File Permissions (Linux/Mac)

If you're on Linux or Mac and having issues:

Make sure the files have the correct permissions:
```bash
chmod 644 ComfyUI/custom_nodes/comfyui_wireless_link_simple/*.py
```

---

## Next Steps

After successful installation:
1. Read `QUICKSTART.md` for a simple test workflow
2. Try the example in "First Test" section
3. Check the console for `[WirelessSend]` and `[WirelessGet]` messages
4. Read `README.md` for detailed usage instructions

---

## Getting Help

If you're still having trouble:

1. **Check the console** - Most errors appear there
2. **Verify file structure** - Use the directory tree above as reference
3. **Test with other custom nodes** - If they work, the issue is with these files
4. **Check ComfyUI version** - Very old versions may have compatibility issues

Console should show on startup:
- Windows: A command prompt window opens with ComfyUI
- Mac/Linux: The terminal you used to launch ComfyUI
- Portable: The console window that appears with the application

Look for error messages related to `wireless_simple` or `comfyui_wireless_link_simple`.

---

## Summary Checklist

Installation is complete when:
- [ ] Files are in `ComfyUI/custom_nodes/comfyui_wireless_link_simple/`
- [ ] `__init__.py` contains the correct import statement
- [ ] `wireless_simple.py` contains the node code
- [ ] ComfyUI has been completely restarted
- [ ] Nodes appear in the "wireless" category in the Add Node menu
- [ ] No error messages in console related to wireless nodes

If all checkboxes are true, you're ready to use the wireless link nodes!
