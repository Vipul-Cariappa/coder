# Code Turing

Code Turing aims to be a website where people can learn how to program. It is similar to a competitive programming website. But need not be limited to it. I have many ideas in my mind for this.

You can find the deployed site at https://codeturing.in/.

Code Turing name is derived from Alan Turing. One of the greatest minds in the field of Computer Science and Mathematics.

## Install instructions for development

Requires Python 3.10 or newer (tested on 3.14) and Django 5.2 LTS.

Install the `pandoc` binary from [here](https://github.com/jgm/pandoc/releases). The
`pandoc` Python package (2.4) knows the document models up to pandoc **3.2.1**, so use a
release at or below that — a newer binary only prints a warning and is treated as 3.2.1,
which is not guaranteed to be correct.

fork the repository first

```bash
git clone git@github.com:<Your-Username>/coder.git
cd coder
python3 -m venv venv
source ./venv/bin/activate # for linux / macos
./venv/Scripts/activate # for windows
pip install -r requirements.txt
cp info.json server_info.json
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

This project uses `server_info.json` file for configurations. If you want to test it with different configurations like changing the database, edit the `info.json` and rename it to `server_info.json`.

Use `db.cnf` to configure the database you want to use. Rename `db.cnf` to `server_db.cnf` after you are done with your edits. By default, this project uses SQLite database while developing. And MariaDB in production.


Using `black` and `djlint` for formatting.
