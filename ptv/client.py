from hashlib import sha1
from enum import Enum
import hmac
import requests
import urllib

API_VER = '/v3/'
BASE_URL = 'https://timetableapi.ptv.vic.gov.au'

class RouteType(Enum):
    """ Enum for Route Types and their IDs."""
    TRAIN = 0
    TRAM = 1
    BUS = 2
    VLINE = 3
    NIGHT_BUS = 4

class PTVClient(object):
    """ Class to make calls to PTV API."""

    def __init__(self,dev_id, api_key):
        """Initialize a PTVClient.

        Parameters
            dev_id (str)
                Developer ID from PTV
            api_key (str)
                API key from PTV
        """
        self.dev_id = dev_id
        self.api_key = api_key

    def _computeSignature(self,path):
        """Utility method to compute signature from url

        Parameters
            path (str)
                The target path of the URL with leading slash (e.g '/v3/search/').

        Returns
            The hex signature. (str)
        """
        key = bytes(self.api_key, 'UTF-8')
        raw = bytes(path, 'UTF-8')
        return hmac.new(key, raw, sha1).hexdigest().upper()

    def _api_call(self, path, params={}):
        """Create URL and call API

        Parameters:
            path (str)
                The endpoint we are calling
            params (dict)
                Dictionary containing parameters to be passed in the query

        Returns
            JSON from response as dict
        """
        params["devid"] = self.dev_id
        query = "?" + urllib.parse.urlencode(params,doseq=True)
        url = BASE_URL + path + query + '&signature=' + self._computeSignature(path + query)
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    # Departures
    def get_departure_from_stop(self, route_type, stop_id, route_id=None, platform_numbers=[],
        direction_id=None, date_utc=None, max_results=None, gtfs=False,
        include_cancelled=False, expand=None):
        """Get Service departures from the specified stop for all routes of the
        specified route type or a single route if route_id is specified.
        departures are timetabled and real-time (if applicable).

        Parameters:
            route_type (RouteType enum)
                Type of transport
            stop_id (int)
                ID of the Stop

        Optional Parameters:
            platform_numbers (int [])
                Filter by platform number at stop
            direction_id (int)
                Filter by identifier of direction of travel
            date_utc (date)
                Filter by the date and time of the request (ISO 8601 UTC format)
            max_results (int)
                Maximum number of results returned
            gtfs (bool)
                Indicates that stop_id parameter will accept "GTFS stop_id" data
            include_cancelled (bool)
                Indicates if cancelled services (if they exist) are returned
                (default = false) - metropolitan train only
            expand (str [])
                List objects to be returned in full (i.e. expanded)
                - options include: all, stop, route, run, direction, disruption
        """
        path = API_VER + 'departures/route_type/{}/stop/{}'
        path = path.format(route_type.value,stop_id)
        if route_id:
            path += '/route/{}'
            path = path.format(route_id)
        params = {}
        if len(platform_numbers) > 0:
            params["platform_numbers"] = platform_numbers
        if direction_id:
            params["direction_id"] = direction_id
        if date_utc:
            params["date_utc"] = date_utc
        if max_results:
            params["max_results"] = max_results
        if gtfs:
            params["gtfs"] = str(True).lower()
        if include_cancelled and route_type == RouteType.TRAIN:
            params["include_cancelled"] = str(True).lower()
        if expand:
            params["expand"] = expand
        return self._api_call(path, params)

    # Directions
    def get_direction_for_route(self, route_id):
        """ Get The directions that a specified route travels in.

        Parameters:
            route_id (int)
                Identifier of route
        """
        path = API_VER + 'directions/route/{}'
        path = path.format(route_id)
        return self._api_call(path)

    def get_direction(self, direction_id):
        """Get All routes that travel in the specified direction.

        Parameters:
            direction_id (int)
                Identifier of direction of travel
        """
        path = API_VER + 'directions/{}'
        path = path.format(direction_id)
        return self._api_call(path)

    def get_direction_for_route_type(self, direction_id, route_type):
        """Get All routes of the specified route type that travel in the specified direction.

        Parameters:
            direction_id (int)
                Identifier of direction of travel
            route_type (RouteType enum)
                Type of Transport
        """
        path = API_VER + 'directions/{}/route_type/{}'
        path = path.format(direction_id, route_type.value)
        return self._api_call(path)

    # Disruptions
    def get_disruptions(self):
        """Get All disruption information for all route types."""
        path = API_VER + 'disruptions'
        return self._api_call(path)

    def get_disruptions_on_route(self, route_id, disruption_status=None):
        """Get All disruption information (if any exists) for the specified route.

        Parameters:
            route_id (int)
                Identifier of route
        Optional Parameters:
            disruption_status (str)
            Filter by status of disruption_status
            Options: 'current' or 'planned'
        """
        path = API_VER + 'disruptions/route/{}'
        path = path.format(route_id)
        params = {}
        if disruption_status:
            if disruption_status.lower() not in ['current', 'planned']:
                raise TypeError('Only \"current\" and \"planned\" allowed for disruption_status')
            params["disruption_status"] = disruption_status.lower()
        return self._api_call(path, params)

    def get_disruption(self, disruption_id):
        """Get Disruption information for the specified disruption ID.

        Parameters:
            disruption_id (int)
                Identifier of disruption
        """
        path = API_VER + 'disruptions/{}'
        path = path.format(disruption_id)
        return self._api_call(path)

    # Patterns
    def get_stopping_pattern_for_run(self, run_id, route_type, stop_id=None, date_utc=None):
        """Get The stopping pattern of the specified trip/service run and route type.

        Parameters:
            run_id (int)
                Identifier of a trip/service run
            route_type (RouteType enum)
                Type of Transport
        Optional Parameters:
            stop_id (int)
                Filter by stop_id
            date_utc (datetime)
                Filter by the date and time of the request (ISO 8601 UTC format)
        """
        path = API_VER + 'pattern/run/{}/route_type/{}'
        path = path.format(run_id, route_type.value)
        params = {}
        if stop_id:
            params['stop_id'] = stop_id
        if date_utc:
            params['date_utc'] = date_utc
        return self._api_call(path, params)

    # Routes
    def get_routes(self, route_types=[], route_name=None):
        """Get Route names and numbers for all routes of all route types.

        Optional Parameters:
            route_types (array[RouteType])
                An array of RouteType we want to filter by
            route_name (str)
                Filter by name of route
        """
        path = API_VER + 'routes'
        params = {}
        if route_name:
            params["route_name"] = route_name
        if len(route_types) > 0:
            params["route_types"] = list(map(lambda x: x.value, route_types))
        return self._api_call(path, params)

    def get_route(self, route_id):
        """Get the route name and number for the specified route ID

        Parameters:
            route_id (int)
                Identifier of route
        """
        path = API_VER + 'routes/{}'
        path = path.format(route_id)
        return self._api_call(path)

    # Route Types
    def get_route_types(self):
        """Get all route types (i.e. identifiers of transport modes) and their names
        """
        path = API_VER + 'route_types'
        return self._api_call(path)

    # Runs
    def get_runs_for_route(self, route_id):
        """Get All trip/service run details for the specified route ID.

        Parameters:
            route_id (int)
                Identifier of route
        """
        path = API_VER + 'runs/route/{}'
        path = path.format(route_id)
        return self._api_call(path)

    def get_run(self, run_id):
        """Get All trip/service run details for the specified run ID.

        Parameters:
            run_id (int)
                Identifier of a trip/service run
        """
        path = API_VER + 'runs/{}'
        path = path.format(run_id)
        return self._api_call(path)

    def get_run_for_route_type(self, run_id, route_type):
        """Get The trip/service run details for the run ID and route type specified.

        Parameters:
            run_id (int)
                Identifier of a trip/service run
            route_type (RouteType enum)
                Type of Transport
        """
        path = API_VER + 'runs/{}/route_type/{}'
        path = path.format(run_id, route_type.value)
        return self._api_call(path)

    # Search
    def search(self, search_term, route_types=[], latitude=None, longitude=None,
        max_distance=None, include_outlets=True):
        """Get Stops, routes and myki ticket outlets that contain the search term
        (note: stops and routes are ordered by route_type by default).

        Parameters:
            search_term (str)
                Search text (note: if search text is numeric and/or less than 3 characters,
                the API will only return routes)

        Optional Parameters:
            route_types (array[RouteType])
                An array of RouteType we want to filter by
            latitude
                Filter by geographic coordinate of latitude
            longitude
                Filter by geographic coordinate of longitude
            max_distance
                Filter by maximum distance (in metres) from location specified via
                latitude and longitude parameters
            include_outlets (bool)
                Indicates if outlets will be returned in response (default = true)
        """
        path = API_VER + 'search/' + urllib.parse.quote(search_term)
        params = {}
        if len(route_types) > 0:
            params['route_types'] = list(map(lambda x: x.value, route_types))
        if latitude:
            params['latitude'] = latitude
        if longitude:
            params['longitude'] = longitude
        if max_distance:
            params['max_distance'] = max_distance
        params['include_outlets'] = str(include_outlets).lower()
        return self._api_call(path, params)

    # Stops
    def get_stop(self, stop_id, route_type, stop_location=False,
        stop_amenities=False, stop_accessibility=False):
        """Get Stop location, amenity and accessibility facility information for
        the specified stop (metropolitan and V/Line stations only).

        Parameters:
            stop_id (int)
                Identifier of stop
            route_type (RouteType enum)
                Type of Transport

        Optional Parameters:
            stop_location (bool)
                Indicates if stop location information will be returned (default = false)
            stop_amenities (bool)
                Indicates if stop amenity information will be returned (default = false)
            stop_accessibility (bool)
                Indicates if stop accessibility information will be returned (default = false)
        """
        path = API_VER + 'stops/{}/route_type/{}'
        path = path.format(stop_id, route_type.value)
        params = {}
        params['stop_location'] = str(stop_location).lower()
        params['stop_amenities'] = str(stop_amenities).lower()
        params['stop_accessibility'] = str(stop_accessibility).lower()
        return self._api_call(path, params)

    def get_stops(self, route_id, route_type):
        """Get All stops on the specified route.

        Parameters:
            route_id (int)
                Identifier of route_id
            route_type (RouteType enum)
                Type of Transport
        """
        path = API_VER + 'stops/route/{}/route_type/{}'
        path = path.format(route_id, route_type.value)
        return self._api_call(path)

    def get_stop_near_location(self, latitude, longitude, route_types=[], max_results=30, max_distance=300):
        """Get All stops near the specified location.

        Parameters:
            latitude
                Geographic coordinate of latitude
            longitude
                Geographic coordinate of longitude

        Optional Parameters:
            route_types (array[RouteType])
                An array of RouteType we want to filter by
            max_results (int)
                Maximum number of results returned (default = 30)
            max_distance
                Filter by maximum distance (in metres) from location specified
                via latitude and longitude parameters (default = 300)
        """
        path = API_VER + 'stops/location/{},{}'
        path = path.format(str(latitude), str(longitude))
        params = {}
        params['max_results'] = max_results
        params['max_distance'] = max_distance
        if len(route_types) > 0:
            params["route_types"] = list(map(lambda x: x.value, route_types))
        return self._api_call(path, params)
