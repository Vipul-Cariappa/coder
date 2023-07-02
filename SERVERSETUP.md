# Server Setup

## Install MariaDB!?

```bash
sudo apt-get install mariadb-server mariadb-client libmariadb-dev -y
```

DB timezone thing

```bash
mysql_tzinfo_to_sql /usr/share/zoneinfo | sudo mysql mysql
```

## Install pandoc

```bash
sudo apt-get install pandoc -y
```
