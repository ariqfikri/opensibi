NAME="opensibi" && \
docker build --rm -t $NAME . && \
docker rm -f $NAME && \
docker run -d --restart always -v /home/graciaevelyn737/opensibi/openSIBI.sqlite3:/code/openSIBI.sqlite3 -p 8000:8000 --name $NAME $NAME
docker logs $NAME