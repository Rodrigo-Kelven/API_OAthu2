from enum import Enum
from core.routes.routes import routes_auth_auten

class Tags(Enum):
    OAuth2 = "OAuth2"

class Prefix(Enum):
    prefix = "/api-auten_auth"

# funcao de uniao de todas as rotas existentes
def all_routes(app):
    app.include_router(routes_auth_auten, tags=[Tags.OAuth2], prefix=Prefix.prefix.value)



"""
def include_router(
    router: APIRouter,
    *,
    prefix: str = "",
    tags: List[str | Enum] | None = None,
    dependencies: Sequence[Depends] | None = None,
    responses: Dict[int | str, Dict[str, Any]] | None = None,
    deprecated: bool | None = None,
    include_in_schema: bool = True,
    default_response_class: type[Response] = Default(JSONResponse),
    callbacks: List[BaseRoute] | None = None,
    generate_unique_id_function: (APIRoute) -> str = Default(generate_unique_id)
)
"""