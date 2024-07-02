# odoo-addon-salutation
Add's salutation, given name, family name to Contacts

## Init Odoo

```bash
odoo --database=odoo --db_user=${USER} --db_password=${PASSWORD} --db_host=postgres --db_port=5432 --stop-after-init --no-http -i base,contacts
```

## Reload addon

```bash
odoo --database=odoo --db_user=${USER} --db_password=${PASSWORD} --db_host=postgres --db_port=5432 --stop-after-init --no-http -d odoo -u salutation
```