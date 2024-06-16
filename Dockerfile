#######################
# Base image
#######################
FROM python:3.12-slim-bookworm AS deps

ARG RUNAS_UID=1000

RUN useradd -m -u $RUNAS_UID -N billy
WORKDIR /home/billy

ENV PYTHONUNBUFFERED=1 \
    # Poetry
    POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    VIRTUAL_ENV="/home/billy/env"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENV/bin:$PATH"

RUN mkdir -p /var/log/supervisord
RUN chown -R billy:users /var/log/supervisord

RUN apt-get update \
    && apt-get install -y curl pkg-config libxml2-dev libxmlsec1-dev libxmlsec1-openssl gcc \
    && apt clean -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/man/?? /usr/share/man/??_*

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | python -

USER billy
RUN python -m venv $VIRTUAL_ENV
ENV PYTHONPATH="/home/billy:$PYTHONPATH"

CMD bash

#######################
# Development image
#######################
FROM deps AS dev

ENV APP_EXEC_MODE_RUNSERVER=1

# Needed for pre-commits
USER root
RUN apt-get update \
    && apt-get install -y git vim \
    && apt clean -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/man/?? /usr/share/man/??_*
USER billy

COPY --chown=billy:users ./pyproject.toml ./poetry.lock ./

RUN poetry install --no-root

COPY --chown=billy:users ./ ./billy_project
COPY --chown=billy:users supervisord.conf ./supervisord.conf

RUN mkdir -p /var/log/supervisord
RUN chown -R billy:users /var/log/supervisord
RUN chown -R billy:users /home/billy/billy_project/run-app.sh
RUN chmod +x /home/billy/billy_project/run-app.sh

CMD supervisord -c /home/billy/supervisord.conf
