# -- Path setup --------------------------------------------------------------
from datetime import date

from pallets_sphinx_themes import ProjectLink

from python_rucaptcha import (
    core,
    control,
    prosopo,
    tencent,
    gee_test,
    hcaptcha,
    turnstile,
    amazon_waf,
    mt_captcha,
    re_captcha,
    atb_captcha,
    captcha_fox,
    capy_puzzle,
    fun_captcha,
    key_captcha,
    grid_captcha,
    text_captcha,
    image_captcha,
    lemin_captcha,
    rotate_captcha,
    datadome_captcha,
    friendly_captcha,
    cyber_siara_captcha,
    draw_around_captcha,
    bounding_box_captcha,
)
from python_rucaptcha.__version__ import __version__

# -- Project information -----------------------------------------------------
project = "python-rucaptcha"
copyright = (
    f"{date.today().year}, " + f"AndreiDrang; Release - {__version__}; " + f"Last update - {date.today()}"
)
author = "AndreiDrang"

# -- General configuration ---------------------------------------------------
extensions = (
    "myst_parser",
    "sphinx.ext.napoleon",
    "pallets_sphinx_themes",
    "enum_tools.autoenum",
    "notfound.extension",
)
myst_enable_extensions = ["deflist"]
intersphinx_mapping = {"python": ("https://docs.python.org/3.10/", None)}
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# Theme config
html_theme = "jinja"
html_theme_options = {"index_sidebar_logo": False}
html_static_path = ["_static"]
html_favicon = "_static/favicon.png"
html_logo = "_static/RuCaptchaMedium.png"
html_title = f"python-rucaptcha ({__version__})"
html_show_sourcelink = False

html_context = {
    "project_links": [
        ProjectLink("PyPI Releases", "https://pypi.org/project/python-rucaptcha/"),
        ProjectLink("Source Code", "https://github.com/AndreiDrang/python-rucaptcha"),
        ProjectLink(
            "2Captcha/RuCaptcha",
            "https://rucaptcha.com/?from=4170435",
        ),
        ProjectLink(
            "DeathByCaptcha",
            "https://deathbycaptcha.com?refid=1237267242",
        ),
        ProjectLink("RedPandaDev group", "https://red-panda-dev.xyz/blog/"),
    ]
}
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html", "ethicalads.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html", "ethicalads.html"],
}

# Typehints config
autodoc_typehints = "both"
autodoc_typehints_description_target = "documented"
autodoc_typehints_format = "short"

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = True
napoleon_type_aliases = True
napoleon_attr_annotations = True

autodoc_preserve_defaults = False
autodoc_member_order = "bysource"
autodoc_class_signature = "mixed"
