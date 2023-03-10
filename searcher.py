import aiohttp
import settings


class StarWarsSearch:
    """ Universal class to search aby Star Wars items"""

    def __init__(self, type: str, fields: list):
        self.type = type
        self.fields = fields

    async def _make_request(self, search_string):
        url = settings.api_url.format(type=self.type, search=search_string)
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
            item_dict = {}
            for field in self.fields:
                try:
                    item_dict[field] = item[field]
                except KeyError:
                    self.fields.remove(field)
                    print(f'Поле {field} исключено, т.к отсутствует в результатах!')
            results_filtered.append(item_dict)
        return results_filtered

    async def search(self, search_string):
        response = await self._make_request(search_string)
        if response:
            results_filtered = await self._filter_response(response)
            if len(results_filtered):
                return {self.type: results_filtered}
        return {}


search_list = [
    StarWarsSearch(type=k, fields=v) for k, v in settings.search_fields.items()
]
