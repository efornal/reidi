# reidi
It allows managing sub-domain requests from a previously specified root URL

### Package Installation debian stretch
```bash
sudo apt-get install python-dev
sudo apt-get install python-pip
sudo apt-get install libpq-dev
sudo apt-get install libyaml-dev
sudo apt-get install libldap2-dev
sudo apt-get install libsasl2-dev
sudo apt-get install gettext
sudo apt-get install libjpeg-dev
sudo apt-get install zlib1g-dev
sudo apt-get install python-dnspython # for reidi
sudo apt-get install mariadb-client # for dumpserver
sudo apt-get install pkg-config
sudo apt-get install libgtk2.0-dev
sudo apt-get install libgirepository1.0-dev
```

### Python lib Installation
```bash
pip install -r requirements.txt
```

# permisos en postgres para reidi_user
```bash
# up
GRANT ALL ON ALL TABLES IN SCHEMA public TO reidi_user;
# down
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM reidi_user;


#up
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO reidi_user;
#down
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM reidi_user;

```