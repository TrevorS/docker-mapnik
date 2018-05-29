FROM ubuntu:16.04

# Prerequisites and runtimes
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    sudo \
    software-properties-common \
    curl \
    wget \
    libboost-dev \
    libboost-filesystem-dev \
    libboost-program-options-dev \
    libboost-python-dev \
    libboost-regex-dev \
    libboost-system-dev \
    libboost-thread-dev \
    libicu-dev \
    libtiff5-dev \
    libfreetype6-dev \
    libpng12-dev \
    libxml2-dev \
    libproj-dev \
    libsqlite3-dev \
    libgdal-dev \
    libcairo-dev \
    python-cairo-dev \
    postgresql-contrib \
    libharfbuzz-dev \
    python3-dev \
    git \
    python3-setuptools \
    python3-pip \
    python3-wheel \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Mapnik
ENV MAPNIK_VERSION 3.0.20
RUN curl -Ls https://github.com/mapnik/mapnik/releases/download/v${MAPNIK_VERSION}/mapnik-v${MAPNIK_VERSION}.tar.bz2 | tar -xj -C /tmp/
RUN cd /tmp/mapnik-v${MAPNIK_VERSION} && python scons/scons.py configure
RUN cd /tmp/mapnik-v${MAPNIK_VERSION} && make JOBS=4 && make install JOBS=4

# Python Bindings
ENV PYTHON_MAPNIK_COMMIT 804a7947d0176e2685ebf62459b44d9d08161451
RUN mkdir -p /opt/python-mapnik && curl -L https://github.com/mapnik/python-mapnik/archive/${PYTHON_MAPNIK_COMMIT}.tar.gz | tar xz -C /opt/python-mapnik --strip-components=1
RUN cd /opt/python-mapnik && python3 setup.py install && rm -r /opt/python-mapnik/build

# Download State Shapes
ENV STATES_SHAPEFILE_ZIP cb_2017_us_state_500k.zip
ENV STATES_SHAPEFILE_DIR /opt/shapefiles/states

RUN mkdir -p ${STATES_SHAPEFILE_DIR} && \
  wget http://www2.census.gov/geo/tiger/GENZ2017/shp/${STATES_SHAPEFILE_ZIP} -P ${STATES_SHAPEFILE_DIR} && \
  unzip -d ${STATES_SHAPEFILE_DIR} ${STATES_SHAPEFILE_DIR}/${STATES_SHAPEFILE_ZIP} && \
  rm ${STATES_SHAPEFILE_DIR}/${STATES_SHAPEFILE_ZIP}

# Download County Shapes
ENV COUNTY_SHAPEFILE_ZIP cb_2017_us_county_500k.zip
ENV COUNTY_SHAPEFILE_DIR /opt/shapefiles/counties

RUN mkdir -p ${COUNTY_SHAPEFILE_DIR} && \
  wget http://www2.census.gov/geo/tiger/GENZ2017/shp/${COUNTY_SHAPEFILE_ZIP} -P ${COUNTY_SHAPEFILE_DIR} && \
  unzip -d ${COUNTY_SHAPEFILE_DIR} ${COUNTY_SHAPEFILE_DIR}/${COUNTY_SHAPEFILE_ZIP} && \
  rm ${COUNTY_SHAPEFILE_DIR}/${COUNTY_SHAPEFILE_ZIP}

ENTRYPOINT ["/bin/bash", "/opt/scripts/run_all.sh"]
