from httpx import AsyncClient

from .base_fittings import Async_Fitting

class Async_Test_Fitting(Async_Fitting):

    async def fitting(self):
        props = self.fso.props
        async with self.client as client:
            r = await client.get(props.url)
            print(r.text)