# MYA FBX Export Tool

## Description
A tool for quickly and cleanly exporting meshes to FBX from Maya 2026 with polygon count and UV verification.

## Files
- **installer_fbx_tool.py**: installation script. Creates the button in the Maya shelf.
- **maya_fbx_export_tool.py**: main tool script.
- **README.md**: this file.

## Installation

1. Copy **installer_fbx_tool.py** script to the Maya scripts folder:
```
C:/Users/<YourName>/OneDrive/Documents/maya/2026/scripts/
```
or
```
C:/Users/<YourName>/Documents/maya/2026/scripts/
```
2. Restart Maya.
3. In Maya > Script Editor (Python) run:
```
import installer_fbx_tool
installer_fbx_tool.install_fbx_export_tool()
```
4. Go find maya_fbx_export_tool.py

5. Close and restart Maya.

6. In Maya > Script Editor (Python) run:
```
from importlib import reload
import maya_fbx_export_tool
reload(maya_fbx_export_tool)
maya_fbx_export_tool.show_fbx_export_tool()
```
## Usage

- Click the **FBX Export** button in the `Custom` shelf.
- Select a mesh, choose a folder and file name.
- Choose the right settings to verify.
- Run verifications and export.

## Reloading after script modification

Without restarting Maya:
```python
from importlib import reload
import maya_fbx_export_tool
reload(maya_fbx_export_tool)
maya_fbx_export_tool.show_fbx_export_tool()
```

## Notes

- On Windows with OneDrive, Maya points to `OneDrive/Documents` for `~/maya/2026/scripts`.
- Verify that files have the `.py` extension and not a hidden `.txt`.