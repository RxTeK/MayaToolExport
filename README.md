# 🎮 Maya FBX Export Tool Advanced

![Maya](https://img.shields.io/badge/Maya-2026+-37A5CC?logo=autodesk&logoColor=white)
![Python](https://img.shields.io/badge/Python-3-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Mac%20%7C%20Linux-lightgrey)

Outil d'export FBX professionnel pour Autodesk Maya avec **vérifications automatiques de qualité** avant export. Idéal pour les pipelines de production de jeux vidéo et les assets 3D optimisés.

![FBX Tool Banner](https://img.shields.io/badge/FBX-Export%20Tool-blue?style=for-the-badge)

---

## ✨ Fonctionnalités

- ✅ **Vérification du Poly Count** - Limite configurable pour optimiser les performances
- ✅ **Validation des UVs** - Détection automatique des UVs hors range (0-1)
- ✅ **Contrôle des UV Sets** - Vérification du nombre de sets UV
- ✅ **Détection des Lightmaps** - Validation des lightmaps (minimum 2 sets UV)
- ✅ **Interface Graphique Complète** - PySide6 moderne et intuitive
- ✅ **Rapport Détaillé** - Tableau de résultats avec statuts colorés
- ✅ **Mode Test** - Validation sans export pour débogage rapide
- ✅ **Configuration Flexible** - Active/désactive les vérifications selon tes besoins

---

## 🚀 Installation Ultra-Rapide

### Méthode Drag & Drop (10 secondes)

1. **Télécharge** ce repository :

2. **Décompresse** le fichier ZIP

3. **Ouvre Maya 2026+**

4. **Drag & Drop** le fichier `Install.mel` dans le viewport Maya

5. ✅ **C'est tout !** Un bouton "FBX" apparaît sur ton shelf

![Installation Demo](https://img.shields.io/badge/Drag%20%26%20Drop-Installation-brightgreen?style=for-the-badge)

---

## 📖 Utilisation

### Lancer l'Outil

Clique simplement sur le bouton **FBX** dans ton shelf Maya.

### Workflow Recommandé

1. **Sélectionne** ton mesh dans la scène
2. **Configure** les paramètres :
- Limite de polygones (par défaut : 10,000)
- Vérifications à effectuer
- Dossier d'export
- Nom du fichier
3. **Clique** sur "Vérifier Informations Objet" pour voir les stats
4. **Teste** avec "Tester le Modèle" (sans export)
5. **Exporte** avec "Vrifier et Exporter"

### Captures d'Écran

L'interface affiche :
- 📊 **Tableau de résultats** avec statuts (PASS/FAIL) colorés
- 📝 **Messages détaillés** pour chaque vérification
- 📈 **Informations en temps réel** sur le mesh sélectionné

---

## ⚙️ Configuration

### Vérifications Disponibles

| Vérification | Description | Par Défaut |
|--------------|-------------|------------|
| **Limite Polygones** | Vérifie que le poly count ne dépasse pas la limite | ✅ Activée |
| **Nombre de Sets UV** | Détecte les objets sans UVs | ✅ Activée |
| **Plage UVs (0-1)** | Vérifie que les UVs sont dans la range valide | ✅ Activée |
| **Lightmaps** | Valide la présence de 2+ sets UV pour lightmaps | ✅ Activée |

Tu peux activer/désactiver chaque vérification via les checkboxes dans l'interface.

---

## 🛠️ Compatibilité

- **Maya** : 2026 et supérieur (PySide6)
- **OS** : Windows, macOS, Linux
- **Python** : 3.x (intégré à Maya)

> ⚠️ **Note** : Maya 2025 et versions antérieures utilisent PySide2. Ce script est optimisé pour Maya 2026+ avec PySide6.

---

## 🗑️ Désinstallation

Pour supprimer complètement l'outil :

1. **Drag & Drop** le fichier `Uninstall.mel` dans Maya

2. ✅ Confirmation automatique de la suppression

Le script supprime :
- Le fichier Python du dossier scripts Maya
- Tous les boutons shelf associés
- Affiche un rapport de désinstallation

![Uninstall](https://img.shields.io/badge/Uninstall-One%20Click-red?style=for-the-badge)

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésite pas à :
- 🐛 Signaler des bugs via les [Issues](../../issues)
- 💡 Proposer de nouvelles fonctionnalités
- 🔧 Soumettre des Pull Requests

---

## 🎯 Cas d'Usage

Parfait pour :
- 🎮 **Game Artists** - Assets optimisés pour Unreal/Unity
- 🏢 **Studios de Production** - Pipeline standardisé d'export
- 🎓 **Étudiants** - Apprentissage des bonnes pratiques 3D
- 🔧 **Technical Artists** - Outil personnalisable pour équipe

---

## 📬 Support

Des questions ? Des problèmes ?
- 📧 Ouvre une [Issue](../../issues) sur GitHub
- 💬 Consulte la documentation dans le code source

---

## ⭐ Remerciements

Développé avec ❤️ pour la communauté Maya.

Si cet outil t'aide, n'hésite pas à mettre une ⭐ sur le repo !

---

<div align="center">

**[⬆ Retour en haut](#-maya-fbx-export-tool-advanced)**

Made with 🎨 for Maya Artists

</div>


