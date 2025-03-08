# Makefile per compilare il documento LaTeX con XeLaTeX e BibTeX
# Include supporto per ambiente virtuale Python per generare grafici SVG

# Nome del file principale LaTeX (senza l'estensione .tex)
FILENAME ?= main

# Comandi per i tool
LATEX = xelatex
BIBTEX = bibtex
PYTHON = python3
PIP = pip3

# Directory virtuenv
VENV_DIR = venv
VENV_ACTIVATE = $(VENV_DIR)/bin/activate

# Comandi Python nell'ambiente virtuale
VENV_PYTHON = . $(VENV_ACTIVATE) && python3.13
VENV_PIP = . $(VENV_ACTIVATE) && pip

# Opzioni per il compilatore LaTeX
LATEX_OPTIONS = --halt-on-error

# Directory per gli script Python e output SVG
SCRIPTS_DIR = scripts
SVG_DIR = figures/svg

# Target predefinito: compila il documento
all: $(FILENAME).pdf

# Regola per compilare il documento LaTeX
$(FILENAME).pdf: $(FILENAME).tex venv-check svg-check
	$(LATEX) $(LATEX_OPTIONS) $(FILENAME).tex
	$(BIBTEX) $(FILENAME)
	$(LATEX) $(LATEX_OPTIONS) $(FILENAME).tex
	$(LATEX) $(LATEX_OPTIONS) $(FILENAME).tex

# Pulisce i file temporanei generati durante la compilazione
clean:
	rm -f $(FILENAME).aux $(FILENAME).log $(FILENAME).out $(FILENAME).pdf $(FILENAME).toc $(FILENAME).bbl $(FILENAME).blg

# Pulisce completamente i file intermedi e il PDF finale
clean-all: clean clean-svg
	rm -f $(FILENAME).lof $(FILENAME).lot

# Configura l'ambiente virtuale Python
venv:
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -r requirements.txt

# Verifica se l'ambiente virtuale esiste, altrimenti lo crea
venv-check:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Ambiente virtuale non trovato. Creazione in corso..."; \
		$(MAKE) venv; \
	fi

# Genera file SVG con gli script Python
svg: venv-check
	@mkdir -p $(SVG_DIR)
	$(VENV_PYTHON) $(SCRIPTS_DIR)/create_timeline.py
	$(VENV_PYTHON) $(SCRIPTS_DIR)/create_technology_graph.py
	$(VENV_PYTHON) $(SCRIPTS_DIR)/create_approach_pie.py

# Verifica se i file SVG esistono, altrimenti li genera
svg-check:
	@if [ ! -d "$(SVG_DIR)" ] || [ $$(ls -1 $(SVG_DIR)/*.svg 2>/dev/null | wc -l) -eq 0 ]; then \
		echo "File SVG non trovati. Generazione in corso..."; \
		$(MAKE) svg; \
	fi

# Pulisce i file SVG generati
clean-svg:
	rm -rf $(SVG_DIR)/*.svg

# Aggiorna i file SVG rigenerandoli
update-svg: clean-svg svg

# Rimuove l'ambiente virtuale Python
clean-venv:
	rm -rf $(VENV_DIR)

# Specifica i target che non sono file
.PHONY: all clean clean-all venv venv-check svg svg-check clean-svg update-svg clean-venv