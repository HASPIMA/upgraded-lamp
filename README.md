# Marvel comics saver

This project is a simple web application that allows users to save
their favorite comics from Marvel.

## Using Docker

### Build project

To build the services it's necessary to include the environment
variables needed to setup postgres, these should be stored in `.env`
file

  ```sh
  docker compose --env-file .env build
  ```

### Running services

In order to use the API, it is necessary to have already built the
services. Once you've done that, you can run the following command:

  ```sh
  docker compose up
  ```

### Stop and remove services

If you want to get rid of the containers for services and volumes,
you should run:

  ```sh
  docker compose down --volumes
  ```
