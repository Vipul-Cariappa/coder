# coder

### Install instructions for development
fork the repository first
```bash
git clone git@github.com:<Your-Username>/coder.git
cd coder
python3 -m venv venv
source ./venv/bin/activate # for linux / macos
./venv/Scripts/activate # for windows
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
