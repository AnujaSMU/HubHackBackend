from fastapi import APIRouter

router = APIRouter(prefix="/health")


@router.get("", tags=["Health"])
def get_health():
    return "Gateway is up and running!"
