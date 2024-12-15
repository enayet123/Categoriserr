import os, sys, time, requests, schedule

def media_to_str(json):
    id=json["id"]
    title=json["title"]
    path=json["path"]
    return f"\n\tid: '{id}'\n\ttitle: '{title}'\n\tpath: '{path}'"

def fetch_media(type, url, api_key):
    """Fetch all media from Radarr or Sonarr."""
    url = f"{url}/api/v3/{type}"
    headers = {"X-Api-Key": api_key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"[Categoriserr] Failed to fetch {type}: {response.status_code}, {response.text}")

def fetch_tags(url, api_key):
    """Fetch all tags from Radarr or Sonarr."""
    url = f"{url}/api/v3/tag"
    headers = {"X-Api-Key": api_key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        tags = response.json()
        return {tag['id']: tag['label'] for tag in tags}
    else:
        raise Exception(f"[Categoriserr] Failed to fetch tags: {response.status_code}, {response.text}")

def update_media_path(type, url, api_key, media_json, new_path, move_files=True):
    """Update the path of a movie in Radarr or Sonarr."""
    id = media_json["id"]
    url = f"{url}/api/v3/{type}/{id}?moveFiles={str(move_files).lower()}"
    headers = {"X-Api-Key": api_key}
    media_json["path"] = new_path
    response = requests.put(url, json=media_json, headers=headers)

    if response.status_code == 202:
        print(f"[Categoriserr] Updated media: {media_to_str(media_json)}'\n\tnew_path: {new_path}'")
    else:
        print(f"[Categoriserr] Failed to update media: {media_to_str(media_json)}")
        print(f"[Categoriserr] Failure Response: {response.status_code}, {response.text}")

def task(type, url, api_key, tag_location_map):
    tag_to_location = {}
    for mapping in tag_location_map.split(","):
        tag, location = mapping.split(":")
        tag_to_location[tag.strip()] = os.path.join(location.strip(), "")

    tag_id_to_name = fetch_tags(url, api_key)

    medias = fetch_media(type, url, api_key)
    for media in medias:
        tag_ids = media.get("tags", [])
        current_path = media["path"]
        folder_name = os.path.basename(current_path)

        tag_names = [tag_id_to_name.get(tag_id, "") for tag_id in tag_ids]

        for tag, new_root in tag_to_location.items():
            if tag in tag_names:
                new_path = os.path.join(new_root, folder_name)
                if current_path != new_path:
                    print(f"[Categoriserr] Enforcing path for media: {media_to_str(media)}\n\ttag: '{tag}'\n\tnew_path: '{new_path}'")
                    update_media_path(type, url, api_key, media, new_path)

if __name__ == "__main__":
    schedule_interval = int(os.getenv("SCHEDULE_INTERVAL_MINUTES", 10))
    print(f"[Categoriserr] Scheduled to run every {schedule_interval} minutes")

    radarr_url = os.getenv("RADARR_URL")
    radarr_api_key = os.getenv("RADARR_API_KEY")
    radarr_tag_location_map = os.getenv("RADARR_TAG_LOCATION_MAP")

    if radarr_url and radarr_api_key and radarr_tag_location_map:
        schedule.every(schedule_interval).minutes.do(lambda: task("movie", radarr_url, radarr_api_key, radarr_tag_location_map))
        task("movie", radarr_url, radarr_api_key, radarr_tag_location_map)

    sonarr_url = os.getenv("SONARR_URL")
    sonarr_api_key = os.getenv("SONARR_API_KEY")
    sonarr_tag_location_map = os.getenv("SONARR_TAG_LOCATION_MAP")

    if sonarr_url and sonarr_api_key and sonarr_tag_location_map:
        schedule.every(schedule_interval).minutes.do(lambda: task("series", sonarr_url, sonarr_api_key, sonarr_tag_location_map))
        task("series", sonarr_url, sonarr_api_key, sonarr_tag_location_map)

    if not schedule.get_jobs():
        print("[Categoriserr] No tasks were scheduled successfully, please provide Radarr or Sonarr url, api key and tag mapping")
        sys.exit()

    while True:
        schedule.run_pending()
        time.sleep(1)
