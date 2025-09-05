from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.models import Match
from app.database import teams_collection, matches_collection
from app.utils.decorators import response_timer
from app.utils.logger import logger
from app.utils.exceptions import MatchCreationFailedException, InvalidMatchSetupException
from app.auth import get_current_user

router = APIRouter()

# Schedule a new match
@router.post("/create_match")
@response_timer
async def create_match(match: Match, current_user: dict = Depends(get_current_user)):
    try:
        # Role-based restriction (Admin only)
        if current_user.get("role") != "admin":
            logger.warning(f"Unauthorized match creation attempt by {current_user['email']}")
            raise HTTPException(status_code=403, detail="Only admins can schedule matches")

        # Validate teams
        home_team = teams_collection.find_one({"_id": ObjectId(match.home_team_id)})
        away_team = teams_collection.find_one({"_id": ObjectId(match.away_team_id)})

        if not home_team or not away_team:
            logger.warning("One or both teams not found")
            raise InvalidMatchSetupException("One or both teams not found")

        if match.home_team_id == match.away_team_id:
            logger.warning("A team cannot play against itself")
            raise InvalidMatchSetupException("A team cannot play against itself")

        match_doc = match.model_dump()
        match_doc["home_team_id"] = ObjectId(match.home_team_id)
        match_doc["away_team_id"] = ObjectId(match.away_team_id)

        result = matches_collection.insert_one(match_doc)
        if not result.inserted_id:
            logger.error("Failed to create match")
            raise MatchCreationFailedException()

        logger.info(f"Match scheduled: {home_team['name']} vs {away_team['name']} on {match.date}")
        return {"message": "Match scheduled successfully", "match_id": str(result.inserted_id)}

    except (MatchCreationFailedException, InvalidMatchSetupException) as e:
        raise e
    except Exception as e:
        logger.exception(f"Unexpected error during match creation: {str(e)}")
        raise MatchCreationFailedException()


# Get all matches
@router.get("/all_matches")
@response_timer
async def get_matches(current_user: dict = Depends(get_current_user)):
    try:
        matches = list(matches_collection.find())
        for m in matches:
            m["id"] = str(m["_id"])
            m["home_team_id"] = str(m["home_team_id"])
            m["away_team_id"] = str(m["away_team_id"])
            del m["_id"]

        logger.info(f"User {current_user['email']} fetched all matches")
        return {"matches": matches}

    except Exception as e:
        logger.exception(f"Error fetching matches: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch matches")