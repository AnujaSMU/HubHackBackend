import logging
from datetime import datetime ,date

from bson import ObjectId
from fastapi import APIRouter, status, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List

from src.models.Program_model import ProgramModel ,SearchEligibility
from src.services import mongo_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

collection = mongo_db.db["Programs"]

router = APIRouter(prefix="/programs")

class MongoProjectException(Exception):
    pass

@router.post("/create", status_code=status.HTTP_201_CREATED, tags=["Programs Controller"])
async def create_programs(programs: ProgramModel):
    """
    Create program entry

    Returns:
        ObjectID of inserted program entry
    """

    try:
        programs_dict = programs.model_dump()
        if isinstance(programs_dict['end_date'], date):
            programs_dict['end_date'] = datetime.combine(programs_dict['end_date'], datetime.min.time())

        inserted_Programs = collection.insert_one(programs_dict)
        return JSONResponse(content={"id": str(inserted_Programs.inserted_id)})

    except Exception as e:
        logger.error(f"Failed to create chat log due to {e.args}")
        raise HTTPException(status_code=404, detail=e.args)


@router.get("/get_programs", status_code=status.HTTP_200_OK, tags=["Programs Controller"])
async def get_all_programs(only_active: bool = True):
    """
        Retrieves all active projects.

        Returns:
            List[str]: A list of all team names.
    """
    try:
        active_programs = []
        if only_active:
            found_programs = list(collection.find({"status":"Active"}))
        else:
            found_programs = list(collection.find({}))
        if found_programs:
            for programs in found_programs:
                programs["_id"] = str(programs["_id"])
                #del programs["_id"]
                #active_programs.append(programs)
            return found_programs
        else:
            raise MongoProjectException()

    except MongoProjectException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No groups found")

    except Exception as e:
        logger.error(f"Failed to get group record due to {e.args}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error {e.args}")

@router.get("/get_eligibility", status_code=status.HTTP_200_OK, tags=["Programs Controller"])
async def search_by_eligibility(eligibility: List[str] = Query(...)):
    """
    Searches program by eligibility
    
    """
    try:
        cursor = collection.find({"eligibility": {"$in": eligibility}})
        documents = list(cursor)
        for document in documents:
            document["_id"] = str(document["_id"])
            #del document["_id"]
        return documents

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update_programs",status_code=status.HTTP_200_OK, tags=["Programs Controller"])
async def update_programs(programs: ProgramModel, program_id: str):
    """
    Update program entry

    Returns:
        ObjectID of updated program entry
    """

    try:
        programs_dict = programs.model_dump()
        if isinstance(programs_dict['end_date'], date):
            programs_dict['end_date'] = datetime.combine(programs_dict['end_date'], datetime.min.time())

        updated_Programs = collection.update_one({"_id": ObjectId(program_id)}, {"$set": programs_dict})
        return JSONResponse(content={"id": str(updated_Programs.inserted_id)})

    except Exception as e:
        logger.error(f"Failed to update chat log due to {e.args}")
        raise HTTPException(status_code=404, detail=e.args)


@router.delete("/delete_programs", status_code=status.HTTP_200_OK, tags=["Programs Controller"])
async def delete_programs(program_id: str):
    """
    Delete program entry

    Returns:
        ObjectID of deleted program entry
    """

    try:
        deleted_Programs = collection.delete_one({"_id": ObjectId(program_id)})
        return JSONResponse(content={"id": str(deleted_Programs.inserted_id)})

    except Exception as e:
        logger.error(f"Failed to delete chat log due to {e.args}")
        raise HTTPException(status_code=404, detail=e.args)