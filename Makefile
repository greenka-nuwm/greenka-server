# Makefile to deploy greenka application.

CERT_NAME = greenka
CERT_FOLDER = certs
CERT_KEY = $(CERT_NAME).key
CERT_CERT = $(CERT_NAME).cert

CERT_TARGET = /etc/apache2/certs

APACHE_USER = www-data
APACHE_CONF = apache-greenka.conf
APACHE_ETC = /etc/apache2

all: install

certificates: 
ifeq ($(and $(wildcard $(CERT_TARGET)),\
       	$(wildcard $(CERT_TARGET)/$(CERT_KEY)),\
       	$(wildcard $(CERT_TARGET)/$(CERT_CERT))),)
	# check if there are installed certs in apache
	@echo 'not found certificates in apache conf directory: $(CERT_TARGET)'
	@mkdir -p $(CERT_TARGET)

	# check for local certs
ifeq ($(and $(wildcard certs/$(CERT_KEY)), $(wildcard certs/$(CERT_CERT))),)
	@echo "generating certs..."
	@mkdir -p certs
	openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
	    -subj "/C=UA/ST=Lviv/L=Lviv/O=Dis/CN=greenka" \
	    -keyout certs/$(CERT_NAME).key  -out certs/$(CERT_NAME).cert
endif
	
	@echo "installing certs from local"
	@cp -r certs/$(CERT_NAME)* $(CERT_TARGET)
	@chown -R $(APACHE_USER):$(APACHE_USER) $(CERT_TARGET)
	

endif

install-apache-conf:
	@echo "installing apache configuration"
	@ln -sfn /opt/greenka/$(APACHE_CONF) $(APACHE_ETC)/conf-enabled/$(APACHE_CONF)

install-source:
	@echo "installing greenka source"
	@./manage.py collectstatic
	@mkdir -p /opt/greenka
	@cp -r * /opt/greenka/.
	@chmod -r $(APACHE_USER):$(APACHE_USER) /opt/greenka

install: certificates install-source install-apache-conf 

migrate:
	@./manage.py migrate
