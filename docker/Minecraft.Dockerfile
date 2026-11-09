FROM ubuntu:latest AS build

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update                                                     \
   && apt-get install -y --no-install-recommends --no-install-suggests \
       python3 python3-pip python3-venv

ENV POETRY_HOME=/opt/poetry
RUN python3 -m venv "$POETRY_HOME"                                  \
    && "$POETRY_HOME/bin/pip" install --no-cache-dir --upgrade pip \
    && "$POETRY_HOME/bin/pip" install --no-cache-dir poetry

ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN mkdir -p /build
COPY . /build
WORKDIR /build
RUN poetry install --no-interaction --no-ansi && poetry build

FROM ubuntu:latest AS production

ENV DEBIAN_FRONTEND=noninteractive

RUN usermod -l armaden ubuntu         \
    && groupmod -n armaden ubuntu     \
    && usermod -d /armaden -m armaden

RUN apt-get update                                                     \
   && apt-get install -y --no-install-recommends --no-install-suggests \
       ca-certificates python3 python3-pip python3-venv                \
   && apt-get remove --purge -y                                        \
   && apt-get clean autoclean                                          \
   && apt-get autoremove -y                                            \
   && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME=/opt/poetry
RUN python3 -m venv "$POETRY_HOME"                                  \
    && "$POETRY_HOME/bin/pip" install --no-cache-dir --upgrade pip \
    && "$POETRY_HOME/bin/pip" install --no-cache-dir poetry

ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN mkdir -p /armaden /armaden/dist
COPY --from=build /build/dist /armaden/dist

COPY user /armaden/user

RUN chown -R armaden:armaden /armaden

RUN mkdir -p /opt/games/minecraft \
   && chown -R armaden:armaden /opt/games

RUN mkdir -p /armaden/storage/framework \
   && chown -R armaden:armaden /armaden/storage

USER armaden

WORKDIR /armaden
RUN tar -xzf ./dist/*.tar.gz --strip-components=1 && poetry install

CMD ["poetry", "run", "armaden-serve"]
