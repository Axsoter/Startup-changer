import requests
import time
# Configuration
PANEL_URL = '' # Your panel link.
APP_API_KEY = '' # Your APP API credintial.
NEW_STARTUP_SCRIPT = '' # The startup script you want the servers be changed to.
TARGET_EGG_ID = 1  # Replace with the specific Egg ID you want to target

def get_all_servers(api_key, egg_id=1, page=1):
    servers = []
    while True:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = requests.get(f'{PANEL_URL}/api/application/servers?page={page}', headers=headers)
        if response.status_code == 200:
            data = response.json()
            for server_data in data['data']:
                if server_data['attributes']['egg'] == egg_id:
                    servers.append(server_data)
            if data['meta']['pagination']['total_pages'] > page:
                page += 1
            else:
                break
        else:
            print(f'Error during the servers gathering process: {response.status_code}')
            break
    return servers

def update_startup_script(identifier):
    """Update the startup script for a given server."""
    headers = {
        'Authorization': f'Bearer {APP_API_KEY}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    data = {
        "startup": NEW_STARTUP_SCRIPT,
        "environment": {
            # Add and remove things to make this work for your egg.
            "SERVER_JARFILE": "server.jar",
            "DL_VERSION": "latest",
            "BUILD_NUMBER": "latest"
        },
        "egg": TARGET_EGG_ID,
        "image": "ghcr.io/pterodactyl/yolks:java_21", # Change it to your own.
        "skip_scripts": False
    }
    response = requests.patch(f'{PANEL_URL}/api/application/servers/{identifier}/startup', headers=headers, json=data)
    if response.status_code == 200:
        print(f'Successfully updated startup script for server {identifier}')
    else:
        print(f'Failed to update startup script for server {identifier}: {response.status_code} - {response.text}')



def main():
    print("Ready for work.")
    while True: 
        servers = get_all_servers(APP_API_KEY, TARGET_EGG_ID)
        for server in servers:
            identifier = server['attributes']['id']
            print(f'Starting start up script change for {identifier}.')
            update_startup_script(identifier)
            time.sleep(1) # This is so the requests wont be blocked.
        print("All servers checked!")
        break

if __name__ == '__main__':
    main()
