
sudo docker stop redis
sudo docker rm redis
sudo docker create --name redis --hostname redis --restart unless-stopped --publish 6379:6379 redis:6.0.8-alpine
sudo docker start redis
