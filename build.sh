#!/bin/sh

# mkdir -p build && cp wordler.py build
# mkdir -p build/wordlertools && cp -R wordlertools/* build/wordlertools

export PKG_DIR="python"

rm -rf ${PKG_DIR} &&\
    rm package.zip &&\
    mkdir -p ${PKG_DIR}

docker run --rm -v $(pwd):/foo -w /foo lambci/lambda:build-python3.8 \
    python3 -m venv .venv && \
    . ./.venv/bin/activate && \
    pip install -r requirements-prod.txt -t ${PKG_DIR} && \
sudo chown -R $UID:$GID ${PKG_DIR}
sudo rm -rf python/botocore
zip -9yr package.zip python
sudo rm -rf python