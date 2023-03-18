''' Endpoints (methods) of the application's API. '''

from aiohttp import web
from core import audience_calculator, db_session


async def get_percent(request: web.Request) -> web.Response:
    ''' Implements the `/getPercent` API method. '''
    request_data = await request.json()
    audience_1_condition = request_data.get('audience1')
    audience_2_condition = request_data.get('audience2')
    if audience_1_condition is None or audience_2_condition is None:
        raise web.HTTPBadRequest(reason='Parameters `audience1` and `audience2` are required')
    try:
        inclusion_percent = audience_calculator.calc_inclusion_percent(
            audience_1_condition,
            audience_2_condition,
        )
    except ArithmeticError as error:
        raise web.HTTPBadRequest(reason=str(error))
    except Exception as error:
        raise web.HTTPInternalServerError(reason=str(error))
    finally:
        db_session.rollback()
    return web.json_response({'percent': inclusion_percent})
