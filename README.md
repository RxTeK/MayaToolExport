# MYA FBX Export Tool

## Description
Un outil pour exporter rapidement et proprement des meshes en FBX depuis Maya 2026 avec vérification du nombre de polygones et des UVs.

## Fichiers
- **installer_fbx_tool.py** : script d'installation. Crée le bouton dans le shelf Maya.
- **maya_fbx_export_tool.py** : script principal de l'outil.
- **README.md** : ce fichier.

## Installation

1. Copier **installer_fbx_tool.py** scripts dans le dossier scripts Maya :
```
C:/Users/<VotreNom>/OneDrive/Documents/maya/2026/scripts/
```
ou
```
C:/Users/<VotreNom>/Documents/maya/2026/scripts/
```
2. Redémarrer Maya.
3. Dans Maya > Script Editor (Python) lancer :
```
import installer_fbx_tool
installer_fbx_tool.install_fbx_export_tool()
```
4. Aller chercher maya_fbx_export_tool.py

5. Fermer et relancer Maya.

6.  Dans Maya > Script Editor (Python) lancer :
```
from importlib import reload
import maya_fbx_export_tool
reload(maya_fbx_export_tool)
maya_fbx_export_tool.show_fbx_export_tool()
```
## Utilisation

- Cliquer sur le bouton **FBX Export** dans le shelf `Custom`.
- Sélectionner un mesh, choisir un dossier et un nom de fichier.
- choisir les bon settings à vérifier.
- Lancer les vérifications et exporter.

## Rechargement après modification du scripts

Sans redémarrer Maya :
```python
from importlib import reload
import maya_fbx_export_tool
reload(maya_fbx_export_tool)
maya_fbx_export_tool.show_fbx_export_tool()
```

## Remarques

- Sur Windows avec OneDrive, Maya pointe sur `OneDrive/Documents` pour `~/maya/2026/scripts`.
- Vérifier que les fichiers ont l'extension `.py` et pas de `.txt` caché.
