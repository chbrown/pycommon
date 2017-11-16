# `pycommon`

General purpose Python programming modules.


#### Install from source with pip:

    pip install -U git+https://github.com/chbrown/pycommon


#### Develop locally:

    git clone https://github.com/chbrown/pycommon.git
    cd pycommon

Link to development sources from Python `site-packages` directory:

    SITE_PACKAGES=$(python -c 'import os,site;print(os.path.realpath(next(iter(site.getsitepackages()))))')
    pwd > "$SITE_PACKAGES"/pycommon.pth


#### Use modules:

    import pycommon
    print(pycommon.__version__)

    from pycommon.algebraic import AlgebraicDict
    from pycommon.memo import memoized_property


## License

Copyright 2015-2017 Christopher Brown. [MIT Licensed](http://chbrown.github.io/licenses/MIT/#2015-2017).
