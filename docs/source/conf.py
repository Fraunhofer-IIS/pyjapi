# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import pathlib
import sys
import os
sys.path.insert(0, pathlib.Path(__file__).parent.parent.parent/'src')
# include source directory to load custom extensions
sys.path.insert(0, os.path.abspath(os.path.dirname('__file__')))

# -- Project information -----------------------------------------------------

project = 'pyjapi'
copyright = '2020, Jannis Mainczyk'
author = 'Jannis Mainczyk'

# The full version, including alpha/beta/rc tags
release = '0.4.0'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    'sphinx.ext.intersphinx',
    "sphinx_automodapi.automodapi",
    'sphinx_automodapi.smart_resolver',
    'sphinxcontrib.programoutput',  # Dynamically generate script output
    'sphinx_click.ext',  # Generate documentation for click cli
    'sphinx.ext.graphviz',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinxcontrib.images',  # include images as thumbnails in HTML output
    'sphinx_git',  # include excerpts from your git history
    # 'sphinx.ext.ifconfig',
    # 'sphinxcontrib.mermaid',
    # 'sphinx_issues',
    # autosummary is required to be explicitly loaded by confluencebuilder
    # (see https://github.com/sphinx-contrib/confluencebuilder/issues/304)
    'sphinx.ext.autosummary',
    'sphinxcontrib.confluencebuilder',
    # Include Markdown Files (README, CHANGELOG, ...)
    'recommonmark',
    'sphinxext.jsonschemaext',  # include jsonschema validation output
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'restructuredtext',
    '.md': 'markdown',
}

default_role = 'py:obj'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
import sphinx_nameko_theme
html_theme_path = [sphinx_nameko_theme.get_html_theme_path()]
html_theme = 'nameko'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_logo = '_static/logo.png'

# -- Options for Confluence Builder ------------------------------------------
# https://sphinxcontrib-confluencebuilder.readthedocs.io/

confluence_publish = True
confluence_server_url = 'https://intern.iis.fhg.de/'
confluence_server_user = 'mkj'
confluence_server_pass = os.getenv("CONF_PW")
# confluence_server_pass = "Vwdhw]NUz/WT7dsexv.FRjv/bt"
confluence_parent_page = 'Home'
confluence_space_name = 'DOCS'

# Generic configuration.
confluence_page_hierarchy = True

# Publishing configuration.
# confluence_purge = True

# -- Options for sphinx-automodapi -----------------------------------------------
# Doesn't seem to work with singlehtml builder

# numpydoc_show_class_members = False  # supposedly required to prevent duplicate entries
# automodapi_toctreedirnm = 'api'  # default: 'api'

# -- Options for intersphinx -------------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pytest': ('https://docs.pytest.org/en/latest/', None)
}

# -- Options for sphinxcontrib-images ----------------------------------------
# https://sphinxcontrib-images.readthedocs.io/en/latest/
images_config = {
    'backend': 'LightBox2',  # default: 'LightBox2'
    'override_image_directive': False,  ## default: False
    'cache_path': '_images',  # default: '_images'
    'requests_kwargs': {},  # default: {}
    'default_image_width': '100%',  # default: '100%'
    'default_image_height': 'auto',  # default: 'auto'
    'default_group': None,  # default: None
    'default_show_title': False,  # default: False (broken)
    'download': True,  # default: True
}

# -- Options for sphinx-git --------------------------------------------------
# https://sphinx-git.readthedocs.io/en/latest/using.html

# -- Options for jsonschemaext -----------------------------------------------
jsonschema_standard = 7

# -- Options for sphinxcontrib-programoutput ---------------------------------
# https://sphinxcontrib-programoutput.readthedocs.io/

# A format string template for the output of the prompt option to command-output. default: '$ {command}\n{output}'
# Available variables: {command} {output} {returncode}
# programoutput_prompt_template = "$ {command}\n{output}"