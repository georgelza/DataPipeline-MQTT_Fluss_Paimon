
FROM arm64v8/flink:1.20.1-scala_2.12-java17
SHELL ["/bin/bash", "-c"]

ENV DUCKDB_VERSION=1.1.3

RUN echo "--> Install some useful tools" \
    && build_deps="neovim tree lnav unzip gradle" \
    && apt-get update \
    && apt-get install -y $build_deps


RUN echo "--> Install Duckdb client" \
    && wget https://github.com/duckdb/duckdb/releases/download/v$DUCKDB_VERSION/duckdb_cli-linux-aarch64.zip \
    && unzip duckdb_cli-linux-aarch64.zip -d /usr/local/bin \
    && rm duckdb_cli-linux-aarch64.zip

RUN echo "--> Purge apt artifacts" \
    && apt-get purge -y --auto-remove $build_deps \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*