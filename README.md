<h1 align="center"> miqsel</h2>
<h3 align="center">Miq Selenium Server</h3>

<p align="center">
<a href="https://pypi.org/project/miqsel"><img alt="Python Versions"
src="https://img.shields.io/pypi/pyversions/miqsel.svg?style=flat"></a>
<a href="https://travis-ci.org/digitronik/miqsel"><img alt="Build Status"
src="https://travis-ci.org/digitronik/miqsel.svg?branch=master"></a>
<a href="https://github.com/digitronik/miqsel/blob/master/LICENSE"><img alt="License: GPLV3"
src="https://img.shields.io/pypi/l/miqsel.svg?version=latest"></a>
<a href="https://pypi.org/project/miqsel/#history"><img alt="PyPI version"
src="https://badge.fury.io/py/miqsel.svg"></a>
<a href="https://pepy.tech/project/miqsel"><img alt="Downloads"
src="https://pepy.tech/badge/miqsel"></a>
<a href="https://pypi.org/project/black"><img alt="Code style: black"
src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

Simple command line application to spin [`selenium docker container`](https://hub.docker.com/r/cfmeqe/cfme_sel_stable) and provide `vnc` access.


## Prerequisite:
1. **Docker**:

    For setting `docker` environment follow below steps:

    - [Fedora](https://developer.fedoraproject.org/tools/docker/docker-installation.html)
    
        * Set Repository:
        ```
        sudo dnf -y install dnf-plugins-core
        sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
        ```
    
        * Install below packages:
    
        ```
        sudo dnf -y install docker-ce
        sudo systemctl start docker
        sudo systemctl enable docker
        ```
        
        * Run docker with non-root User:
        ```
        sudo groupadd docker
        sudo usermod -aG docker <non-root-user>
        ```
    
    - [Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/) and [others](https://docs.docker.com/install/)

2. **TigerVNC Versions(based on various Distro's)**:
    - Fedora:
        ```
        sudo dnf install tigervnc
        ```
    - [TigerVNC link for other Distro's](http://tigervnc.bphinz.com/nightly/)



## Installation:
```bash
pip install miqsel --user
```
or
```bash
 pip install git+https://github.com/digitronik/miqsel#egg=miqsel --user
```

## Usage:
```
Usage: miqsel [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  browser   Set Browser
  config    Configure Miq Selenium webdriver
  hostname  Miq Selenium Server Hostname
  start     Start Miq Selenium Server
  status    Status of Miq Selenium Server
  stop      Stop Miq Selenium Server
  urls      VNC and Command Executor URL's
  viewer    VNC viewer
```
- **Note**: If the project directory `not set` then you need to run commands from `integration_tests` directory. 

* set-project-directory:
    ```
    cd `<path>/integration_tests`
    miqsel config
    # follow options
    ```
