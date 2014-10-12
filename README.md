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
 
