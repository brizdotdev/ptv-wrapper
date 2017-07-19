Public Transport Victoria (PTV) API Wrapper
============================================

Python3 API Wrapper for Public Transport Victoria (https://www.ptv.vic.gov.au/)

For the full API Documentation as well as information on how to request an API key, check out PTV Documentation_ and Swagger_

Installation
-------------

.. code-block:: bash

    $ python install ptv-wrapper

Usage
------
Instantiate client passing in Developer ID and API Key from PTV

.. code-block:: bash

  from ptv.client import PTVClient

  client = PTVClient(DEV_ID, API_KEY)

Note: Route types should always be passed using the RouteType Enum

.. code-block:: Python

   class RouteType(Enum):
    TRAIN = 0
    TRAM = 1
    BUS = 2
    VLINE = 3
    NIGHT_BUS = 4


Get Departures from stop
""""""""""""""""""""""""""""
Get Service departures from the specified stop for all routes of the specified route type or a single route if route_id is specified. Departures are timetabled and real-time (if applicable).

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

Example:

.. code-block:: Python

  client.get_departure_from_stop(RouteType.TRAIN, 1071)

Get Direction For Route
"""""""""""""""""""""""""""""
Get The directions that a specified route travels in.

        Parameters:
            route_id (int)
                Identifier of route

Example:

.. code-block:: Python

  client.get_direction_for_route(7)

Get All routes for a Direction
"""""""""""""""""""""""""""""""""""""

Get All routes that travel in the specified direction.

        Parameters:
            direction_id (int)
                Identifier of direction of travel

Example:

.. code-block:: Python

  client.get_direction(1)


Get Direction for Route Type
"""""""""""""""""""""""""""""""""""""
Get All routes of the specified route type that travel in the specified direction.

        Parameters:
            direction_id (int)
        Identifier of direction of travel
            route_type (RouteType enum)
                Type of Transport

Example:

.. code-block:: Python

    client.get_direction_for_route(1, RouteType.TRAIN)

Get Disruptions
"""""""""""""""""
Get All disruption information for all route types.

Example:

.. code-block:: Python

    client.get_disruptions()

Get Disruptions on Route
""""""""""""""""""""""""""
Get All disruption information (if any exists) for the specified route.

        Parameters:
            route_id (int)
                Identifier of route
        Optional Parameters:
            disruption_status (str)
            Filter by status of disruption_status
            Options: 'current' or 'planned'

.. code-block:: Python

    client.get_disruptions_on_route(7)

Get Disruption
"""""""""""""""
Get Disruption information for the specified disruption ID.

        Parameters:
            disruption_id (int)
                Identifier of disruption

.. code-block:: Python

    client.get_disruption(7)

Get Stopping Pattern for Run
""""""""""""""""""""""""""""""""
Get The stopping pattern of the specified trip/service run and route type.

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

.. code-block:: Python

    client.get_stopping_pattern_for_run(1, RouteType.TRAM)

Get Routes
"""""""""""""
Get Route names and numbers for all routes of all route types.

        Optional Parameters:
            route_types (array[RouteType])
                An array of RouteType we want to filter by
            route_name (str)
                Filter by name of route

.. code-block:: Python

    client.get_routes(route_types=[RouteType.TRAIN, RouteType.TRAM])

Get Route
"""""""""""
Get the route name and number for the specified route ID

        Parameters:
            route_id (int)
                Identifier of route

.. code-block:: Python

    client.get_route(1)

Get Route Types
"""""""""""""""
Get all route types (i.e. identifiers of transport modes) and their names

.. code-block:: Python

    client.get_route_types()

Get Runs For Route
"""""""""""""""""""
Get All trip/service run details for the specified route ID.

        Parameters:
            route_id (int)
                Identifier of route

.. code-block:: Python

    client.get_runs_for_route(7)

Get Run
""""""""
Get All trip/service run details for the specified run ID.

        Parameters:
            run_id (int)
                Identifier of a trip/service run


.. code-block:: Python

    client.get_run(12)

Get Run For Route Type
"""""""""""""""""""""""
Get The trip/service run details for the run ID and route type specified.

        Parameters:
            run_id (int)
                Identifier of a trip/service run
            route_type (RouteType enum)
                Type of Transport

.. code-block:: Python

    client.get_run_for_route_type(12, RouteType.TRAM)

Search
""""""""
Get Stops, routes and myki ticket outlets that contain the search term
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

.. code-block:: Python

    client.search("Flinders St")

Get Stop
"""""""""
Get Stop location, amenity and accessibility facility information for
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

.. code-block:: Python

    client.get_stop(1, RouteType.TRAIN)

Get Stops
"""""""""""
Get All stops on the specified route.

        Parameters:
            route_id (int)
                Identifier of route_id
            route_type (RouteType enum)
                Type of Transport

.. code-block:: Python

    client.get_stops(1, RouteType.TRAIN)

Get Stop Near Location
""""""""""""""""""""""""
Get All stops near the specified location.

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

.. code-block:: Python

    client.get_stop_near_location('-37.8182711', '144.9648731')

Contributing
-------------
If you've found a bug or would like a new feature, please open an issue or create a pull request.

.. _Documentation: https://www.ptv.vic.gov.au/about-ptv/ptv-data-and-reports/digital-products/ptv-timetable-api/
.. _Swagger: http://timetableapi.ptv.vic.gov.au/swagger/ui/index
