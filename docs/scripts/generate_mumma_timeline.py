#!/usr/bin/env python3
"""
Script per generare una timeline LaTeX delle opere di Gordon Mumma
utilizzando il package chronology e i dati da un file YAML.
"""
import yaml
import sys
from datetime import datetime

def load_yaml_data(filename):
    """Carica i dati dal file YAML."""
    with open(filename, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def generate_timeline(data, output_file):
    """Genera il file LaTeX con la timeline."""
    # Ordina le opere per anno
    opere = sorted(data['opere'], key=lambda x: x['anno'])
    
    # Trova gli anni minimo e massimo
    min_year = min(opera['anno'] for opera in opere)
    max_year = max(opera['anno'] for opera in opere) + 2  # Aggiungi spazio
    
    # Inizio del documento LaTeX - usando triple apici e concatenazione diretta
    latex = r"""\documentclass[a4paper,12pt]{article}
\usepackage{chronology}
\usepackage[italian]{babel}
\usepackage{xcolor}

\title{Timeline delle opere di Gordon Mumma}
\author{}
\date{\today}

\begin{document}

\maketitle

\section*{Cronologia delle opere principali}

% Timeline principale con tutti gli eventi
\begin{chronology}[5]{""" + str(min_year) + r"""}{""" + str(max_year) + r"""}{\textwidth}[90ex]
"""
    
    # Aggiungi ogni opera come punto singolo
    for opera in opere:
        latex += r"\event{" + str(opera['anno']) + r"}{" + opera['titolo'] + r"}" + "\n"
    
    # Chiudi la prima timeline
    latex += r"\end{chronology}" + "\n\n"
    
    # Aggiungi la timeline dettagliata con approcci
    latex += r"\vspace{1cm}" + "\n\n"
    latex += r"\section*{Timeline dettagliata con opere e approcci}" + "\n\n"
    latex += r"\begin{chronology}[5]{" + str(min_year) + r"}{" + str(max_year) + r"}{\textwidth}[90ex]" + "\n"
    
    for i, opera in enumerate(opere):
        next_year = opere[i+1]['anno'] if i < len(opere)-1 else opera['anno'] + 1
        # Evento con descrizione approccio
        approccio_desc = opera['titolo'] + " (" + opera['approccio'] + ")"
        latex += r"\event[" + str(opera['anno']) + r"]{" + str(next_year) + r"}{" + approccio_desc + r"}" + "\n"
    
    latex += r"\end{chronology}" + "\n\n"
    
    # Aggiungi la timeline delle tecnologie
    if 'tecnologie_sviluppate' in data:
        latex += r"\vspace{1cm}" + "\n\n"
        latex += r"\section*{Timeline delle tecnologie sviluppate}" + "\n\n"
        latex += r"\begin{chronology}[5]{" + str(min_year) + r"}{1980}{\textwidth}[90ex]" + "\n"
        
        for tech in data['tecnologie_sviluppate']:
            if 'periodo' in tech:
                period = tech['periodo'].split('-')
                if len(period) == 2:
                    start_year = int(period[0])
                    end_year = int(period[1])
                    latex += r"\event[" + str(start_year) + r"]{" + str(end_year) + r"}{" + tech['nome'] + r"}" + "\n"
        
        latex += r"\end{chronology}" + "\n\n"
    
    # Aggiungi note sulle tecnologie
    latex += r"\vspace{1cm}" + "\n\n"
    latex += r"\section*{Note sulle tecnologie principali}" + "\n"
    latex += r"\begin{itemize}" + "\n"
    for opera in opere:
        tecnologie = ", ".join(opera['tecnologie'][:2]) if opera['tecnologie'] else "N/A"
        latex += r"  \item \textbf{" + opera['titolo'] + r"}: " + tecnologie + "\n"
    latex += r"\end{itemize}" + "\n\n"
    
    # Aggiungi la legenda
    latex += r"""
\section*{Legenda degli approcci}
\begin{itemize}
  \item \textbf{Approccio generativo}: sistemi che reagiscono e evolvono durante l'esecuzione
  \item \textbf{Approccio deterministico}: composizioni con struttura predefinita
\end{itemize}

\end{document}
"""
    
    # Scrivi il file LaTeX
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(latex)
    
    print(f"File LaTeX generato: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Utilizzo: python generate_mumma_timeline.py input.yaml output.tex")
        sys.exit(1)
    
    yaml_file = sys.argv[1]
    output_file = sys.argv[2]
    
    data = load_yaml_data(yaml_file)
    generate_timeline(data, output_file)