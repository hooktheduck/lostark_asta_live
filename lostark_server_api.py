from urllib.request import urlopen

def getStatusOf(euServer):
    url = "https://www.playlostark.com/de-de/support/server-status"
    page = urlopen(url)

    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    title_index = html.find(euServer.lower().capitalize()) - 683
    title = html[title_index : title_index + 135]  

    if "good" in title:
        astaStatus = "Good"
    elif "busy" in title:
        astaStatus = "Busy"
    elif "full" in title:
        astaStatus = "Full"
    elif "maintenance" in title:
        astaStatus = "Maintenance"
    else:
        raise Exception

    return astaStatus
