from aiohttp import web
import asyncio

async def handle(request):
    return web.Response(text="Hello, this is a web server!")

async def init_app():
    app = web.Application()
    app.router.add_get('/', handle)
    return app

if __name__ == "__main__":
    app = asyncio.run(init_app())
    web.run_app(app)