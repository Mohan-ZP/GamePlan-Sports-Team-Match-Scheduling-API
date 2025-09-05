from fastapi import FastAPI
from app.routes import auth_routes, team_routes, player_routes, match_routes, analytics_routes

app = FastAPI(title="GamePlan - Sports Team & Match Scheduling API")


app.include_router(auth_routes.router, tags=["Authentication"])
app.include_router(team_routes.router, tags=["Teams"])
app.include_router(player_routes.router, tags=["Players"])
app.include_router(match_routes.router, tags=["Matches"])