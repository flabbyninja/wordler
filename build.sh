#!/bin/sh

# mkdir -p build && cp wordler.py build
# mkdir -p build/wordlertools && cp -R wordlertools/* build/wordlertools

export BUILD_DIR="build"
export PKG_DIR="python"

mkdir -p ${BUILD_DIR}

rm -rf ${BUILD_DIR}\/${PKG_DIR} &&\
    rm ${BUILD_DIR}\/package.zip &&\
    mkdir -p ${BUILD_DIR}\/${PKG_DIR}


docker run --rm -v $(pwd):/cleanbuild -w /cleanbuild lambci/lambda:build-python3.8 \
    python3 -m venv .venv && \
    . ./.venv/bin/activate && \
    pip install -r lambda_layer/requirements.txt -t ${BUILD_DIR}\/${PKG_DIR}
sudo chown -R $UID:$GID ${BUILD_DIR}

cd ${BUILD_DIR}
rm -rf ${PKG_DIR}/botocore
cp -R ../wordlertools ${PKG_DIR}
zip -9yr package.zip ${PKG_DIR}
sudo rm -rf ${PKG_DIR}