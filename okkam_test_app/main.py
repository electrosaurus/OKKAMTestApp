from aiohttp import web
from endpoints import get_percent


app = web.Application()
app.add_routes([web.get('/getPercent', get_percent)])

if __name__ == '__main__':
    web.run_app(app)
