import logging
from datetime import datetime ,date

from bson import ObjectId
from fastapi import APIRouter, status, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List

from src.models.Changes_model import ChangesModel
from src.services import mongo_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

collection = mongo_db.db["Changes"]

programs_collection = mongo_db.db["Programs"]

router = APIRouter(prefix="/changes")

@router.post("/create", status_code=status.HTTP_201_CREATED, tags=["Changes Controller"])
async def create_programs(changes: ChangesModel):
    """
    Create program entry

    Returns:
        ObjectID of inserted program entry
    """

    try:
        programs_dict = changes.model_dump()
        if isinstance(programs_dict['end_date'], date):
            programs_dict['end_date'] = datetime.combine(programs_dict['end_date'], datetime.min.time())

        inserted_Programs = collection.insert_one(programs_dict)
        return JSONResponse(content={ "program_id": programs_dict['id'] , "changes_id": str(inserted_Programs.inserted_id)})

    except Exception as e:
        logger.error(f"Failed to create chat log due to {e.args}")
        raise HTTPException(status_code=404, detail=e.args)

@router.put("/approve/{program_id}", status_code=status.HTTP_200_OK, tags=["Changes Controller"])
async def approve_changes(program_id: str, changes_id: str):
    """
    Approve changes

    Returns:
        ObjectID of inserted program entry
    """

    try:
        returned_doc = collection.find_one_and_update({"_id": ObjectId(changes_id)}, {"$set": {"change_status": "Approved"}})
        if returned_doc:
            updated_program = {
                key: returned_doc[key] for key in [
                    "program_name", "description", "delivery_method", "status", "funders",
                    "end_date", "team", "other_eligibility_criteria", "geographic_availability",
                    "literacy_requirement", "age_targeting", "gender_targeting",
                    "staff_member_names", "eligibility"
                ]
            }
            updated_program["previous_id"] = program_id
            inserted_program_changes = programs_collection.insert_one(updated_program)

            programs_collection.update_one({"_id": ObjectId(program_id)},{"$set":{"status":"Inactive"}})

        return JSONResponse(content={"id": str(inserted_program_changes.inserted_id)})

    except Exception as e:
        logger.error(f"Failed to create chat log due to {e.args}")
        raise HTTPException(status_code=404, detail=e.args)