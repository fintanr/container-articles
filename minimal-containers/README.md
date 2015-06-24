## Introduction

At [Weave](http://weave.works/), we, as you would expect, distribute all of our software as containers, and make heavy use of both Alpine Linux and the ability to build a container “from scratch”.

When you first experiment with Docker many of the initial examples you come across are based on Ubuntu, Debian and other full Linux distributions. Indeed we provide similar examples in our own getting started guides. 

This approach of building from a full distribution is, however, less than optimal. In this post we will cover why you should consider using a minimal distribution such as Alpine Linux for your containers, and provide a number of simple examples. 

## Background

Firstly let us step back a little bit from distributions and consider the purpose of containers. At their simplest level containers use various kernel facilities, such as cgroups and namespaces, to provide resource and process isolation. Unlike a virtual machine, and in spite of the examples, containers do not require a complete, or, depending on the circumstances, any, operating system.

However, an operating system does provide very useful primitives, particularly in terms of packaging and distributing software. Given this it make sense to use operating systems as the basis for our containers in most cases and for most users.

The question which arises, is just how much of the operating system infrastructure and internal plumbing you really need to allow your application to run. The answer, generally, is not very much and reducing the overall footprint of an operating system is a good security practice.  Given this, starting from a very small footprint and adding in the components you need is preferable to removing components from a larger distribution.

## Introducing Alpine Linux

Alpine Linux is a lightweight, secure by default, Linux distribution with a simple, and up to date set of packages for use. It is intended for general-purpose use, and more importantly has a design principle of trying to stay out of your way.

Gliderlabs have developed an ["Alpine Linux Docker Image"](https://github.com/gliderlabs/docker-alpine), for general use. Further details are available on github. As Gliderlabs themselves say, their image “will help you win at minimalism” and it is also an [official docker image](https://docs.docker.com/docker-hub/official_repos/).

We will use of this image in our examples over the rest of this post.

## Size Matters

The size of your containers may not seem that important, but it does matter once you move into production. As the team at Gliderlabs show with the numbers below the difference between a base image of Ubuntu and Alpine Linux is huge.

```bash
REPOSITORY          TAG           IMAGE ID          VIRTUAL SIZE
gliderlabs/alpine   latest        157314031a17      5.03 MB
debian              latest        4d6ce913b130      84.98 MB
ubuntu              latest        b39b81afc8ca      188.3 MB
centos              latest        8efe422e6104      210 MB
```

Now for your initial experiments large base images are fine, but as the number of containers you are using grows size does matter. As a general case think of the distribution of containers in a relatively complex environment, say across 30 nodes, each running 30 instances of a service in two data centers. The numbers add up quickly, and once you are in the realm of multiple deployments
per day so will the bandwidth charges. 

## A Simple Image

Lets create two very simple Docker containers, one based on Alpine Linux, and one based on Ubuntu. Both images provide the same, 
very dumb, php based app which says hello. If you want try this out for yourself, you can download
the source code from [github](https://github.com/fintanr/container-articles). 

Our Dockerfile for the Alpine Linux image is

```
FROM 	gliderlabs/alpine:edge
COPY 	repositories /etc/apk/repositories
RUN 	apk --update add php
RUN 	mkdir /demo
ADD	./demo-src/index.php /demo/index.php
ENTRYPOINT 	["php", "-S", "0.0.0.0:80", "-t", "/demo"]
```

while for Ubuntu it is 

```
FROM    ubuntu
MAINTAINER      fintan@weave.works
RUN     apt-get -y update
RUN     apt-get -y install php5-cli
RUN 	mkdir /demo
ADD	./demo-src/index.php /demo/index.php
ENTRYPOINT ["php", "-S", "0.0.0.0:80", "-t", "/demo"]
```

Now when we build these images we see the following image sizes

```bash
docker build -t fintanr/ubuntu-size-php -f Dockerfile-ubuntu .
docker build -t fintanr/alpine-size-php -f Dockerfile-alpine .
```

## Container Image Size

After our build we get the following images which accomplish the same basic task

```
vagrant@weave-gs-01:~$ docker images | grep fintanr
fintanr/ubuntu-size-php   latest              439cabc52f80        About a minute ago   225.4 MB
fintanr/alpine-size-php   latest              7df8ccc6a40a        About a minute ago   20.14 MB
```

As you can see there is an 11x size difference.

## Container Memory Usage

The other interesting aspect to take note of is the memory usage in the form of RSS and Cache. 
We provide a small python script to look at some basic memory stats.

```bash
vagrant@weave-gs-01:~$ ./dockerRSSUsage.py | grep -v weave
RSS	Cache	Image Name

2.36Mb	0.68Mb	fintanr/alpine-size-php 
3.25Mb	5.27Mb	fintanr/ubuntu-size-php 
```

Again the Alpine image is smaller.

## Conclusion

As we move further into the era of containers how we build our container images will become ever more important.
If you plan on using containers in your environment it is worth considering Alpine Linux or similar as a base to build
upon, or investigate "from scratch" docker images.
