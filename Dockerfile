FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

# Create the steam user first
RUN useradd -m steam

# Install system dependencies
RUN apt-get update                                                     \
   && apt-get install -y --no-install-recommends --no-install-suggests \
       lib32gcc-s1 software-properties-common                          \
       binutils curl wget ca-certificates                              \
       python3 python3-pip python3-venv                                \
   && apt-get remove --purge -y                                        \
   && apt-get clean autoclean                                          \
   && apt-get autoremove -y                                            \
   && rm -rf /var/lib/apt/lists/*

RUN dpkg --add-architecture i386 && add-apt-repository multiverse && apt-get update

# Install Poetry globally for all users
RUN pip3 install --break-system-packages poetry

# Copy library source and give ownership to steam
COPY pyproject.toml poetry.lock README.md /opt/armaden/
COPY src /opt/armaden/src
RUN chown -R steam:steam /opt/armaden

# Install steamcmd directories
RUN mkdir -p /steamcmd /arma               \
   && chown -R steam:steam /steamcmd /arma

# Switch to steam user for all remaining operations
USER steam

# Install the Python project as steam
WORKDIR /opt/armaden
RUN poetry install --no-interaction --no-ansi

# Install steamcmd as steam
WORKDIR /steamcmd
RUN wget -qO- "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz" | tar zxvf -

# User application directory
ENV APP_DIR=/app

# Volumes
VOLUME /steamcmd
VOLUME /arma
VOLUME /app

# Run server
WORKDIR /opt/armaden
CMD ["poetry", "run", "armaden-serve"]
