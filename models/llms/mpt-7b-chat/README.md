# MPT-7b-chat

Chat + Completions RPC demo

## Running the docker container

* **Build** - Choose one method to build the image
  1) Simple Build *(recommended)* - Use the default LeapfrogAI base version defined in the docker image
     * `docker build . --tag leapfrogai/mpt-7b-chat:latest`

  2) Advanced Build - Use the latest LeapfrogAI base version
     * `export IMAGE_TAG=<latest-image-tag>`
       * Replace `<latest-image-tag>` with the latest [latest LeapfrogAI base container image](https://github.com/defenseunicorns/leapfrogai/pkgs/container/leapfrogai%2Fbase).
     * `docker build . --tag leapfrogai/mpt-7b-chat:latest --build-arg="$IMAGE_TAG"`

* **Run**
  * `docker run --rm --gpus all -p 50051:50051 -d --name mpt-7b-chat leapfrogai/mpt-7b-chat:latest`
