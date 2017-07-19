from pytest import fixture
from ptv.client import PTVClient
from ptv.client import RouteType

DEV_ID = "1000733"
API_KEY = "dfa5929b-04f9-11e6-a65e-029db85e733b"

FLINDERS_ST_STATION_STOP_ID = 1071
ROUTE_ID = 1
DIRECTION_ID = 1
DISRUPTION_ID = 1
RUN_ID = 1
LAT = '-37.8182711'
LON = '144.9648731'
SEARCH_TERM = 'Flinders St'

EXPECTED_DEPARTURE_KEYS = set([
    'departures',
    'stops',
    'routes',
    'runs',
    'directions',
    'disruptions',
    'status'
])

EXPECTED_DIRECTION_KEYS = set([
    'directions',
    'status'
])

EXPECTED_DISRUPTIONS_KEYS = set([
    'disruptions',
    'status'
])


EXPECTED_DISRUPTION_KEYS = set([
    'disruption',
    'status'
])

EXPECTED_PATTERN_KEYS = set([
    'departures',
    'disruptions',
    'status'
])

EXPECTED_ROUTE_KEYS = set([
    'route',
    'status'
])

EXPECTED_ROUTES_KEYS = set([
    'routes',
    'status'
])

EXPECTED_ROUTE_TYPE_KEYS = set([
    'route_types',
    'status'
])

EXPECTED_RUN_KEYS = set([
    'run',
    'status'
])

EXPECTED_RUNS_KEYS = set([
    'runs',
    'status'
])

EXPECTED_SEARCH_KEYS = set([
    'stops',
    'routes',
    'outlets',
    'status'
])

EXPECTED_STOP_KEYS = set([
    'stop',
    'status'
])

EXPECTED_STOPS_KEYS = set([
    'stops',
    'status'
])
@fixture
def client():
    """Instanciate the client class to query API """
    return PTVClient(DEV_ID,API_KEY)

# Departures Test
def test_get_departure_from_stop(client):
    json = client.get_departure_from_stop(RouteType.TRAIN,FLINDERS_ST_STATION_STOP_ID)
    assert isinstance(json, dict)
    assert EXPECTED_DEPARTURE_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1

def test_get_departure_from_stop_for_route(client):
    json = client.get_departure_from_stop(RouteType.TRAIN,FLINDERS_ST_STATION_STOP_ID, ROUTE_ID)
    assert isinstance(json, dict)
    assert EXPECTED_DEPARTURE_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1

# Directions Test
def test_get_direction_for_route(client):
    json = client.get_direction_for_route(ROUTE_ID)
    assert isinstance(json, dict)
    assert EXPECTED_DIRECTION_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1

def test_get_direction(client):
    json = client.get_direction(DIRECTION_ID)
    assert isinstance(json, dict)
    assert EXPECTED_DIRECTION_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1

def test_get_direction_for_route_type(client):
    json = client.get_direction_for_route_type(DIRECTION_ID, RouteType.TRAIN)
    assert isinstance(json, dict)
    assert EXPECTED_DIRECTION_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1

# Disruptions Test
def test_get_disruptions(client):
    json = client.get_disruptions()
    assert isinstance(json, dict)
    assert EXPECTED_DISRUPTIONS_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1

def test_get_disruptions_on_route(client):
    json = client.get_disruptions_on_route(ROUTE_ID)
    assert isinstance(json, dict)
    assert EXPECTED_DISRUPTIONS_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1

def test_get_disruption(client):
    json = client.get_disruption(DISRUPTION_ID)
    assert isinstance(json, dict)
    assert EXPECTED_DISRUPTION_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1

# Patterns Test
def test_get_stopping_pattern_for_run(client):
    json = client.get_stopping_pattern_for_run(RUN_ID, RouteType.TRAIN)
    assert isinstance(json, dict)
    assert EXPECTED_PATTERN_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1

# Routes Test
def test_get_routes(client):
    json = client.get_routes()
    assert isinstance(json, dict)
    assert EXPECTED_ROUTES_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1

def test_get_route(client):
    json = client.get_route(ROUTE_ID)
    assert isinstance(json, dict)
    assert EXPECTED_ROUTE_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1

# Route Types Test
def test_get_route_types(client):
    """Tests the GET RouteTypes endpoint"""
    json = client.get_route_types()
    assert isinstance(json, dict)
    assert EXPECTED_ROUTE_TYPE_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1

# Runs Test
def test_get_runs_for_route(client):
    json = client.get_runs_for_route(ROUTE_ID)
    assert isinstance(json, dict)
    assert EXPECTED_RUNS_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1

def test_get_run(client):
    json = client.get_run(RUN_ID)
    assert isinstance(json, dict)
    assert EXPECTED_RUNS_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1

def test_get_run_for_route_type(client):
    json = client.get_run_for_route_type(RUN_ID, RouteType.TRAIN)
    assert isinstance(json, dict)
    assert EXPECTED_RUN_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1

# Search Test
def test_search(client):
    json = client.search(SEARCH_TERM)
    assert isinstance(json, dict)
    assert EXPECTED_SEARCH_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1

# Stops Test
def test_get_stop_near_location(client):
    json = client.get_stop_near_location(LAT,LON)
    assert isinstance(json, dict)
    assert EXPECTED_STOPS_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1

def test_get_stop(client):
    json = client.get_stop(FLINDERS_ST_STATION_STOP_ID, RouteType.TRAIN)
    assert isinstance(json, dict)
    assert EXPECTED_STOP_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1

def test_get_stops(client):
    json = client.get_stops(ROUTE_ID, RouteType.TRAIN)
    assert isinstance(json, dict)
    assert EXPECTED_STOPS_KEYS.issubset(json.keys())
    assert json['status']['health'] == 1
