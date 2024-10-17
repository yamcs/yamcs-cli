import os

project = "yamcs-cli"
copyright = "2019-present, Space Applications Services"
author = "Yamcs Team"

# The short X.Y version
version = ""

# The full version, including alpha/beta/rc tags
try:
    release = os.environ["DOC_VERSION"]
except KeyError:
    import pkg_resources

    dist = pkg_resources.get_distribution("yamcs-cli")
    release = dist.version

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinxcontrib.fulltoc",
]

# Force-disable conversion of -- to en-dash
smartquotes = False

source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    "fixed_sidebar": False,
    "show_powered_by": False,
    "font_family": "Helvetica,Arial,sans-serif",
    "font_size": "15px",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

html_show_sourcelink = False

latex_elements = {
    "papersize": "a4paper",
    "figure_align": "htbp",
    "extraclassoptions": "openany",
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        f"yamcs-cli-{release}.tex",
        "Yamcs Command-Line Interface",
        "Space Applications Services",
        "manual",
    ),
]

man_pages = [
    (
        "yamcs",
        "yamcs",
        "Yamcs command-line interface",
        author,
        1,
    ),
    (
        "yamcs_alarms",
        "yamcs-alarms",
        "Manage alarms",
        author,
        1,
    ),
    (
        "yamcs_algorithms",
        "yamcs-algorithms",
        "Read algorithms",
        author,
        1,
    ),
    (
        "yamcs_commands",
        "yamcs-commands",
        "Read commands",
        author,
        1,
    ),
    (
        "yamcs_config",
        "yamcs-config",
        "Manage Yamcs CLI properties",
        author,
        1,
    ),
    (
        "yamcs_containers",
        "yamcs-containers",
        "Read containers",
        author,
        1,
    ),
    (
        "yamcs_dbshell",
        "yamcs-dbshell",
        "Launch Yamcs DB Shell",
        author,
        1,
    ),
    (
        "yamcs_events",
        "yamcs-events",
        "Read and create events",
        author,
        1,
    ),
    (
        "yamcs_instances",
        "yamcs-instances",
        "Manage Yamcs instances",
        author,
        1,
    ),
    (
        "yamcs_links",
        "yamcs-links",
        "Read and manipulate data links",
        author,
        1,
    ),
    (
        "yamcs_login",
        "yamcs-login",
        "Login to a Yamcs server",
        author,
        1,
    ),
    (
        "yamcs_logout",
        "yamcs-logout",
        "Logout of a Yamcs server",
        author,
        1,
    ),
    (
        "yamcs_packets",
        "yamcs-packets",
        "Read packets",
        author,
        1,
    ),
    (
        "yamcs_parameter-archive",
        "yamcs-parameter-archive",
        "Manipulate the Parameter Archive",
        author,
        1,
    ),
    (
        "yamcs_parameters",
        "yamcs-parameters",
        "Manage parameters",
        author,
        1,
    ),
    (
        "yamcs_processors",
        "yamcs-processors",
        "Manage processors",
        author,
        1,
    ),
    (
        "yamcs_rocksdb",
        "yamcs-rocksdb",
        "Manage RocksDB storage engine",
        author,
        1,
    ),
    (
        "yamcs_services",
        "yamcs-services",
        "Read and manipulate services",
        author,
        1,
    ),
    (
        "yamcs_space-systems",
        "yamcs-space-systems",
        "Read space systems",
        author,
        1,
    ),
    (
        "yamcs_storage",
        "yamcs-storage",
        "Manage object storage",
        author,
        1,
    ),
    (
        "yamcs_streams",
        "yamcs-streams",
        "Read and manipulate streams",
        author,
        1,
    ),
    (
        "yamcs_tables",
        "yamcs-tables",
        "Read and manipulate tables",
        author,
        1,
    ),
]
