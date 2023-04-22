docker stop quantlib
docker build . -t jcorderop/quantlib
docker push docker.io/jcorderop/quantlib
docker run --rm --name quantlib -p 8000:8000 -d jcorderop/quantlib