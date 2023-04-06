docker stop cache
docker rm cache
docker create --name cache --hostname cache \
--network memcache-app \
--restart unless-stopped --publish 11211:11211 --entrypoint memcached  \
memcached
docker start cache


