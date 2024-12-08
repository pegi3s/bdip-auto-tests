FROM pegi3s/docker
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y python3 pip x11-xserver-utils
RUN pip install requests
COPY retrieve_test_data.py /opt
COPY run_docker.py /opt
COPY get_json.py /opt
COPY main.py /opt
WORKDIR /opt
