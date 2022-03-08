#!/bin/sh

# mkdir -p build && cp wordler.py build
# mkdir -p build/wordlertools && cp -R wordlertools/* build/wordlertools

export BUILD_DIR="build"
export PKG_DIR="python"

rm -rf ${PKG_DIR} &&\
    rm package.zip &&\
    mkdir -p ${PKG_DIR}

cd ${BUILD_DIR}

docker run --rm -v $(pwd):/cleanbuild -w /cleanbuild lambci/lambda:build-python3.8 \
    python3 -m venv .venv && \
    . ./.venv/bin/activate && \
    pip install -r lambda_layer/requirements.txt -t ${PKG_DIR} && \
sudo chown -R $UID:$GID ${BUILD_DIR}
sudo rm -rf python/botocore
zip -9yr package.zip python
sudo rm -rf python