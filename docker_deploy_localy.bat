REM Stop local container
set CONTAINER_NAME=oe_trading_api
set REGISTRY=oe

REM Stopping container
docker stop %CONTAINER_NAME%

REM Removing container
docker rm %CONTAINER_NAME%

REM Build image
docker build . -t %REGISTRY%/%CONTAINER_NAME%

REM Run container
docker run -d --name %CONTAINER_NAME% -p 8000:8000 %REGISTRY%/%CONTAINER_NAME%