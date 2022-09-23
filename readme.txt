Download from Google Disk models and put in NN_models (3 files)
Download from Google Disk pyface-rec-service-image.zip

!!!! if not working as is - install Docker Desktop !!!!
install Docker Desktop on Windows (before enable Hyper V in add/remove Windows components,
 Virtual Machine Platform and Windows Subsystem for Linux -
 https://stackoverflow.com/questions/66267529/docker-desktop-3-1-0-installation-issue-access-is-denied
 )
run docker desktop from start menu
!!!!!


!!!!!!!!!!!!! Use container !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
On server load and run:
docker load -i pyface-rec-service-image.zip
docker run -d -p 127.0.0.1:5000:5000 --name pyface-rec-service pyface-rec-service:v0.1.0

You can run multiple containers:
docker run -d -p 127.0.0.1:5000:5000 --name pyface-rec-service_0 pyface-rec-service:v0.1.0
docker run -d -p 127.0.0.1:5001:5000 --name pyface-rec-service_1 pyface-rec-service:v0.1.0
docker run -d -p 127.0.0.1:5002:5000 --name pyface-rec-service_2 pyface-rec-service:v0.1.0
....


Stop service:
docker stop pyface-rec-service

Remove service:
docker rm -f pyface-rec-service
docker rmi --force pyface-rec-service:v0.1.0


!!!!!!!!!!!!! For dev - build and deploy !!!!!!!!!!!!!!!!
Build container:
docker build -t pyface-rec-service:v0.1.0 backend/

run container:
docker run -d -p 5000:5000 --name pyface-rec-service pyface-rec-service:v0.1.0

stop container:
docker stop pyface-rec-service
docker rm -f pyface-rec-service

remove container:
docker rmi --force pyface-rec-service:v0.1.0

Save to file
docker save -o pyface-rec-service-image.zip pyface-rec-service
