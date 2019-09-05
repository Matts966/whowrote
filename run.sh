#!/bin/bash
docker run --name notebook \
  --user=root  \
  # -e NB_UID=$(id -u) \
  # -e NB_GID=$(id -g) \
  -e CHOWN_HOME=yes \
  -e GRANT_SUDO=yes \
  -v $(pwd):/home/jovyan/work -d -p 8888:8888 \
  jupyter/datascience-notebook \
  jupyter notebook --allow-root 2>/dev/null
url=$(docker exec notebook jupyter notebook list | grep http | awk '{print $1}')
if [[ -z $url ]]; then
    echo server is not ready. try again later.
    exit 1
fi

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    xdg-open $url
elif [[ "$OSTYPE" == "darwin"* ]]; then
    open $url
else
    echo $url
fi
