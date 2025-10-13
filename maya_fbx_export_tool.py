import maya.cmds as cmds
import os

# Import PySide6 modules adaptés à Maya 2026
try:
    from PySide6.QtWidgets import *
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from shiboken6 import wrapInstance
except ImportError:
    cmds.error("PySide6 ou shiboken6 non disponible dans Maya 2026.")

import maya.OpenMayaUI as omui

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QMainWindow)

class FBXExportTool(QDialog):
    def __init__(self, parent=None):
        super(FBXExportTool, self).__init__(parent)
        self.setWindowTitle("Maya FBX Export Tool")
        self.setMinimumSize(400, 300)
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)

        self.max_poly_count = 10000
        self.export_folder = ""
        self.filename = "export"

        # Nouveau: contrôle de la vérification des lightmaps (2 sets UV)
        self.check_lightmaps_enabled = True

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Outil d'Export FBX avec Vérifications")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)

        params_group = QGroupBox("Paramètres d'Export")
        params_layout = QVBoxLayout(params_group)

        poly_layout = QHBoxLayout()
        poly_layout.addWidget(QLabel("Polygones max:"))
        self.poly_spinbox = QSpinBox()
        self.poly_spinbox.setRange(1000, 100000)
        self.poly_spinbox.setValue(self.max_poly_count)
        self.poly_spinbox.setSuffix(" polygones")
        poly_layout.addWidget(self.poly_spinbox)
        poly_layout.addStretch()
        params_layout.addLayout(poly_layout)

        # Nouveau: case à cocher pour la vérification des lightmaps
        self.lightmap_checkbox = QCheckBox("Vérifier lightmaps (2 sets UV)")
        self.lightmap_checkbox.setChecked(True)
        self.lightmap_checkbox.toggled.connect(self.on_lightmap_toggle)
        params_layout.addWidget(self.lightmap_checkbox)

        folder_layout = QHBoxLayout()
        folder_layout.addWidget(QLabel("Dossier d'export:"))
        self.folder_label = QLabel("Aucun dossier sélectionné")
        self.folder_label.setStyleSheet("background-color: #f0f0f0; padding: 5px; border: 1px solid #ccc;")
        folder_layout.addWidget(self.folder_label)
        self.browse_btn = QPushButton("Parcourir...")
        self.browse_btn.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.browse_btn)
        params_layout.addLayout(folder_layout)

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Nom du fichier:"))
        self.filename_edit = QLineEdit(self.filename)
        name_layout.addWidget(self.filename_edit)
        name_layout.addWidget(QLabel(".fbx"))
        params_layout.addLayout(name_layout)

        layout.addWidget(params_group)

        info_group = QGroupBox("Informations Objet Sélectionné")
        info_layout = QVBoxLayout(info_group)
        self.info_label = QLabel("Sélectionnez un mesh pour voir les informations")
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("background-color: #f9f9f9; padding: 10px; border: 1px solid #ddd;")
        info_layout.addWidget(self.info_label)
        self.check_btn = QPushButton("Vérifier l'Objet Sélectionné")
        self.check_btn.clicked.connect(self.check_selected_mesh)
        info_layout.addWidget(self.check_btn)
        layout.addWidget(info_group)

        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(100)
        self.results_text.setReadOnly(True)
        layout.addWidget(QLabel("Messages:"))
        layout.addWidget(self.results_text)

        buttons_layout = QHBoxLayout()
        self.export_btn = QPushButton("Vérifier et Exporter")
        self.export_btn.clicked.connect(self.verify_and_export)
        self.export_btn.setEnabled(False)

        self.validate_btn = QPushButton("Juste Vérifier")
        self.validate_btn.clicked.connect(self.validate_only)

        cancel_btn = QPushButton("Fermer")
        cancel_btn.clicked.connect(self.close)

        buttons_layout.addWidget(self.export_btn)
        buttons_layout.addWidget(self.validate_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)

    def on_lightmap_toggle(self, checked):
        self.check_lightmaps_enabled = checked
        # Optionnel: re-vérifier l'objet automatiquement si souhaité
        # self.check_selected_mesh()

    def browse_folder(self):
        try:
            folder = cmds.fileDialog2(fileMode=3, caption="Sélectionner le dossier d'export")
            if folder:
                self.export_folder = folder[0]
                self.folder_label.setText(self.export_folder)
                self.export_btn.setEnabled(True)
                self.log_message(f"Dossier sélectionné: {self.export_folder}")
        except Exception as e:
            self.log_message(f"Erreur lors de la sélection du dossier: {e}")

    def log_message(self, message):
        self.results_text.append(message)

    def validate_only(self):
        selection = cmds.ls(selection=True, long=True)
        if not selection:
            self.log_message("❌ Aucun objet sélectionné")
            return

        mesh = selection[0]
        shapes = cmds.listRelatives(mesh, shapes=True)
        if not shapes or cmds.nodeType(shapes[0]) != "mesh":
            self.log_message("❌ L'objet sélectionné n'est pas un mesh")
            return

        self.results_text.clear()
        self.log_message("🔍 Vérification sur l'objet sélectionné…")

        if self.check_mesh(mesh):
            self.log_message("✅ Toutes les vérifications sont passées 👍")
        else:
            self.log_message("❌ Une ou plusieurs vérifications ont échoué")

    def check_selected_mesh(self):
        selection = cmds.ls(selection=True, long=True)
        if not selection:
            self.info_label.setText("Aucun objet sélectionné")
            return

        mesh = selection[0]
        shapes = cmds.listRelatives(mesh, shapes=True)

        if not shapes or cmds.nodeType(shapes[0]) != "mesh":
            self.info_label.setText("L'objet sélectionné n'est pas un mesh")
            return

        poly_count = cmds.polyEvaluate(mesh, face=True)
        vertex_count = cmds.polyEvaluate(mesh, vertex=True)
        uv_sets = cmds.polyUVSet(mesh, query=True, allUVSets=True)
        uv_count = len(uv_sets) if uv_sets else 0

        required_uv_sets = 2 if self.check_lightmaps_enabled else 1

        info_text = f"""
        Mesh: {mesh.split('|')[-1]}
        Polygones: {poly_count}
        Vertices: {vertex_count}
        Sets UV: {uv_count} (requis: {required_uv_sets})
        """

        warnings = []
        if poly_count > self.poly_spinbox.value():
            warnings.append(f"⚠️ Trop de polygones ({poly_count} > {self.poly_spinbox.value()})")
        if uv_count < required_uv_sets:
            if required_uv_sets == 2:
                warnings.append("⚠️ Pas assez de sets UV pour lightmaps (2 requis)")
            else:
                warnings.append("⚠️ Aucun set UV détecté (au moins 1 requis)")

        if warnings:
            info_text += "\n" + "\n".join(warnings)
        else:
            info_text += "\n✅ Toutes les vérifications OK"

        self.info_label.setText(info_text)

    def check_mesh(self, mesh):
        try:
            poly_count = cmds.polyEvaluate(mesh, face=True)
            max_polys = self.poly_spinbox.value()

            if poly_count > max_polys:
                self.log_message(f"❌ Trop de polygones ({poly_count}). Max autorisé: {max_polys}")
                return False
            else:
                self.log_message(f"✅ Nombre de polygones OK ({poly_count})")

            faces = cmds.polyListComponentConversion(mesh, toFace=True)
            uvs = cmds.polyListComponentConversion(faces, toUV=True)
            uvs = list(set(uvs))

            if uvs:
                uvs_coords = [cmds.polyEditUV(uv, query=True) for uv in uvs]
                u_values = [uv[0] for uv in uvs_coords]
                v_values = [uv[1] for uv in uvs_coords]

                if max(u_values) > 1 or max(v_values) > 1 or min(u_values) < 0 or min(v_values) < 0:
                    self.log_message("⚠️ Certains UVs dépassent la plage 0-1")
                else:
                    self.log_message("✅ UVs dans la plage 0-1")
            else:
                self.log_message("❌ Aucune UV trouvée")
                return False

            uv_sets = cmds.polyUVSet(mesh, query=True, allUVSets=True)
            uv_count = len(uv_sets) if uv_sets else 0
            required_uv_sets = 2 if self.check_lightmaps_enabled else 1

            if uv_count >= required_uv_sets:
                if required_uv_sets == 2:
                    self.log_message(f"✅ {uv_count} sets UV détectés (lightmaps OK)")
                else:
                    self.log_message(f"✅ {uv_count} set(s) UV détecté(s) (exigence minimale 1 OK)")
            else:
                if required_uv_sets == 2:
                    self.log_message("⚠️ Pas assez de sets UV pour lightmaps (au moins 2 attendus)")
                else:
                    self.log_message("⚠️ Pas de set UV détecté (au moins 1 attendu)")
                return False

            return True

        except Exception as e:
            self.log_message(f"❌ Erreur lors de la vérification: {e}")
            return False

    def verify_and_export(self):
        if not self.export_folder:
            self.log_message("❌ Veuillez sélectionner un dossier d'export")
            return

        filename = self.filename_edit.text().strip()
        if not filename:
            self.log_message("❌ Veuillez entrer un nom de fichier")
            return

        selection = cmds.ls(selection=True, long=True, dag=True, shapes=False)
        if not selection:
            self.log_message("❌ Aucun objet sélectionné")
            return

        mesh = selection[0]
        shapes = cmds.listRelatives(mesh, shapes=True)

        if not shapes or cmds.nodeType(shapes[0]) != "mesh":
            self.log_message("❌ L'objet sélectionné n'est pas un mesh")
            return

        self.results_text.clear()
        self.log_message("🔍 Début des vérifications...")

        if not self.check_mesh(mesh):
            self.log_message("❌ Vérifications échouées, export annulé")
            return

        export_path = os.path.join(self.export_folder, filename + ".fbx")

        try:
            self.log_message("📦 Export en cours...")
            cmds.FBXResetExport()
            cmds.select(mesh)
            cmds.file(export_path, force=True, options="v=0;", type="FBX export", exportSelected=True)
            self.log_message(f"✅ Export réussi vers: {export_path}")
            QMessageBox.information(self, "Export Réussi", f"Le fichier a été exporté avec succès:\n{export_path}")
        except Exception as e:
            self.log_message(f"❌ Erreur lors de l'export: {e}")
            QMessageBox.critical(self, "Erreur d'Export", f"Erreur lors de l'export:\n{e}")

def show_fbx_export_tool():
    global fbx_export_dialog
    try:
        fbx_export_dialog.close()
        fbx_export_dialog.deleteLater()
    except:
        pass

    parent = get_maya_main_window()
    fbx_export_dialog = FBXExportTool(parent)
    fbx_export_dialog.show()

fbx_export_dialog = None
