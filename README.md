# Miq Selenium Server

This is a simple script to make my life easy.
As I want to run `selenium server` `locally` but don't want to use `wharf`.
I don't want to check docker `ip's` and `ports`;
I want to overwrite to my `env.ymal`.
I want to select my `browser` with a single command.
Simple command line application should spin selenium docker container
and give me `vnc` access and solve my problems.
 

## Prerequisite:
1. **Docker**:

    I think you have a `docker` environment already setup. if not you can follow. 

    - [fedora](https://developer.fedoraproject.org/tools/docker/docker-installation.html)
    
        * set repo
        ```
        sudo dnf -y install dnf-plugins-core
        sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
        ```
    
        * Install
    
        ```
        sudo dnf -y install docker-ce
        sudo systemctl start docker
        sudo systemctl enable docker
        ```
        
        * Non root-user
        ```
        sudo usermod -aG docker <your-user-name>
        ```
    
    - [ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/) and [others](https://docs.docker.com/install/)

2. **TigerVNC**:
    - Fedora:
        ```
        sudo dnf install tigervnc
        ```
    - [Other:](http://tigervnc.bphinz.com/nightly/)


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
  --help  Show this message and exit.

Commands:
  browser   Set Browser
  config    Configure Miq Selenium webdriver
  hostname  Miq Selenium Server Hostname
  start     Start Miq Selenium Server
  status    Status of Miq Selenium Server
  stop      Stop Miq Selenium Server
```
- **Note**: If the project directory `not set` then you need to run commands from `integration_tests` directory. 

* set-project-directory:
    ```
    cd `<path>/integration_tests`
    miqsel config
    # fallow options
    ```
