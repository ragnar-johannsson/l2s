FROM debian:8

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update        \
    && apt-get install -y \
        build-essential   \
        curl              \
        git               \
        make              \
        ruby-dev          \
        rubygems          \
        vim               \
        wget              \
    && gem install fpm

# Bake in the src dir instead of using a volume mount
# in case we building the package on a remote host
ADD . /src
