FROM ubuntu:20.04

MAINTAINER Kyle Shannon <kyle@pobox.com>

USER root
ADD . /opt/src/windninja/
ADD ../../scripts/ /opt/src/scripts/
SHELL [ "/usr/bin/bash", "-c" ]
ENV DEBIAN_FRONTEND noninteractive
ENV WM_PROJECT_INST_DIR /opt
RUN dpkg-reconfigure debconf --frontend=noninteractive && \
    apt-get update &&  \
    apt-get install -y wget gnupg2 cmake git apt-transport-https ca-certificates \
                       software-properties-common sudo build-essential \
                       pkg-config g++ libboost-program-options-dev \
                       libboost-date-time-dev libboost-test-dev python3-pip && \
    cd /opt/src && \
    DEBIAN_FRONTEND=noninteractive ./windninja/scripts/build_deps_ubuntu_2004.sh && \
    rm -rf /var/lib/apt/lists

RUN cd  /opt/src/windninja && \
    mkdir build && \
    mkdir /data && \
    cd  /opt/src/windninja/build && \
    cmake -D SUPRESS_WARNINGS=ON -DNINJAFOAM=ON -DBUILD_FETCH_DEM=ON  .. && \
    make -j12 && \
    make install && \
    ldconfig && \
    cd /opt/src/windninja && \
    /usr/bin/bash -c scripts/build_libs.sh

RUN source /opt/openfoam8/etc/bashrc &&\
mkdir -p $FOAM_RUN/../applications && \
cp -r /opt/src/windninja/src/ninjafoam/8/* $FOAM_RUN/../applications && \
cd $FOAM_RUN/../applications/ && \
# mkdir /openfoam && \
# cp -r /opt/openfoam8/* /openfoam/ && \
sed -i "s|export WM_PROJECT_INST_DIR=|export WM_PROJECT_INST_DIR=/opt|g" /opt/openfoam8/etc/bashrc && \
sed -i "s|export WM_PROJECT_DIR=\$WM_PROJECT_INST_DIR/openfoam8|export WM_PROJECT_DIR=/opt/openfoam8|g" /opt/openfoam8/etc/bashrc && \
. /opt/openfoam8/etc/bashrc && \
wmake libso && \
cd utility/applyInit && \
wmake  &&\
pip3 install numpy

VOLUME /data
WORKDIR /data
