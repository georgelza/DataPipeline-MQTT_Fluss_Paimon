
FROM fluss/fluss:0.6.0
SHELL ["/bin/bash", "-c"]


RUN echo "--> Install some useful tools" && \
    build_deps="neovim tree lnav unzip" && \
    apt-get update && \
    apt-get install -y $build_deps



RUN echo "--> Purge apt artifacts" && \
    apt-get purge -y --auto-remove $build_deps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
