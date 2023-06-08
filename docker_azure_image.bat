set CONTAINER_NAME=oe_trading_api
set REGISTRY=oeappsregistry.azurecr.io
set TAG=latest_local

REM Stopping container
docker stop %CONTAINER_NAME%

REM
docker rm %CONTAINER_NAME%

REM Build image
docker build . -t %REGISTRY%/%CONTAINER_NAME%:%TAG%

REM Push Image to Azure
docker tag %REGISTRY%/%CONTAINER_NAME%:%TAG% %REGISTRY%/%CONTAINER_NAME%:%TAG%
docker push %REGISTRY%/%CONTAINER_NAME%:%TAG%

REM Run container
docker run -d --name %CONTAINER_NAME% -p 8000:8000 %REGISTRY%/%CONTAINER_NAME%