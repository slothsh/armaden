FROM ubuntu:latest AS build

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update                                                     \
   && apt-get install -y --no-install-recommends --no-install-suggests \
       python3 python3-pip python3-venv

# Install Poetry globally for all users
ENV POETRY_HOME=/opt/poetry
RUN python3 -m venv "$POETRY_HOME"                                  \
    && "$POETRY_HOME/bin/pip" install --no-cache-dir --upgrade pip \
    && "$POETRY_HOME/bin/pip" install --no-cache-dir poetry

ENV PATH="${POETRY_HOME}/bin:${PATH}"

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
ENV POETRY_HOME=/opt/poetry
RUN python3 -m venv "$POETRY_HOME"                                  \
    && "$POETRY_HOME/bin/pip" install --no-cache-dir --upgrade pip \
    && "$POETRY_HOME/bin/pip" install --no-cache-dir poetry

ENV PATH="${POETRY_HOME}/bin:${PATH}"

# Copy build artifacts and give ownership to armaden
RUN mkdir -p /armaden /armaden/dist
COPY --from=build /build/dist /armaden/dist
COPY .env /armaden
RUN chown -R armaden:armaden /armaden && chmod 600 /armaden/.env

# Install game directories
RUN mkdir -p /opt/games/steamcmd /opt/games/arma_reforger \
   && chown -R armaden:armaden /opt/games

# Create writable application storage directories
RUN mkdir -p /armaden/storage/framework \
   && chown -R armaden:armaden /armaden/storage

USER armaden

# Install the Python project as armaden
WORKDIR /armaden
RUN tar -xzf ./dist/*.tar.gz --strip-components=1 && poetry install

# Run server
CMD ["poetry", "run", "armaden-serve"]

