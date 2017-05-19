# Virtual Environment Notes

Run these commands to initialize the virtual environment

    virtualenv v
    export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python
    . ./v/bin/activate


Run these commands to install the prereqs for our script:

    env LDFLAGS="-L$(brew --prefix openssl)/lib" CFLAGS="-I$(brew --prefix openssl)/include"
    pip install cryptography
    pip install fabric
    pip install configparser
    pip install pycurl


Run these commands to resume the virtual environment

    export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python
    . ./v/bin/activate
