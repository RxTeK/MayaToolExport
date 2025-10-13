# Maya FBX Export Tool — Automatic Installation

This script automatically installs the FBX export tool in Maya, creates a button on the shelf, adds the necessary path, and launches the user interface, all in one click.

---

## Contents

- `installer_fbx_tool.py` — Automatic installation script  
- `maya_fbx_export_tool.py` — Main tool script

---

## Installation

1. Place both files (`installer_fbx_tool.py` and `maya_fbx_export_tool.py`) in the same folder.

2. Open Maya.

3. Drag and drop `installer_fbx_tool.py` into the Maya window.

4. The script will automatically copy the main file to the correct Maya scripts folder for your version, create the shelf button, and launch the tool automatically.

---

## Usage

- Use the **FBX Export** button in the Maya shelf to launch the tool.

- To update, repeat the same installation process.

- To uninstall, manually delete the `maya_fbx_export_tool.py` file from the Maya scripts folder and the shelf button in Maya.

---

## Technical Notes

- The Maya scripts folder is automatically detected according to your Maya version.

- The installation is silent and only requires dragging and dropping the `installer_fbx_tool.py` script.

- No manual path or configuration is necessary.

---
