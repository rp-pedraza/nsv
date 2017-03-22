# Nmap Scans Visualizer

This tool demonstrates visualization of specially-formatted Nmap scan data.  It runs by 3 components:

- An ElasticSearch server were the data is stored and queried
- A backend server using Flask that communicates with the ElasticSearch server and exposes API services to the web
- The frontend server which provides the Web UI that interacts with the user and communicate with the backend server

## Requirements

- A running ElasticSearch server that is accessible to the backend
- Python (Tested with 3.4.3), Ruby, Bash
- [npm](https://www.npmjs.com/)
- [pip](https://pip.pypa.io/en/stable/)

## Installation and Running Frontend and Backend Locally

First, we create a local copy by cloning repo:

    git clone https://github.com/rp-pedraza/nsv.git

Then, we change the working directory to the local copy:

    cd nsv

### Importing Data

Then, we prepare data for importing.  This will process data from the raw JSONified nmap scan files in `data` directory and save them to `data.processed`.

    ruby process-data.rb

After that, we import the processed data to the ElasticSearch server.  The default target server is `localhost:9200`, but it can be changed by opening `import-processed-data.sh` with a text editor and changing the value next to `ELASTICSEARCH_ADDRESS=`.

    bash import-processed-data.sh

### Setting Up and Running the Backend Server

After importing data, we now set up the backend server.  Change the working directory to `backend`:

    cd backend

#### Preparing a Virtualenv Environment

From here, we create an isolated environment through `virtualenv`.

If you don't have the tool installed in your system, you can install it with `pip`.

    pip install virtualenv

Alternatively, you can have it installed for the current user only by adding the `--user` option.  This would install the files in `~/.local`.

You would have to add `~/.local/bin` to the value of the `PATH` variable to be able to relatively execute the `virtualenv` binary.

    pip install virtualenv --user
    PATH=~/.local/bin:${PATH}

You can also make the modification of `PATH` permanent by adding `[[ -f ~/.bashrc ]] && . ~/.bashrc` to `~/.bash_profile` and `PATH=~/.local/bin:${PATH}` to `~/.bashrc`.

Once `virtualenv` is properly installed, we continue with the creation of the environment.  Make sure you're in the `backend` directory before running the following command:

    virtualenv venv

Then, we activate the environment.

    source venv/bin/activate

You would notice a change in your shell prompt when done.  It would be prefixed with `venv`.

At this point, we can now freely install the dependency modules without worrying about causing conflict with other setups.

#### Installing Backend Dependencies

The following command will install all modules listed in `requirements.txt`, which are required by the backend to run.

    pip install -r requirements.txt

Note: For some reason the dependency package `appdirs` does not get installed.  If that happens, just run `pip install appdirs` to install it, and then run `pip install -r requirements.txt` again.

#### Running the Backend

And here, we finally run the backend.  It would interact with the ElasticSearch server which is expected to be listening on `localhost:9200`.  If you have it somewhere else, you can change the values in `config.py`.

    python application.py

The server by default listens on [http://localhost:5000](http://localhost:5000).

### Setting Up and Running the Frontend Server

Open another terminal and change the working directory to `nsv/frontend`.

    cd /path/to/nsv/frontend

We then install `bower` and `npm` components required by the frontend.

    bower install && npm install

Then, we create the server instance.  This may also automatically open up your browser and redirect it to the web applicaton's home page.

    PATH=$(npm bin):$PATH grunt serve

The server by default listens on [http://localhost:9000](http://localhost:9000).

### Compiling the Pages and Running the Frontend Server Statically

We can also compile the frontend to make it more distributable by running:

    PATH=$(npm bin):$PATH grunt build

This would create a compiled version of the site in the `dist` directory.

From there, we can run the simple Python server:

    ( cd dist && python -m http.server )

The server by default listens on `0.0.0.0`, port `8000`.
