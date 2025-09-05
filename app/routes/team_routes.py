from fastapi import APIRouter, Depends, HTTPException
from app.auth import get_current_user
from app.models import Team
from app.database import teams_collection
from app.utils.decorators import response_timer
from app.utils.logger import logger
from app.utils.exceptions import TeamAlreadyExistsException, TeamCreationFailedException

router = APIRouter()

# Create a new team
@router.post("/create_team")
@response_timer
async def create_team(team: Team, current_user: dict = Depends(get_current_user)):
    try:
        # Role-based protection
        if current_user.get("role") != "admin":
            logger.warning(f"Unauthorized team creation attempt by {current_user['email']}")
            raise HTTPException(status_code=403, detail="Only admins can create teams")
        
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


# Get all teams
@router.get("/all_teams")
@response_timer
async def get_teams(current_user: dict = Depends(get_current_user)):
    try:
        teams = list(teams_collection.find())
        for t in teams:
            t["id"] = str(t["_id"])
            del t["_id"]

        logger.info(f"User {current_user['email']} fetched all teams")
        return {"teams": teams}

    except Exception as e:
        logger.exception(f"Error fetching teams: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch teams")