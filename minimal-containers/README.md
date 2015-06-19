## Introduction

At Weave, we, as you would expect, distribute all of our software as containers, and make heavy use of both Alpine Linux and the ability to build a container “from scratch”.

When you first experiment with Docker many of the initial examples you come across are based on Ubuntu, Debian and other full Linux distributions. Indeed we provide similar examples in our own getting started guides. 

This approach of building from a full distribution is, however, less than optimal. In this post we will cover why you should consider using a minimal distribution such as Alpine Linux for your containers, and provide a number of simple examples. 

## Background

Firstly let us step back a little bit from distributions and consider the purpose of containers. At their simplest level containers use various kernel facilities, such as cgroups and namespaces, to provide resource and process isolation. Unlike a virtual machine, and in spite of the examples, containers do not require a complete, or, depending on the circumstances, any, operating system.

However, an operating system does provide very useful primitives, particularly in terms of packaging and distributing software. Given this it make sense to use operating systems as the basis for our containers in most cases and for most users.

The question, which arises, is just how much of the operating system infrastructure and internal plumbing you really need to allow your application to run. The answer, generally, is not very much and reducing the overall footprint of an operating system is a good security practice.  Given this, starting from a very small footprint and adding in the components you need is preferable to removing components from a larger distribution.

## Introducing Alpine Linux

Alpine Linux is a lightweight, secure by default, Linux distribution with a simple, and up to date set of packages for use. It is intended for general-purpose use, and more importantly has a design principle of trying to stay out of your way.

Gliderlabs have developed an “Alpine Linux Docker Image”, for general use. Further details are available on github. As Gliderlabs themselves say, their image “will help you win at minimalism” and it is also an official docker image. (https://docs.docker.com/docker-hub/official_repos/)

We will use of this image in our examples over the rest of this post.

## Size Matters

The size of your containers may not seem that important, but it does matter. As the team at Gliderlabs show with the numbers below the difference between a base image of Ubuntu and Alpine Linux is huge.

<< details from  gliderlabs github page >>

Now for your initial experiments large base images are fine, but as the number of containers you are using grows size does matter.  As a general case think of the distribution of containers in a relatively complex environment, say across 30 nodes, each running 30 instances of a service in two data centers. 



All the code from this example is available at





## From Scratch



