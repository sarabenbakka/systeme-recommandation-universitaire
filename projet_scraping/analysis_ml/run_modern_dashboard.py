"""
Système de Recommandation Universitaire - Dashboard Moderne
Ce script lance l'application Streamlit avec l'interface utilisateur moderne.
"""

import streamlit as st
import os
import sys

# Assurez-vous que tous les modules sont dans le chemin
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Importer le dashboard principal
from modern_dashboard_main import main

# Exécuter l'application
if __name__ == "__main__":
    main()
