#!/usr/bin/env bash

# This script fetches and extracts Odoo Enterprise source code using the subscription code provided via an environment variable.
# It ensures the Enterprise addons are up-to-date, copying new addons and updating existing ones if necessary.

# Global Variables
readonly ODOO_VERSION="${ODOO_VERSION:-17.0}"
readonly ODOO_SUBSCRIPTION_CODE="${ODOO_SUBSCRIPTION_CODE:-}"

# Helper Functions

##
# Logs messages to stdout with a timestamp and message type.
# Globals:
#   None
# Arguments:
#   $1: The type of message (INFO, ERROR, etc.)
#   $2: The message text
# Returns:
#   None
log_message() {
    local type="$1"
    shift
    local message="$*"
    echo "$(date '+%Y-%m-%d %H:%M:%S') [$type] $message"
}

##
# Downloads and extracts Odoo Enterprise addons, updating them as needed.
# Globals:
#   ODOO_SUBSCRIPTION_CODE
#   ODOO_VERSION
# Arguments:
#   None
# Returns:
#   None
fetch_odoo_enterprise() {
    if [[ -z "${ODOO_SUBSCRIPTION_CODE}" ]]; then
        log_message "ERROR" "ODOO_SUBSCRIPTION_CODE environment variable is not set."
        exit 1
    fi

    if [ ! -f /opt/odoo/enterprise/__init__.py ]; then
        log_message "INFO" "Fetching Odoo Enterprise..."
        local enterprise_download_url
        enterprise_download_url=$(curl -s "https://www.odoo.com/thanks/download?code=${ODOO_SUBSCRIPTION_CODE}&platform_version=src_${ODOO_VERSION%%.*}e" \
            | grep -oP "(https:\/\/download\.odoocdn\.com\/download\/\d+e\/src\?payload=[A-Za-z0-9]+)" | head -n 1)

        if [[ -n ${enterprise_download_url} ]]; then
            log_message "INFO" "Downloading Enterprise source from ${enterprise_download_url}..."
            curl -sS -o /tmp/odoo-enterprise.tar.gz -L "${enterprise_download_url}"

            log_message "INFO" "Extracting Odoo Enterprise..."
            mkdir -p /tmp/odoo /opt/odoo/enterprise/
            if ! tar -xzf /tmp/odoo-enterprise.tar.gz --strip-components=1 -C /tmp/odoo; then
                log_message "ERROR" "Failed to extract Odoo Enterprise archive."
                exit 1
            fi

            update_enterprise_addons "/tmp/odoo/odoo/addons" "/opt/odoo/enterprise"
            
            log_message "INFO" "Cleaning up temporary files..."
            rm -rf /tmp/odoo /tmp/odoo-enterprise.tar.gz
            sudo chown -R 101:101 /opt/odoo/enterprise
            log_message "INFO" "Odoo Enterprise addons are up-to-date."
        else
            log_message "ERROR" "No valid Odoo Enterprise download URL found. Please check the subscription code (env:ODOO_SUBSCRIPTION_CODE) or try again later."
            exit 1
        fi
    else
        log_message "INFO" "Odoo Enterprise is already present. Skipping download."
    fi
}

##
# Updates Odoo Enterprise addons by comparing and copying necessary addon files.
# Globals:
#   None
# Arguments:
#   $1: The source directory of the Enterprise addons
#   $2: The target directory of the Enterprise addons
# Returns:
#   None
update_enterprise_addons() {
    local source_dir="$1"
    local target_dir="$2"

    for addon in "$source_dir"/*/; do
        local addon_name
        addon_name=$(basename "$addon")
        local target_addon="${target_dir}/${addon_name}"
        local source_manifest="${addon}__manifest__.py"
        local target_manifest="${target_addon}/__manifest__.py"

        # Ensure the addon directory exists at the target
        if [ ! -d "${target_addon}" ]; then
            log_message "INFO" "Copying new Enterprise addon ${addon_name}..."
            cp -a "${addon}" "${target_addon}"
            continue
        fi

        # Check if the manifest file is different or missing, copy the whole addon if it is
        if [ ! -f "${target_manifest}" ] || ! diff -q "${source_manifest}" "${target_manifest}"; then
            log_message "INFO" "Updating Enterprise addon ${addon_name}..."
            rm -rf "${target_addon}"
            cp -a "${addon}" "${target_addon}"
        fi
    done
}

##
# Enale the addon in the odoo configuration file
# Globals:
#   None
# Arguments:
#   None
# Returns:
#   None
enable_enterprise_addons() {
    docker exec -it odoo-addon-salutation_devcontainer-odoo-1 /bin/bash -c '
    log_message() {
        local level="$1"
        local message="$2"
        echo "[$level] $message"
    }

    enable_enterprise_addons() {
        local addons_path="/opt/odoo/enterprise"
        local odoo_conf="/etc/odoo/odoo.conf"

        if [ -f "${odoo_conf}" ]; then
            log_message "INFO" "Enabling Odoo Enterprise addons..."
            local addons
            addons=$(find "${addons_path}" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | paste -sd, -)
            sed -i "s|^addons_path = .*|addons_path = /mnt/extra-addons,${addons_path}|" "${odoo_conf}"
        else
            log_message "ERROR" "Odoo configuration file not found at ${odoo_conf}."
            exit 1
        fi
    }

    enable_enterprise_addons
    '
}

# Main script execution
fetch_odoo_enterprise