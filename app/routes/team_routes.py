from fastapi import APIRouter
from app.models import Team
from app.database import teams_collection
from app.utils.decorators import response_timer
from app.utils.logger import logger
from app.utils.exceptions import TeamAlreadyExistsException, TeamCreationFailedException

router = APIRouter()

# POST /teams - Create a new team
@router.post("/create_team")
@response_timer
async def create_team(team: Team):
    try:
        # Check if team exists
        if teams_collection.find_one({"name": team.name}):
            logger.warning(f"Team creation failed: {team.name} already exists")
            raise TeamAlreadyExistsException(team.name)

        team_doc = team.model_dump()
        result = teams_collection.insert_one(team_doc)

        if not result.inserted_id:
            logger.error(f"Failed to create team: {team.name}")
            raise TeamCreationFailedException()

        logger.info(f"Team created successfully: {team.name}")
        return {"message": "Team created successfully", "team_id": str(result.inserted_id)}

    except TeamAlreadyExistsException as e:
        raise e
    except Exception as e:
        logger.exception(f"Unexpected error during team creation: {str(e)}")
        raise TeamCreationFailedException()

