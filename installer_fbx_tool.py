# -*- coding: utf-8 -*-
"""
Installation automatique du Maya FBX Export Tool
Placez ce fichier avec maya-fbx-export-tool.py dans le même dossier
Puis exécutez ce script dans Maya pour installer l'outil
"""

import maya.cmds as cmds
import os
import shutil
import sys

def install_fbx_export_tool():
    """Installe automatiquement l'outil FBX Export dans Maya"""
    try:
        # Chemin vers le dossier scripts de Maya
        maya_version = cmds.about(version=True)
        user_docs = os.path.expanduser("~/Documents")
        maya_scripts_dir = os.path.join(user_docs, "maya", maya_version, "scripts")
        
        # Créer le dossier scripts s'il n'existe pas
        if not os.path.exists(maya_scripts_dir):
            os.makedirs(maya_scripts_dir)
        
        # Chemin du fichier principal
        source_file = cmds.fileDialog2(fileMode=1, caption="Sélectionnez maya-fbx-export-tool.py")[0]

        if not os.path.exists(source_file):
            print("❌ Fichier 'maya-fbx-export-tool.py' non trouvé dans le même dossier")
            return False
        
        # Copier le fichier vers le dossier scripts de Maya
        destination = os.path.join(maya_scripts_dir, "maya_fbx_export_tool.py")
        shutil.copy2(source_file, destination)
        
        print(f"✅ Fichier copié vers: {destination}")
        
        # Créer le bouton sur le shelf
        shelf_name = "Custom"
        
        # Créer le shelf s'il n'existe pas
        if not cmds.shelfLayout(shelf_name, exists=True):
            cmds.shelfLayout(shelf_name, parent="MainShelfForm")
        
        # Code à exécuter quand on clique sur le bouton
        command = '''
import maya_fbx_export_tool
reload(maya_fbx_export_tool)
maya_fbx_export_tool.show_fbx_export_tool()
'''
        
        # Créer le bouton
        cmds.shelfButton(
            parent=shelf_name,
            label="FBX Export",
            image="polyMesh.png",
            command=command,
            annotation="Outil d'export FBX avec vérifications automatiques"
        )
        
        print("✅ Bouton 'FBX Export' ajouté au shelf Custom")
        print("📁 Installation terminée ! Vous pouvez maintenant utiliser le bouton sur le shelf.")
        
        # Afficher une boîte de dialogue de confirmation
        cmds.confirmDialog(
            title="Installation Réussie",
            message="L'outil FBX Export a été installé avec succès!\n\nVous pouvez maintenant l'utiliser via le bouton 'FBX Export' sur le shelf Custom.",
            button=["OK"]
        )
        
        return True
        
    except Exception as e:
        error_msg = f"❌ Erreur lors de l'installation: {e}"
        print(error_msg)
        cmds.confirmDialog(
            title="Erreur d'Installation",
            message=error_msg,
            button=["OK"],
            icon="critical"
        )
        return False

def uninstall_fbx_export_tool():
    """Désinstalle l'outil FBX Export"""
    try:
        # Supprimer le fichier du dossier scripts
        maya_version = cmds.about(version=True)
        user_docs = os.path.expanduser("~/Documents")
        maya_scripts_dir = os.path.join(user_docs, "maya", maya_version, "scripts")
        script_file = os.path.join(maya_scripts_dir, "maya_fbx_export_tool.py")
        
        if os.path.exists(script_file):
            os.remove(script_file)
            print(f"✅ Fichier supprimé: {script_file}")
        
        # Note: Les boutons de shelf devront être supprimés manuellement
        print("📝 Note: Supprimez manuellement le bouton 'FBX Export' du shelf si désiré.")
        
        cmds.confirmDialog(
            title="Désinstallation Terminée",
            message="L'outil FBX Export a été désinstallé.\n\nVous pouvez supprimer manuellement le bouton du shelf si désiré.",
            button=["OK"]
        )
        
    except Exception as e:
        error_msg = f"❌ Erreur lors de la désinstallation: {e}"
        print(error_msg)
        cmds.confirmDialog(
            title="Erreur de Désinstallation",
            message=error_msg,
            button=["OK"],
            icon="critical"
        )

# Interface simple pour installer/désinstaller
def show_installer():
    """Affiche l'interface d'installation"""
    result = cmds.confirmDialog(
        title="Maya FBX Export Tool - Installation",
        message="Que voulez-vous faire ?",
        button=["Installer", "Désinstaller", "Annuler"],
        defaultButton="Installer",
        cancelButton="Annuler",
        dismissString="Annuler"
    )
    
    if result == "Installer":
        install_fbx_export_tool()
    elif result == "Désinstaller":
        uninstall_fbx_export_tool()

# Exécuter l'installateur si le script est lancé directement
if __name__ == "__main__":
    show_installer()