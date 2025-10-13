# Maya FBX Export Tool — Installation Automatique

Ce script installe automatiquement l'outil d'export FBX dans Maya, crée un bouton sur le shelf, ajoute le chemin nécessaire, et lance l'interface utilisateur, en un seul clic.

---

## Contenu

- `installer_fbx_tool.py` — Script d'installation automatique  
- `maya_fbx_export_tool.py` — Script principal de l'outil

---

## Installation

1. Placez les deux fichiers (`installer_fbx_tool.py` et `maya_fbx_export_tool.py`) dans le même dossier.

2. Ouvrez Maya.

3. Glissez-déposez `installer_fbx_tool.py` dans la fenêtre Maya.

4. Le script copiera automatiquement le fichier principal dans le bon dossier scripts Maya pour votre version, créera le bouton shelf, et lancera l'outil automatiquement.

---

## Utilisation

- Utilisez le bouton **FBX Export** dans le shelf Maya pour lancer l’outil.

- Pour mettre à jour, refaites la même installation.

- Pour désinstaller, supprimez manuellement le fichier `maya_fbx_export_tool.py` du dossier scripts Maya et le bouton shelf dans Maya.

---

## Notes techniques

- Le dossier scripts Maya est automatiquement détecté selon votre version Maya.

- L'installation est silencieuse et nécessite uniquement un glisser-déposer du script `installer_fbx_tool.py`.

- Aucun chemin manuel ou configuration n’est nécessaire.

---
