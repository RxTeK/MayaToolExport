# -*- coding: utf-8 -*-
import maya.cmds as cmds
import os
import shutil
import sys

def auto_install():
    maya_version = cmds.about(version=True)
    user_docs = os.path.expanduser('~/Documents')
    scripts_dir = os.path.join(user_docs, 'maya', maya_version, 'scripts')
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)
    this_folder = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(this_folder, "maya_fbx_export_tool.py")
    dest = os.path.join(scripts_dir, "maya_fbx_export_tool.py")
    shutil.copy2(source, dest)
    print(f"Fichier copié dans {dest}")
    if scripts_dir not in sys.path:
        sys.path.append(scripts_dir)
    shelf = "Custom"
    btn = "FBX Export"
    command = "import maya_fbx_export_tool; maya_fbx_export_tool.show_fbx_export_tool()"
    if not cmds.shelfLayout(shelf, exists=True):
        cmds.shelfLayout(shelf, parent="MainShelfForm")
    for b in cmds.shelfLayout(shelf, q=True, childArray=True) or []:
        if cmds.shelfButton(b, q=True, label=True) == btn:
            cmds.deleteUI(b)
    cmds.shelfButton(parent=shelf, label=btn, image="polyMesh.png", command=command,
                     annotation="Outil d'export FBX avec vérifications")
    print(f"Bouton shelf {btn} créé/mis à jour dans {shelf}")
    import maya_fbx_export_tool
    maya_fbx_export_tool.show_fbx_export_tool()

auto_install()
