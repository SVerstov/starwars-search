
api_url = 'https://swapi.dev/api/{type}/?search={search}'

search_fields = {
    # type: [fields]
    'people': ['name', 'mass', 'height'],
    'planets': ['name', 'diameter', 'population'],
    'starships': ['name', 'length', 'crew'],
}
