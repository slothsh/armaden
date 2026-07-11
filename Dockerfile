FROM ubuntu:latest AS build

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update                                                     \
   && apt-get install -y --no-install-recommends --no-install-suggests \
       python3 python3-pip python3-venv

# Install Poetry globally for all users
RUN pip3 install --break-system-packages poetry

# Copy library source and build
RUN mkdir -p /build
COPY . /build
WORKDIR /build
RUN poetry install --no-interaction --no-ansi && poetry build

FROM ubuntu:latest AS production

ENV DEBIAN_FRONTEND=noninteractive

# Create the user first
RUN usermod -l armaden ubuntu         \
    && groupmod -n armaden ubuntu     \
    && usermod -d /armaden -m armaden

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

# Copy build artifacts and give ownership to armaden
RUN mkdir -p /armaden /armaden/dist
COPY --from=build /build/dist /armaden/dist
COPY .env /armaden
COPY ./user /armaden/user
RUN chown -R armaden:armaden /armaden && chmod 600 /armaden/.env

# Install steamcmd directories
RUN mkdir -p /opt/games/steamcmd /opt/games/arma                   \
   && chown -R armaden:armaden /opt/games/steamcmd /opt/games/arma

USER armaden

# Install the Python project as armaden
WORKDIR /armaden
RUN tar -xzf ./dist/*.tar.gz --strip-components=1 && poetry install

# Run server
CMD ["poetry", "run", "armaden-serve"]
