#!/usr/bin/env python3
"""
Script per generare una timeline SVG delle opere di Gordon Mumma.
"""
import json
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D

# Configura le directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')
SVG_DIR = os.path.join(ROOT_DIR, 'figures/svg')

# Assicurati che la directory di output esista
os.makedirs(SVG_DIR, exist_ok=True)

def load_data():
    """Carica i dati dal file JSON."""
    data_file = os.path.join(DATA_DIR, 'mumma_works.json')
    
    # Se il file non esiste, crea un set di dati di esempio
    if not os.path.exists(data_file):
        print(f"File {data_file} non trovato. Utilizzo dati di esempio.")
        return [
            {"titolo": "Mesa", "anno": 1966, "approccio": "deterministico", 
             "tecnologie": ["oscillatori", "filtri"]},
            {"titolo": "Hornpipe", "anno": 1967, "approccio": "generativo", 
             "tecnologie": ["cybersonic console", "corno francese"]},
            {"titolo": "Conspiracy 8", "anno": 1970, "approccio": "generativo", 
             "tecnologie": ["nastro magnetico", "feedback"]},
            {"titolo": "Telepos", "anno": 1971, "approccio": "generativo", 
             "tecnologie": ["sensori di movimento", "cybersonic console"]}
        ]
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Gestisce sia il formato con 'opere' che l'array diretto
    return data['opere'] if isinstance(data, dict) and 'opere' in data else data

def create_timeline():
    """Crea una timeline delle opere di Mumma e la salva come SVG."""
    opere = load_data()
    
    # Converti in DataFrame per facilità di manipolazione
    df = pd.DataFrame([{
        'opera': opera['titolo'],
        'anno': opera['anno'],
        'approccio': opera['approccio'],
        'tecnologia': opera['tecnologie'][0] if 'tecnologie' in opera and opera['tecnologie'] else 'N/A'
    } for opera in opere])
    
    # Ordina per anno
    df = df.sort_values('anno')
    
    # Mappa gli approcci a colori
    color_map = {"generativo": "blue", "deterministico": "red"}
    colors = [color_map.get(app, "gray") for app in df["approccio"]]
    
    # Crea la figura
    plt.figure(figsize=(12, 6))
    
    # Crea la timeline
    plt.scatter(df["anno"], np.zeros_like(df["anno"]), s=120, c=colors)
    
    # Aggiungi etichette per le opere
    for i, row in df.iterrows():
        plt.annotate(row["opera"], 
                    xy=(row["anno"], 0),
                    xytext=(0, 20 if i % 2 == 0 else -20),
                    textcoords="offset points",
                    ha='center', va='center',
                    fontweight='bold')
        
        # Aggiungi info sulla tecnologia
        plt.annotate(row["tecnologia"], 
                    xy=(row["anno"], 0),
                    xytext=(0, 40 if i % 2 == 0 else -40),
                    textcoords="offset points",
                    ha='center', va='center',
                    fontsize=8)
    
    # Configura l'aspetto
    plt.grid(False)
    plt.yticks([])
    plt.title("Timeline delle opere di Gordon Mumma", fontsize=14)
    
    # Nascondi le linee dei bordi e dell'asse y
    ax = plt.gca()
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Aggiungi una legenda
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Approccio generativo'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='Approccio deterministico')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    
    # Salva come SVG
    output_file = os.path.join(SVG_DIR, 'mumma_timeline.svg')
    plt.savefig(output_file, format='svg', bbox_inches='tight')
    print(f"Timeline salvata come {output_file}")
    
    plt.close()

if __name__ == "__main__":
    create_timeline()