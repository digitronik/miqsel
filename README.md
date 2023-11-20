<h1 align="center"> miqsel</h1>
<h3 align="center">Miq Selenium Server</h3>

<p align="center">
<a href="https://pypi.org/project/miqsel"><img alt="Python Versions"
src="https://img.shields.io/pypi/pyversions/miqsel.svg?style=flat"></a>
<a href="https://github.com/digitronik/miqsel/actions?query=workflow%3A%22%F0%9F%95%B5%EF%B8%8F+Test+suite%22"><img alt="Build Status"
src="https://github.com/digitronik/miqsel/workflows/%F0%9F%95%B5%EF%B8%8F%20Test%20suite/badge.svg"></a>
<a href="https://github.com/digitronik/miqsel/blob/master/LICENSE"><img alt="License: GPLV3"
src="https://img.shields.io/pypi/l/miqsel.svg?version=latest"></a>
<a href="https://pypi.org/project/miqsel/#history"><img alt="PyPI version"
src="https://badge.fury.io/py/miqsel.svg"></a>
<a href="https://pepy.tech/project/miqsel"><img alt="Downloads"
src="https://pepy.tech/badge/miqsel"></a>
<a href="https://pypi.org/project/black"><img alt="Code style: black"
src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

`miqsel` is a Python CLI utility leaveraging a Selenium container image to efficiently manage a
`selenium server` and provide `vnc` access.


### Prerequisite:
1. **Podman/Docker**:

    Make sure `podman` or `docker` running on your system.
    - [Podman Installation](https://podman.io/getting-started/installation.html)
    - [Docker Installation](https://docs.docker.com/engine/install/)

2. **VNC Viewer**:

    You can choose any vnc viewer but most of user used _tigervnc_.
    - Fedora:
        ```
        sudo dnf install tigervnc
        ```
    - [TigerVNC link for other Distro's](http://tigervnc.bphinz.com/nightly/)

### Installation:
```bash
pip install miqsel --user
```
or
```bash
 pip install git+https://github.com/digitronik/miqsel#egg=miqsel --user
```

## Usage:
- **Help**:
    ```shell
    ❯❯❯ miqsel --help
    Usage: miqsel [OPTIONS] COMMAND [ARGS]...

      Miq Selenium Server

    Options:
      --version  Show the version and exit.
      --help     Show this message and exit.

    Commands:
      config    Set Configuration
      executor  Selenium executor URL
      start     Start Selenium Server
      status    Status of Selenium Server
      stop      Stop Selenium Server
      viewer    VNC viewer
      vnc       VNC URL
    ```

- **Status**:
Check status of selenium container (running/ stopped).
    ```shell
    ❯❯❯ miqsel status
    stopped
    ```

- **Start/Stop**:
    ```shell
    ❯❯❯ miqsel start
    Selenium Server started

    TigerVNC Viewer 64-bit v1.9.0

    ❯❯❯ miqsel stop

    Sun Apr 28 12:29:02 2019
     CConn:       End of stream
    Selenium Server stopped
    ```
    Note: `start` default invoke `vnc-viewer`. You can stop it like `miqsel start --no-viewer`

- **Viewer**:
Take `vnc` access of selenium server. At the start of selenium server, vnc viewer will be `invoked` automatically.
If the `status` is `running` and the `viewer` is `close` then viewer command will help to re-open vnc session.

    ```shell
    ❯❯❯ miqsel status
    running
    ❯❯❯ miqsel viewer
    TigerVNC Viewer 64-bit v1.9.0
    ```

- **Executor**:
Get command executor url
    ```shell
    ❯❯❯ miqsel executor
    http://172.17.0.2:4444/wd/hub
    ```

- **VNC**:
Get vnc session url
    ```shell
    ❯❯❯ miqsel vnc
    172.17.0.2:5999
    ```

- **Configuration**:
    Manage your miqsel configuration and change default setting as per need.
    ```shell
    ❯❯❯ miqsel config
    Container Engine (auto, podman, docker) [auto]:
    Selenium container image [selenium/standalone-chrome:latest]:
    VNC viewer (auto, vncviewer, vinagre, xdg-open) [auto]:
    Selenium server running on port? [4444]:
    VNC running on port? [5999]:
    Selenium container name [miqsel_container]:
    Selenium container network [default]:
    Selenium container shared Memory [2g]:
    Testing data mount to directory '/data' [default]:
    Configuration saved successfully...
    ```

    `selenium/standalone-chrome:latest` is default image. You can use other from [SeleniumHQ](https://github.com/SeleniumHQ/docker-selenium) or custom images.
