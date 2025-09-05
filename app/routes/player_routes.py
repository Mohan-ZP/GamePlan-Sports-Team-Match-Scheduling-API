from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from app.models import Player
from app.database import players_collection, teams_collection
from app.utils.decorators import response_timer
from app.utils.logger import logger
from app.utils.exceptions import PlayerAlreadyExistsException, PlayerCreationFailedException, PlayerNotFoundException
from app.auth import get_current_user

router = APIRouter()

# Add a new player
@router.post("/add_player")
@response_timer
async def create_player(player: Player, current_user: dict = Depends(get_current_user)):
    try:
        # Role-based check
        if current_user.get("role") not in ["admin", "coach"]:
            logger.warning(f"Unauthorized player creation attempt by {current_user['email']}")
            raise HTTPException(status_code=403, detail="Only admins or coaches can add players")

        # Check if team exists
        if not teams_collection.find_one({"_id": ObjectId(player.team_id)}):
            logger.warning("Team not found")
            raise HTTPException(status_code=404, detail="Team not found")

        # Check if player already exists in same team
        if players_collection.find_one({"name": player.name, "team_id": player.team_id}):
            logger.warning(f"Player creation failed: {player.name} already exists in team {player.team_id}")
            raise PlayerAlreadyExistsException(player.name)

        player_doc = player.model_dump()
        player_doc["team_id"] = ObjectId(player.team_id)  # Store as ObjectId
        result = players_collection.insert_one(player_doc)

        if not result.inserted_id:
            logger.error(f"Failed to create player: {player.name}")
            raise PlayerCreationFailedException()

        logger.info(f"Player created successfully: {player.name}")
        return {"message": "Player created successfully", "player_id": str(result.inserted_id)}

    except PlayerAlreadyExistsException as e:
        raise e
    except Exception as e:
        logger.exception(f"Unexpected error during player creation: {str(e)}")
        raise PlayerCreationFailedException()


# Get all players
@router.get("/all_players")
@response_timer
async def get_players(current_user: dict = Depends(get_current_user)):
    try:
        players = list(players_collection.find())
        for p in players:
            p["id"] = str(p["_id"])
            p["team_id"] = str(p["team_id"])  
            del p["_id"]

        logger.info(f"User {current_user['email']} fetched all players")
        return {"players": players}

    except Exception as e:
        logger.exception(f"Error fetching players: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch players")
    

# Get a single player by ID
@router.get("/players/{player_id}")
@response_timer
async def get_player(player_id: str, current_user: dict = Depends(get_current_user)):
    try:
        # Role-based check
        if current_user.get("role") not in ["admin", "coach"]:
            logger.warning(f"Unauthorized player creation attempt by {current_user['email']}")
            raise HTTPException(status_code=403, detail="Only admins or coaches can add players")
        
        player = players_collection.find_one({"_id": ObjectId(player_id)})
        
        if not player:
            logger.warning(f"Player not found: {player_id}")
            raise PlayerNotFoundException(player_id)

        player["id"] = str(player["_id"])
        player["team_id"] = str(player["team_id"])
        del player["_id"]

        logger.info(f"User {current_user['email']} fetched player {player['name']}")
        return player

    except PlayerNotFoundException as e:
        raise e
    except Exception as e:
        logger.exception(f"Error fetching player {player_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch player")
