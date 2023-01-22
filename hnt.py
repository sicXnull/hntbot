import requests
import json
import time

addresses = [ 'address1' 'address2']
webhook_url = ""
helium_api = "https://api.helium.io/v1/hotspots"
online_status = { }
initial_rewards = {}

while True:
    for address in addresses:
        hotspot_url = f'{helium_api}/{address}'
        hotspot_response = requests.get ( hotspot_url )
        if hotspot_response.status_code == 200:
            hotspot_data = hotspot_response.json ( )
            online = hotspot_data [ 'data' ] [ 'status' ] [ 'online' ]
            block = hotspot_data [ 'data' ] [ 'status' ] [ 'height' ]
            name = hotspot_data [ 'data' ] [ 'name' ]
            print ( f"Hotspot {name} is {online}" )

            # check if online status has changed
            if address not in online_status or online != online_status[address]:
                if online == "online":
                    # Create payload
                    payload = {
                        "embeds": [ {
                            "title": "Hotspot Status",
                            "fields": [ {
                                "name": "Hotsport Name",
                                "value": name
                            }, {
                                "name": "Address",
                                "value": address
                            }, {
                                "name": "Status",
                                "value": online
                            } ],
                            "color": 3066993
                        } ]
                    }
                    print ( f"Hotspot {name} is {online}" )
                    print("online status changed")
                if online == "offline":
                    # create embed
                    payload = {
                        "embeds": [ {
                            "title": "Hotspot {name} is Offline!",
                            "fields": [ {
                                "name": "Hotsport Name",
                                "value": name
                            }, {
                                "name": "Address",
                                "value": address
                            }, {
                                "name": "Status",
                                "value": "offline"
                            } ],
                            "color": 3066993
                        } ]
                    }
                    print ( f"Hotspot {name} is {online}" )
                    print("online status changed")
                # Send to webhook
                response = requests.post ( webhook_url, json=payload )
                print ( response )
                online_status [ address ] = online
        else:
            print(f'Error, status code: {hotspot_response.status_code}')

    for address in addresses:
        sum_url = f'{helium_api}/{address}/rewards'
        sum_response = requests.get ( sum_url )
        if sum_response.status_code == 200:
            sum_data = sum_response.json ( )
            if 'data' in sum_data:
                rewards = sum_data [ 'data' ] [ 'total' ] if sum_data['data'] else 0
                rewards = "{:.6f}".format(rewards)
                print ( rewards )

            # check for rewards,send embed
            if rewards != 0 and (address not in initial_rewards or rewards != initial_rewards [ address ]):
                payload = {
                    "embeds": [ {
                        "title": "New Reward for Hotspot",
                        "fields": [ {
                            "name": "Hotspot Name",
                            "value": name
                        }, {
                            "name": "Rewards",
                            "value": rewards
                        } ],
                        "color": 3066993
                    } ]
                }
                # Send to webhook
                response = requests.post ( webhook_url, json=payload )
                print ( response )
                initial_rewards [ address ] = rewards
        else:
            print ( f'Error, status code: {sum_response.status_code}' )


    time.sleep ( 300 )
