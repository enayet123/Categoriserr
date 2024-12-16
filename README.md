# Categoriserr

A category enforcing companion app for the Starr applications Sonarr and Radarr which changes the location of media based on the tags associated 

Categoriserr utilises the existing Radarr and Sonarr APIs to change the file/hardlink location and gets the Starr app to move the files

## Installation/Setup

### Docker

The docker image is available and can be pulled from Docker Hub: [enayet123/categoriserr](https://hub.docker.com/r/enayet123/categoriserr) 

> **Note:** All environment variables associated with the Starr service you wish to manage must be provided.

Using docker compose is the recommended way to setup categoriserr e.g.
```
services:
  categoriserr:
    image: enayet123/categoriserr:latest
    container_name: categoriserr
    restart: unless-stopped
    environment:
      - RADARR_URL=http://192.168.1.1:7878
      - RADARR_API_KEY=api-key
      - RADARR_TAG_LOCATION_MAP=kids:/data/movies-kids/,anime:/data/movies-anime/,horror:/data/movies-horror/
      - SONARR_URL=http://192.168.1.1:8989
      - SONARR_API_KEY=api-key
      - SONARR_TAG_LOCATION_MAP=kids:/data/media/shows-kids/,anime:/data/media/shows-anime/
      - SCHEDULE_INTERVAL_MINUTES=1
```

Using docker CLI as an alternative
```
docker run -d \
  --name=categoriserr \
  -e RADARR_URL=http://192.168.1.1:7878 \
  -e RADARR_API_KEY=api-key \
  -e RADARR_TAG_LOCATION_MAP=kids:/data/movies-kids/,anime:/data/movies-anime/,horror:/data/movies-horror/ \
  -e SONARR_URL=http://192.168.1.1:8989 \
  -e SONARR_API_KEY=api-key \
  -e SONARR_TAG_LOCATION_MAP=kids:/data/media/shows-kids/,anime:/data/media/shows-anime/ \
  -e SCHEDULE_INTERVAL_MINUTES=1 \
  --restart unless-stopped \
  enayet123/categoriserr:latest
```

### Python

> **Note:** The following steps assume you already have python installed.

Clone the repository to a location of your choice
```
git clone git@github.com:enayet123/Categoriserr.git
cd Categoriserr
```

Provide the required environment variables and run the application
```
RADARR_URL=radarr RADARR_API_KEY=key RADARR_TAG_LOCATION=kids:/data/movies/kids python main.py
```

## Environment Variables

All variables are optional however providing none will result in the application quitting

| Variable                    | Description                                                                                          |
|-----------------------------|------------------------------------------------------------------------------------------------------|
| `RADARR_URL`                | The URL used to locate your Radarr instance                                                          |
| `RADARR_API_KEY`            | The API key used to authenticate with your Radarr instance (Settings -> General -> API Key)          |
| `RADARR_TAG_LOCATION`       | The expected tags in Radarr mapped to their corresponding location with a colon delimited by a comma |
| `SONARR_URL`                | The URL used to locate your Sonarr instance                                                          |
| `SONARR_API_KEY`            | The API key used to authenticate with your Sonarr instance (Settings -> General -> API Key)          |
| `SONARR_TAG_LOCATION`       | The expected tags in Sonarr mapped to their corresponding location with a colon delimited by a comma |
| `SCHEDULE_INTERVAL_MINUTES` | The time between scans in minutes                                                                    |

## Limitations

- Current implementation is designed for a single instance of Radarr or Sonarr or both but no more (A work around to this can be to deploy multiple instances of Categoriserr)
- Only a single tag is expected to be found, multiple will lead to undesired behaviour and the location will be the latest tag it reads

## Disclaimer 

This application is provided "as is" without any warranties or guarantees of any kind, either express or implied. The use of this application is at your own risk. The developers assume no liability for any damages, losses, or issues, including but not limited to data loss, system malfunctions, or financial impacts, that may arise from the use or misuse of this application.

By using this application, you agree to take full responsibility for any outcomes and understand that the developers are not liable for any consequences resulting from its use. Always test the application in a controlled environment before deploying it in production.
