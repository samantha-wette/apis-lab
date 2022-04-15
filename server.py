from flask import Flask, render_template, request

from pprint import pformat
import os
import requests
import json


app = Flask(__name__)
app.secret_key = 'hlshgherlhgjgdshgk'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['TICKETMASTER_KEY']

# ROOT URL - https://app.ticketmaster.com/discovery/v2/

# Search for events sourced by Universe in the United States with keyword “devjam” https://app.ticketmaster.com/discovery/v2/events.json?keyword=devjam&source=universe&countryCode=US&apikey={apikey}

# Parameter [radius]

payload = {'apikey': API_KEY}

@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')

@app.route('/afterparty')
def show_afterparty_form():
    """Show event search form"""

    return render_template('search-form.html')


@app.route('/afterparty/search')
def find_afterparties():
    """Search for afterparties on Eventbrite"""

    keyword = request.args.get('keyword', '')
    postalcode = request.args.get('zipcode', '')
    radius = request.args.get('radius', '')
    unit = request.args.get('unit', '')
    sort = request.args.get('sort', '')

    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {
        'apikey': API_KEY,
        'keyword': keyword,
        'radius': radius,
        'unit': unit,
        'sort': sort,
    }

    res = requests.get(url, params=payload)
    data = res.json()
    #tmbg_songs = res.json()
    
    #with open('afterparties.json', 'w') as f:
	    #json.dump(data, f)


    # - Make sure to save the JSON data from the response to the `data`

    
    # TODO: Make a request to the Event Search endpoint to search for events
    #
    # - Use form data from the user to populate any search parameters
    #
    
    #   variable so that it can display on the page. This is useful for
    #   debugging purposes!
    #
    # - Replace the empty list in `events` with the list of events from your
    #   search results

    # data = {'Test': ['This is just some test data'],
    #         'page': {'totalElements': 1}}

    
    # events = data.get(["_embedded"]["events"]["id"])
    embedded_info = data.get("_embedded", {})
    events = embedded_info.get("events", [])

    #events = list(events)
    
    return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results=events)


# ===========================================================================
# FURTHER STUDY
# ===========================================================================


@app.route('/event/<id>')
def get_event_details(id):
    """View the details of an event."""

    print(f"ID =>>>>>>> {id}")
    # TODO: Finish implementing this view function
    # make a request to the Ticketmaster API in order to retrieve data about one event
    # Hint: you’ll need to look up the correct endpoint for getting event details
    # Hint: you’ll also need to use id to construct your final endpoint

    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {
        'apikey': API_KEY,
        'id' : id
    }

    res = requests.get(url, params=payload)
    data = res.json()

    embedded_info = data.get("_embedded", {})
    breakpoint()
    events = embedded_info.get("events", [])
    # event = events[0]
    # event["id"] = "string"
    # our_id = events[0]["id"]

    event_name = events[0]["name"]

    # # "events": [{"id": "string"}]

    return render_template('event-details.html', data=data, event_name=event_name)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
