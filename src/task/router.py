from fastapi import APIRouter, HTTPException

from src.task.task_features import prepare_response

tree_router = APIRouter()


@tree_router.get("/paraphrase")
async def paraphrase_tree(tree: str, limit: int = 20) -> dict:
    try:
        return prepare_response(tree, limit)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid syntax Tree")
