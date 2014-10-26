IyE
===

Development
---

1. Clone this repository:
 ```
 https://github.com/cdvr1993/IyE.git
 ```
 
1. Install the virtual environment dependencies:
 1. On Ubuntu:

   ```
   sudo apt-get install python-pip python-dev build-essential
   sudo pip install --upgrade pip
   sudo pip install --upgrade virtualenv
   ```
 1. On Archlinux:
 
   ```
   sudo pacman -S python-virtualenv
   ```
 
1. Inside the project's directory, run the following to create the virtual environment:
 ```
 virtualenv .venv
 ```
 
1. Activate the virtual environment:
 ```
 . .venv/bin/activate
 ```
 
1. Install the project's dependencies:
 ```
 pip install -r requirements.txt
 ```
 
Deploy to Openshift (tornado server)
---

1. First you need to create a new project using the "Do it Yourself" cartridge.
1. Then you need to install python 3.
 ```
 wget http://www.python.org/ftp/python/3.3.5/Python-3.3.5.tar.xz
 tar xJf ./Python-3.3.5.tar.xz
 cd ./Python-3.3.5
 ./configure --prefix={INSTALL_PATH}
 make && sudo make install
 ```

1. Then copy the manage.py file to a new onew named "manage_openshift.py".
1. Then edit the listen line (the "DIY" is the project's name):
 ```
 server.listen(os.environ['OPENSHIFT_DIY_PORT'], os.environ['OPENSHIFT_DIY_IP'])
 ```
 
1. Finally you need to edit the start and stop scripts under "{REPO_DIR}/.openshift/action_hooks":
 1. Start
  ```
  #!/bin/bash
  nohup ${OPENSHIFT_REPO_DIR}/diy/IyE/manage_openshift.py > ${OPENSHIFT_DIY_LOG_DIR}/iye.log 2>&1 &
  ```
  
 1. Stop
  ```
  #!/bin/bash
  kill `ps -ef | grep manage | grep -v grep | awk '{ print $2 }'` > /dev/null 2>&1
  exit 0
  ```
