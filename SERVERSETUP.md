# Server Setup

## Install MariaDB!?

```bash
sudo apt-get install mariadb-server mariadb-client libmariadb-dev pkg-config -y
```

DB timezone thing

```bash
mysql_tzinfo_to_sql /usr/share/zoneinfo | sudo mysql mysql
```

Create DataBase

```bash
CREATE DATABASE <database-name> CHARACTER SET utf8;
```

## Move DataBases!?

> Do Not Do This But

Store data in a JSON file

```bash
python manage.py dumpdata > data.json
```

Load data

```bash
python manage.py loaddata data.json
```

## Install pandoc

```bash
sudo apt-get install pandoc -y
```

## Using letsencrypt

Install dependency

```bash
sudo apt install certbot python3-certbot-nginx -y
```

Generate certificate and associate it

```bash
sudo certbot --nginx -d <example.com>
```

Auto renew the certificate
```bash
sudo systemctl status certbot.timer
sudo certbot renew --dry-run        # test if auto renewal works
```
