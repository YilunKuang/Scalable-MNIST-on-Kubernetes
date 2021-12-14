# Start with a Linux micro-container to keep the image tiny
FROM python:3.8

# Document who is responsible for this image
MAINTAINER Yilun Kuang "yk2516@nyu.edu"

# Expose any ports the app is expecting in the environment
ENV PORT 6000
EXPOSE $PORT

# Set up a working folder and install the pre-reqs
WORKDIR /project2_deploy
#RUN pip3 install --upgrade pip3
RUN pip3 --no-cache-dir install requests

# Add the code as the last Docker layer because it changes the most
ADD test.png  /project2_deploy/test.png
ADD client.py  /project2_deploy/client.py

# Run the service
CMD [ "python3", "client.py", ">", "trial.txt"] 
