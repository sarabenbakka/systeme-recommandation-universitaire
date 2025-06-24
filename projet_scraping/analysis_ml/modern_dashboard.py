import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
from datetime import datetime
import time

# Import des modules personnalisés
from utils import load_data, create_custom_theme, display_metric_card, display_recommendation_card
from job_profiles_recommender import recommend_profiles
from university_recommender import UniversityRecommender

# Configuration de la page
st.set_page_config(
    page_title="Système de Recommandation Universitaire",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Appliquer le thème personnalisé
create_custom_theme()

# Fonction pour créer un en-tête animé
def create_animated_header(title, subtitle):
    st.markdown(f"""
    <header>
        <h1 class="header-title animate-fadeIn">{title}</h1>
        <p class="header-subtitle animate-fadeIn">{subtitle}</p>
    </header>
    """, unsafe_allow_html=True)

# Fonction pour afficher une carte métrique moderne avec icône
def display_modern_metric(icon, title, value, delta=None, delta_color="normal"):
    delta_html = ""
    if delta:
        delta_class = "metric-delta-positive" if delta_color == "normal" else "metric-delta-negative"
        delta_icon = "fa-arrow-up" if delta_color == "normal" else "fa-arrow-down"
        delta_html = f'<div class="metric-delta {delta_class}"><i class="fas {delta_icon}"></i> {delta}</div>'
    
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon"><i class="fas {icon}"></i></div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{title}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

# Fonction pour créer une carte de profil interactive
def display_profile_card(title, description, skills, badges=None):
    badges_html = ""
    if badges:
        for badge, is_primary in badges:
            badge_class = "badge-primary" if is_primary else "badge-secondary"
            badges_html += f'<span class="{badge_class}">{badge}</span>'
    
    skills_html = ""
    for skill in skills[:5]:  # Limiter à 5 compétences pour l'affichage
        skills_html += f'<span class="badge">{skill}</span>'
    
    st.markdown(f"""
    <div class="recommendation-card">
        <div class="recommendation-title">{title}</div>
        <div class="recommendation-content">{description}</div>
        <div class="recommendation-subtitle">Compétences clés:</div>
        <div>{skills_html}</div>
        <div style="margin-top: 10px;">{badges_html}</div>
    </div>
    """, unsafe_allow_html=True)

# Fonction pour créer un graphique interactif avec Plotly
def create_interactive_chart(df, x, y, title, color=None, type="bar"):
    if type == "bar":
        fig = px.bar(
            df, x=x, y=y, color=color,
            title=title,
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
    elif type == "line":
        fig = px.line(
            df, x=x, y=y, color=color,
            title=title,
            template="plotly_white",
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Bold
        )
    elif type == "pie":
        fig = px.pie(
            df, names=x, values=y,
            title=title,
            template="plotly_white",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Bold
        )
    
    fig.update_layout(
        font=dict(family="Inter, sans-serif"),
        title_font=dict(size=20, family="Inter, sans-serif", color="#1e293b"),
        legend_title_font=dict(size=14),
        legend_font=dict(size=12),
        hoverlabel=dict(font_size=14, font_family="Inter, sans-serif"),
        hovermode="closest"
    )
    
    return fig
