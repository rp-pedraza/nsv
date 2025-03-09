The `requirements.txt` file only contains the snapshot of the packages
that worked since this source code has been developed or tested.

The packages can be refreshed to newer versions by simply installing the
immediate dependencies in a new virtual environment:

    rm -fr ./.venv
    python -m venv ./venv
    . ./venv/bin/activate
    pip install flask
    pip install Flask_RESTful
    pip install flask_cors
    pip install requests
    python application.py

Also see `python -m pip freeze --help`.
