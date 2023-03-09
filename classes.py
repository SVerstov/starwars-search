import aiohttp


class SWarsSearch:
    """ Universal class to search aby Star Wars items"""
    base_url = 'https://swapi.dev/api/{type}/?search={search}'

    def __init__(self, type: str, fields: list):
        self.type = type
        self.fields = fields

    async def _make_request(self, search_string):
        url = self.base_url.format(type=self.type, search=search_string)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    return None

    async def _filter_response(self, response):
        search_results = response['results']
        results_filtered = []
        for item in search_results:
            results_filtered.append({
                x: item[x] for x in self.fields
            })
        return results_filtered

    async def search(self, search_string):
        response = await self._make_request(search_string)
        if response:
            results_filtered = await self._filter_response(response)
            if len(results_filtered):
                return {self.type: results_filtered}
        return {}
