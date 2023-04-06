sudo mkdir -p /var/folders/datastore/conf/
sudo cp datastore.env /var/folders/datastore/conf/datastore.env
sudo docker stop datastore
sudo docker rm datastore

sudo docker create --name datastore --hostname datastore \
--restart unless-stopped --publish 5432:5432 \
--env-file /var/folders/datastore/conf/datastore.env postgis/postgis:12-2.5-alpine
sudo docker start datastore
