# Odoo Salutation Fieds

This Odoo 17 addon enhances the Contacts module by introducing fields for salutation, given name, and family name. This facilitates better categorisation and personalisation of contact records.

## Features

- **Salutation**: Adds a field for the salutation (title) of a contact.
- **Given Name**: Adds a field for the given name (first name) of a contact.
- **Family Name**: Adds a field for the family name (surname) of a contact.
- **Manual Overrides**: Allows manual overrides for each above-mentioned field.

## Installation

### Step 1: Add the Addon to Your Odoo Addons

1. **Clone the Repository**
    ```bash
    git clone https://github.com/productioncity/odoo-addon-salutation.git
    ```

2. **Copy the Addon to Your Odoo Addons Directory**
    ```bash
    cp -r odoo-addon-salutation /path/to/your/odoo/addons/
    ```

3. **Update Your Odoo Configuration File**  
   Ensure that the addons path in your `odoo.conf` includes the path to the new addon:
    ```ini
    [options]
    addons_path = /path/to/your/odoo/addons
    ```

### Step 2: Load and Activate the Addon

1. **Start Odoo**  
   Start your Odoo server if it is not already running.
   ```bash
   odoo
   ```

2. **Activate the Addon**
   - Go to the Odoo main dashboard.
   - Navigate to the Apps menu and click on **Update App List**.
   - Search for the `salutation` addon.
   - Click **Install**.

## Usage

### Automatic and Manual Name Parts Management

- **Automatic Population**: The addon automatically populates the given name, family name, and salutation based on the contact name.
- **Manual Overrides**: You can manually set the given name, family name, or salutation, which prevents automatic updates to these fields.

### Updating Existing Contacts

To update existing contacts with the new fields, follow these steps:

1. **Backup Your Database**  
   **Warning**: This operation will update your database. Ensure you take a backup of your database before proceeding. All care taken, no responsibility accepted for any data loss or issues.

2. **Update Existing Contacts**
    - Run the following command to launch Odoo in shell mode:
    ```bash
    odoo shell --database=your_database_name
    ```

    - In the Odoo shell, run:
    ```python
    env['res.partner'].sudo()._update_existing_contacts()
    ```

    - To exit the shell, run:
    ```python
    exit()
    ```

## Development

### Cloning and Working on the Code

1. **Fork the Repository**  
   Fork the repository to your GitHub account.

2. **Clone Your Fork**  
   Clone the forked repository to your local machine:
    ```bash
    git clone https://github.com/your-username/odoo-addon-salutation.git
    cd odoo-addon-salutation
    ```

3. **Create a Feature Branch**  
   Create and switch to a new feature branch for your changes:
   ```bash
   git checkout -b my-feature-branch
   ```

### Benefits of Our Dev Container

We provide a `.devcontainer` configuration for Visual Studio Code, which streamlines the development process by setting up a consistent development environment with all necessary tools and dependencies:

- **Consistent Environment**: Guarantees that all developers work within the same environment, reducing "works on my machine" issues.
- **Pre-installed Tools**: Includes tools like Python, Docker, Git, and other utilities pre-installed.
- **Zsh Shell**: Configures Zsh with useful plugins for an enhanced terminal experience.

#### Developing with Dev Containers

1. **Open the Project in Visual Studio Code**  
   Ensure you have the [Dev Containers](https://code.visualstudio.com/docs/remote/containers) extension installed.

2. **Reopen the Project in Container**  
   When prompted, reopen the project in the container.

3. Get a shall in the Odoo container

```zsh
docker exec -it odoo-addon-salutation_devcontainer-odoo-1 /bin/bash
```

4. Initialise the Odoo instance (in the container shell)

Add "marketing_automation" at the end if you are using it.

```bash
odoo --database=odoo --db_user=${USER} --db_password=${PASSWORD} --db_host=${HOST} --db_port=5432 --stop-after-init --no-http -i base,contacts
exit
```

4. Restart Odoo

```zsh
docker restart odoo-addon-salutation_devcontainer-odoo-1
```

##### Changes

If you change the addon and want to test it locally.

1. Get a shall in the Odoo container

```zsh
docker exec -it odoo-addon-salutation_devcontainer-odoo-1 /bin/bash
```

2. Then, in the container update the addon

```bash
odoo --database=odoo --db_user=${USER} --db_password=${PASSWORD} --db_host=${HOST} --db_port=5432 --stop-after-init --no-http -u salutation
exit
```

3. Then restart odoo

```zsh
docker restart odoo-addon-salutation_devcontainer-odoo-1
```

##### Odoo Shell in Odoo Container

1. Get a shall in the Odoo container

```zsh
docker exec -it odoo-addon-salutation_devcontainer-odoo-1 /bin/bash
```

2. Then, in the container update the addon

```bash
odoo shell --database=odoo --db_user=${USER} --db_password=${PASSWORD} --db_host=postgres --db_port=5432 --stop-after-init --no-http
```

### Contributing

We welcome contributions to improve this addon. Please follow these steps to contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push the branch to your fork.
5. Create a pull request.

## Support

For any issues or feature requests, please create an issue [here](https://github.com/productioncity/odoo-addon-salutation/issues).

## License

This project is licensed under the OPL-1 License. See the [LICENSE](LICENSE) file for more details.