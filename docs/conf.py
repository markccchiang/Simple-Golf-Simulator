# Configuration file for Sphinx documentation builder.

project = 'Simple Golf Simulator'
copyright = '2026, Cheng-Chin Chiang'
author = 'Cheng-Chin Chiang'
release = '1.0'

extensions = [
    'sphinx.ext.mathjax',
]

templates_path = ['_templates']
exclude_patterns = ['_build']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_title = 'Simple Golf Simulator Documentation'

mathjax3_config = {
    'tex': {
        'macros': {
            'vect': [r'\vec{#1}', 1],
        }
    }
}
