@echo off
REM run.bat - Build and run Lightbulb_AI container on Windows
REM Myriad Cognitive Architecture - Phase 1

set AGENT_NAME=lightbulb_ai
set PORT=5001

echo === Myriad Cognitive Architecture - Lightbulb_AI Agent ===
echo Building and running %AGENT_NAME% on port %PORT%

REM Stop and remove existing container if it exists
echo Stopping existing container (if any)...
docker stop %AGENT_NAME% 2>nul
docker rm %AGENT_NAME% 2>nul

REM Build the Docker image
echo Building Docker image...
docker build -t %AGENT_NAME%:latest .

REM Run the container
echo Starting container...
docker run -d ^
    --name %AGENT_NAME% ^
    -p %PORT%:5001 ^
    --restart unless-stopped ^
    %AGENT_NAME%:latest

echo Container started successfully!
echo Agent is running on http://localhost:%PORT%
echo.
echo Available endpoints:
echo   - http://localhost:%PORT%/health (Health check)
echo   - http://localhost:%PORT%/query (Main query endpoint)
echo   - http://localhost:%PORT%/info (Agent information)
echo.
echo To view logs: docker logs %AGENT_NAME%
echo To stop: docker stop %AGENT_NAME%

pause