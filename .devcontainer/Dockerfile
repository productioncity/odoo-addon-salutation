# Use the odoo:17 image as the base
FROM odoo:17

# Switch to the root user
USER root

# Install necessary tools and dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get install -y \
    sudo \
    vim \
    git \
    curl \
    wget \
    git \
    less \
    unzip \
    zsh

# Create the vscode user and add to sudoers
RUN useradd -m -s /bin/zsh vscode \
    && echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Set environment variables for user and group
ENV USER=vscode
ENV HOME=/home/vscode

# Set the working directory
WORKDIR /home/vscode

# Switch to the vscode user
USER vscode

# [Optional] Install Python packages if needed
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# Set the default command
CMD ["sleep", "infinity"]
