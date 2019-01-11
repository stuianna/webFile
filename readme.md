# Introduction

Webfile can be used to send single files, with username / password authentication to recipients through a standard web browser HTTPS protocol.

It consists of a server running with the [Bottle web framework](https://bottlepy.org/docs/dev/) and automated SSH server with remote port forwarding to [Serveo](https://serveo.net/), which in turn hosts the public URL.


Please respect the free service provided by [Serveo](https://serveo.net/) and use this application conservatively. A accept no responsibility for the contents of the files sent through this application.

# Installation

WebFile is build for Linux based distributions only and assumes [ssh](https://www.ssh.com/ssh/command/) is available.

The binary can be obtained using wget:
```
wget https://github.com/stuianna/webFile/releases/download/v0.1.0/ucConfig
```

Or the source can be downloaded and build using the instructions below.
```
git clone https://github.com/stuianna/webFile.git
```

Place the binary or link to binary in a directory which forms part of your PATH variable for convenience.

# Usage

Let's say you want to transfer a file 'hairyKnees.jpg' to a friend who's making an add for a new razor, the picture is super hi-def so you can't send it via email and neither of you use the same cloud hosting service.

To transfer the file using webFile with a given username [-u] and password [-p], from the command line run:
```
webFile /path/to/hairyKnees.jpg -u example -p 1234
```

The Bottle WSGI server will start and port forwarding will begin on port 8142, the following output will be written to stdout:
```
Bottle v0.12.16 server starting up (using WSGIRefServer())...
Listening on http://0.0.0.0:8142/
Hit Ctrl-C to quit.

Hi there
Forwarding HTTP traffic from https://****.serveo.net
Press g to start a GUI session and ctrl-c to quit.
```

The HTTP address given ```https://****.serveo.net``` will have the '*' replaced by a randomly generate word. Send the address to your friend along with the username and password you specified in the command line arguments.

The reciever of the file can then browse to the http address supplied, login with their crediential and the file download will begin automatically.

The close the server, press CTRL+C

# Build Instructions

PyInstaller is used to build generate a single file executable.

To use pyInstaller:

1. From the main python directory run:
```
pyi-makespec webFile.py -n webFile --onefile
```

2. Inside ucConfig_linux.spec change:
```
datas=[]
```
to
```
datas=[('static','static')],
```
3. From the main directory run:
```
pyinstaller webFile.spec
```
The binary is now located in the 'dist' directory.
