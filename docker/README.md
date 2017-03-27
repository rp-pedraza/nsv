# Building and Running Images Locally

To build images you first have to prepare the following files and/or
directories:

- frontend/html/*

  These files are basically the ones generated in ../frontend/dist.
  You can simply copy the whole directory as 'html'.

  If you're in the same directory where this README.md file exists, you
  can run this command:

      cp -av ../frontend/dist frontend/html

  Note: It's not necessary to configure and rebuild the pre-existing
  files in ../frontend/dist since they are dynamic enough for common
  deployments.  The only thing needed to be modified to build the
  frontend image is the value of NSV_FRONTEND_SERVERNAME variable in
  docker-compose.yml.

- backend/application.py, backend/config.py, and backend/requirements.txt

  These files are same files in ../backend.  They already exist, and
  normally don't need to be updated, but if you do make changes, make
  sure that the target elasticsearch hostname in config.py is
  kept set to 'nsv-es'.

- initial-data-uploader/data.processed/*

  You can create these files by running the following command:

      ruby ../process-data.rb ../data initial-data-uploader/data.processed

  Or if ../data.processed already exists, you can simply copy the
  whole directory and save it to initial-data-uploader/.

  Note: The initial-data-uploader image is not really a requirement
  since its only purpose is to upload the initial data to elasticsearch.
  If you want, you can just simply call `bash `import-processed-data.sh`
  after the elasticsearch container has loaded and initialized.  Just
  make sure that the port 9200 is published as 9200.  If you publish it
  as another port, you can use a modified copy of
  import-processed-data.sh where all instances of 9200 are replaced with
  the differnet port.

Now to build the images using docker-compose.yml, run:

    docker-compose build

And to run the containers, do:

    docker-compose up

You can try accessing http://localhost:80/ after the data has been
initially loaded, which is about 40 seconds.

# Prebuilt Images

I created stack-files but I weren't able to make to them really work yet
since I'm getting some issues which could be specific to my setup.  Feel
free to try them.
