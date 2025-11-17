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
        self.setWindowTitle("Maya FBX Export Tool Advanced")
        self.setMinimumSize(700, 900)
        self.setWindowFlags(Qt.Dialog | Qt.WindowStaysOnTopHint)
        
        self.max_poly_count = 10000
        self.export_folder = ""
        self.filename = "export"
        
        # Contrôles des vérifications
        self.checks_enabled = {
            "poly_count": True,
            "uv_count": True,
            "uv_range": True,
            "lightmaps": True
        }
        
        # Résultats des dernières vérifications
        self.last_check_results = {}
        
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # ===== TITRE =====
        title = QLabel("Outil d'Export FBX Avancé avec Vérifications Configurables")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px;")
        main_layout.addWidget(title)
        
        # ===== GROUPE PARAMÈTRES D'EXPORT =====
        params_group = QGroupBox("Paramètres d'Export")
        params_layout = QVBoxLayout(params_group)
        
        # Polygones max
        poly_layout = QHBoxLayout()
        poly_layout.addWidget(QLabel("Polygones max:"))
        self.poly_spinbox = QSpinBox()
        self.poly_spinbox.setRange(1000, 100000)
        self.poly_spinbox.setValue(self.max_poly_count)
        self.poly_spinbox.setSuffix(" polygones")
        poly_layout.addWidget(self.poly_spinbox)
        poly_layout.addStretch()
        params_layout.addLayout(poly_layout)
        
        # Dossier d'export
        folder_layout = QHBoxLayout()
        folder_layout.addWidget(QLabel("Dossier d'export:"))
        self.folder_label = QLabel("Aucun dossier sélectionné")
        self.folder_label.setStyleSheet("background-color: #f0f0f0; padding: 5px; border: 1px solid #ccc;")
        folder_layout.addWidget(self.folder_label)
        self.browse_btn = QPushButton("Parcourir...")
        self.browse_btn.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.browse_btn)
        params_layout.addLayout(folder_layout)
        
        # Nom du fichier
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Nom du fichier:"))
        self.filename_edit = QLineEdit(self.filename)
        name_layout.addWidget(self.filename_edit)
        name_layout.addWidget(QLabel(".fbx"))
        params_layout.addLayout(name_layout)
        
        main_layout.addWidget(params_group)
        
        # ===== GROUPE CONTRÔLES DE VÉRIFICATIONS =====
        checks_group = QGroupBox("Sélectionner les Vérifications à Effectuer")
        checks_layout = QVBoxLayout(checks_group)
        
        self.check_poly_checkbox = QCheckBox("✓ Vérifier limite de polygones")
        self.check_poly_checkbox.setChecked(True)
        self.check_poly_checkbox.toggled.connect(self.on_check_toggle)
        checks_layout.addWidget(self.check_poly_checkbox)
        
        self.check_uv_count_checkbox = QCheckBox("✓ Vérifier nombre de sets UV")
        self.check_uv_count_checkbox.setChecked(True)
        self.check_uv_count_checkbox.toggled.connect(self.on_check_toggle)
        checks_layout.addWidget(self.check_uv_count_checkbox)
        
        self.check_uv_range_checkbox = QCheckBox("✓ Vérifier UVs dans la plage 0-1")
        self.check_uv_range_checkbox.setChecked(True)
        self.check_uv_range_checkbox.toggled.connect(self.on_check_toggle)
        checks_layout.addWidget(self.check_uv_range_checkbox)
        
        self.check_lightmap_checkbox = QCheckBox("✓ Vérifier lightmaps (2 sets UV minimum)")
        self.check_lightmap_checkbox.setChecked(True)
        self.check_lightmap_checkbox.toggled.connect(self.on_check_toggle)
        checks_layout.addWidget(self.check_lightmap_checkbox)
        
        main_layout.addWidget(checks_group)
        
        # ===== GROUPE INFORMATIONS OBJET SÉLECTIONNÉ =====
        info_group = QGroupBox("Informations Objet Sélectionné")
        info_layout = QVBoxLayout(info_group)
        
        self.info_label = QLabel("Sélectionnez un mesh pour voir les informations")
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("background-color: #f9f9f9; padding: 10px; border: 1px solid #ddd;")
        info_layout.addWidget(self.info_label)
        
        self.check_info_btn = QPushButton("Vérifier Informations Objet")
        self.check_info_btn.clicked.connect(self.check_selected_mesh_info)
        info_layout.addWidget(self.check_info_btn)
        
        main_layout.addWidget(info_group)
        
        # ===== GROUPE RÉSULTATS DES VÉRIFICATIONS =====
        results_group = QGroupBox("Résultats des Vérifications")
        results_layout = QVBoxLayout(results_group)
        
        # Tableau des résultats
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(["Vérification", "Statut"])
        self.results_table.horizontalHeader().setStretchLastSection(False)
        self.results_table.setColumnWidth(0, 350)
        self.results_table.setColumnWidth(1, 150)
        self.results_table.setMaximumHeight(150)
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        results_layout.addWidget(self.results_table)
        
        # Messages détaillés
        results_layout.addWidget(QLabel("Messages Détaillés:"))
        self.results_text = QTextEdit()
        self.results_text.setMaximumHeight(120)
        self.results_text.setReadOnly(True)
        results_layout.addWidget(self.results_text)
        
        main_layout.addWidget(results_group)
        
        # ===== GROUPE BOUTONS D'ACTION =====
        buttons_layout = QHBoxLayout()
        
        self.validate_btn = QPushButton("✓ Juste Vérifier")
        self.validate_btn.clicked.connect(self.validate_only)
        buttons_layout.addWidget(self.validate_btn)
        
        self.export_btn = QPushButton("📦 Vérifier et Exporter")
        self.export_btn.clicked.connect(self.verify_and_export)
        self.export_btn.setEnabled(False)
        buttons_layout.addWidget(self.export_btn)
        
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.close)
        buttons_layout.addWidget(close_btn)
        
        main_layout.addLayout(buttons_layout)

    def on_check_toggle(self, checked):
        """Met à jour l'état des vérifications quand une checkbox est modifiée"""
        self.checks_enabled["poly_count"] = self.check_poly_checkbox.isChecked()
        self.checks_enabled["uv_count"] = self.check_uv_count_checkbox.isChecked()
        self.checks_enabled["uv_range"] = self.check_uv_range_checkbox.isChecked()
        self.checks_enabled["lightmaps"] = self.check_lightmap_checkbox.isChecked()

    def browse_folder(self):
        """Ouvrir le dialogue pour sélectionner le dossier d'export"""
        try:
            folder = cmds.fileDialog2(fileMode=3, caption="Sélectionner le dossier d'export")
            if folder:
                self.export_folder = folder[0]
                self.folder_label.setText(self.export_folder)
                self.export_btn.setEnabled(True)
                self.log_message(f"✅ Dossier sélectionné: {self.export_folder}")
        except Exception as e:
            self.log_message(f"❌ Erreur lors de la sélection du dossier: {e}")

    def log_message(self, message):
        """Ajouter un message au texte de résultats"""
        self.results_text.append(message)

    def clear_results(self):
        """Effacer les résultats précédents"""
        self.results_text.clear()
        self.results_table.setRowCount(0)
        self.last_check_results = {}

    def display_verification_results(self, results):
        """Afficher les résultats des vérifications dans le tableau"""
        self.results_table.setRowCount(len(results))
        
        for idx, (check_name, (status, message)) in enumerate(results.items()):
            # Colonne 1: Nom de la vérification
            name_item = QTableWidgetItem(check_name)
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            self.results_table.setItem(idx, 0, name_item)
            
            # Colonne 2: Statut avec couleur
            status_text = "✅ PASS" if status else "❌ FAIL"
            status_item = QTableWidgetItem(status_text)
            status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
            
            if status:
                status_item.setBackground(QColor("#c8e6c9"))  # Vert clair
            else:
                status_item.setBackground(QColor("#ffcdd2"))  # Rouge clair
            
            self.results_table.setItem(idx, 1, status_item)
            
            # Afficher aussi le message
            self.log_message(f"{check_name}: {message}")

    def check_selected_mesh_info(self):
        """Afficher les informations du mesh sélectionné sans vérification"""
        selection = cmds.ls(selection=True, long=True)
        if not selection:
            self.info_label.setText("❌ Aucun objet sélectionné")
            return

        mesh = selection[0]
        shapes = cmds.listRelatives(mesh, shapes=True)
        if not shapes or cmds.nodeType(shapes[0]) != "mesh":
            self.info_label.setText("❌ L'objet sélectionné n'est pas un mesh")
            return

        try:
            poly_count = cmds.polyEvaluate(mesh, face=True)
            vertex_count = cmds.polyEvaluate(mesh, vertex=True)
            uv_sets = cmds.polyUVSet(mesh, query=True, allUVSets=True)
            uv_count = len(uv_sets) if uv_sets else 0

            info_text = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Mesh: {mesh.split('|')[-1]}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Statistiques:
  • Polygones: {poly_count}
  • Vertices: {vertex_count}
  • Sets UV: {uv_count}

⚙️ Limites configurées:
  • Max polygones: {self.poly_spinbox.value()}
  • Lightmaps attendus: {'OUI (2 sets UV)' if self.checks_enabled['lightmaps'] else 'NON'}
"""
            self.info_label.setText(info_text)
        except Exception as e:
            self.info_label.setText(f"❌ Erreur lors de la récupération des informations: {e}")

        mesh = selection[0]
        shapes = cmds.listRelatives(mesh, shapes=True)
        if not shapes or cmds.nodeType(shapes[0]) != "mesh":
            self.clear_results()
            self.log_message("❌ L'objet sélectionné n'est pas un mesh")
            return

        self.clear_results()
        self.log_message("🧪 Test du modèle en cours…\n")
        
        results = self.check_mesh_detailed(mesh)
        self.display_verification_results(results)
        
        # Résumé global
        all_pass = all(status for status, _ in results.values())
        if all_pass:
            self.log_message("\n✅ ✅ ✅ TOUS LES TESTS SONT PASSÉS ✅ ✅ ✅")
        else:
            self.log_message("\n❌ Certains tests ont échoué. Corrigez les erreurs avant l'export.")

    def validate_only(self):
        """Valider le mesh avec les vérifications activées"""
        selection = cmds.ls(selection=True, long=True)
        if not selection:
            self.clear_results()
            self.log_message("❌ Aucun objet sélectionné")
            return

        mesh = selection[0]
        shapes = cmds.listRelatives(mesh, shapes=True)
        if not shapes or cmds.nodeType(shapes[0]) != "mesh":
            self.clear_results()
            self.log_message("❌ L'objet sélectionné n'est pas un mesh")
            return

        self.clear_results()
        self.log_message("🔍 Vérification du modèle…\n")
        
        results = self.check_mesh_detailed(mesh)
        self.display_verification_results(results)
        
        # Résumé global
        all_pass = all(status for status, _ in results.values())
        if all_pass:
            self.log_message("\n✅ Toutes les vérifications activées sont passées 👍")
        else:
            self.log_message("\n❌ Une ou plusieurs vérifications ont échoué")

    def check_mesh_detailed(self, mesh):
        """Vérifier le mesh et retourner les résultats détaillés"""
        results = {}

        try:
            # ===== VÉRIFICATION 1: Nombre de polygones =====
            if self.checks_enabled["poly_count"]:
                poly_count = cmds.polyEvaluate(mesh, face=True)
                max_polys = self.poly_spinbox.value()
                
                if poly_count > max_polys:
                    status = False
                    message = f"Polygones: {poly_count} / Max: {max_polys} ❌ DÉPASSE"
                else:
                    status = True
                    message = f"Polygones: {poly_count} / Max: {max_polys} ✅"
                
                results["Limite Polygones"] = (status, message)
            
            # ===== VÉRIFICATION 2: UV Range (0-1) =====
            if self.checks_enabled["uv_range"]:
                try:
                    faces = cmds.polyListComponentConversion(mesh, toFace=True)
                    uvs = cmds.polyListComponentConversion(faces, toUV=True)
                    uvs = list(set(uvs))
                    
                    if uvs:
                        uvs_coords = [cmds.polyEditUV(uv, query=True) for uv in uvs]
                        u_values = [uv[0] for uv in uvs_coords]
                        v_values = [uv[1] for uv in uvs_coords]
                        
                        u_min, u_max = min(u_values), max(u_values)
                        v_min, v_max = min(v_values), max(v_values)
                        
                        if u_max > 1 or v_max > 1 or u_min < 0 or v_min < 0:
                            status = False
                            message = f"UVs hors limite: U[{u_min:.2f}-{u_max:.2f}] V[{v_min:.2f}-{v_max:.2f}] ❌"
                        else:
                            status = True
                            message = f"UVs OK: U[{u_min:.2f}-{u_max:.2f}] V[{v_min:.2f}-{v_max:.2f}] ✅"
                    else:
                        status = False
                        message = "Aucune UV trouvée ❌"
                    
                    results["Plage UVs (0-1)"] = (status, message)
                except Exception as e:
                    results["Plage UVs (0-1)"] = (False, f"Erreur: {str(e)}")
            
            # ===== VÉRIFICATION 3: Nombre de sets UV =====
            if self.checks_enabled["uv_count"]:
                uv_sets = cmds.polyUVSet(mesh, query=True, allUVSets=True)
                uv_count = len(uv_sets) if uv_sets else 0
                
                if uv_count > 0:
                    status = True
                    message = f"Sets UV: {uv_count} ✅"
                else:
                    status = False
                    message = "Aucun set UV détecté ❌"
                
                results["Sets UV"] = (status, message)
            
            # ===== VÉRIFICATION 4: Lightmaps (2 sets UV) =====
            if self.checks_enabled["lightmaps"]:
                uv_sets = cmds.polyUVSet(mesh, query=True, allUVSets=True)
                uv_count = len(uv_sets) if uv_sets else 0
                
                if uv_count >= 2:
                    status = True
                    message = f"Lightmaps: {uv_count} sets UV (2 minimum) ✅"
                else:
                    status = False
                    message = f"Lightmaps insuffisantes: {uv_count} sets UV (2 minimum requis) ❌"
                
                results["Lightmaps"] = (status, message)

        except Exception as e:
            results["Erreur Générale"] = (False, f"Erreur lors de la vérification: {e}")

        return results

    def check_mesh(self, mesh):
        """Vérifier le mesh et retourner True/False (compatible avec export)"""
        results = self.check_mesh_detailed(mesh)
        
        # Retourner True seulement si toutes les vérifications activées sont passées
        enabled_results = {k: v for k, v in results.items() 
                          if not k.startswith("Erreur")}
        
        if not enabled_results:
            return True
        
        return all(status for status, _ in enabled_results.values())

    def verify_and_export(self):
        """Vérifier et exporter le mesh"""
        if not self.export_folder:
            self.clear_results()
            self.log_message("❌ Veuillez sélectionner un dossier d'export")
            return

        filename = self.filename_edit.text().strip()
        if not filename:
            self.clear_results()
            self.log_message("❌ Veuillez entrer un nom de fichier")
            return

        selection = cmds.ls(selection=True, long=True, dag=True, shapes=False)
        if not selection:
            self.clear_results()
            self.log_message("❌ Aucun objet sélectionné")
            return

        mesh = selection[0]
        shapes = cmds.listRelatives(mesh, shapes=True)
        if not shapes or cmds.nodeType(shapes[0]) != "mesh":
            self.clear_results()
            self.log_message("❌ L'objet sélectionné n'est pas un mesh")
            return

        self.clear_results()
        self.log_message("🔍 Début des vérifications…\n")
        
        # Afficher les résultats de vérification
        results = self.check_mesh_detailed(mesh)
        self.display_verification_results(results)
        
        # Vérifier si tout est OK
        if not self.check_mesh(mesh):
            self.log_message("\n❌ Vérifications échouées, export annulé")
            return

        # Procéder à l'export
        export_path = os.path.join(self.export_folder, filename + ".fbx")

        try:
            self.log_message("\n📦 Export en cours…")
            cmds.FBXResetExport()
            cmds.select(mesh)
            cmds.file(export_path, force=True, options="v=0;", type="FBX export", exportSelected=True)
            
            self.log_message(f"✅ Export réussi vers: {export_path}")
            QMessageBox.information(self, "Export Réussi", 
                                  f"Le fichier a été exporté avec succès:\n{export_path}")
        except Exception as e:
            self.log_message(f"❌ Erreur lors de l'export: {e}")
            QMessageBox.critical(self, "Erreur d'Export", 
                               f"Erreur lors de l'export:\n{e}")

def show_fbx_export_tool():
    """Afficher ou mettre à jour l'outil d'export FBX"""
    global fbx_export_dialog
    
    try:
        fbx_export_dialog.close()
        fbx_export_dialog.deleteLater()
    except:
        pass
    
    parent = get_maya_main_window()
    fbx_export_dialog = FBXExportTool(parent)
    fbx_export_dialog.show()

# Initialisation
fbx_export_dialog = None

# Pour tester: exécuter show_fbx_export_tool()
# show_fbx_export_tool()
