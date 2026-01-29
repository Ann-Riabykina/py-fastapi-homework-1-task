from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import MovieModel, get_db
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter(prefix="/movies")


@router.get("/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    total_items = await db.scalar(select(func.count()).select_from(MovieModel))
    total_items = int(total_items or 0)

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = ceil(total_items / per_page)
    offset = (page - 1) * per_page

    result = await db.execute(
        select(MovieModel).order_by(MovieModel.id).offset(offset).limit(per_page)
    )
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    base_path = "/theater/movies/"

    prev_page = None
    if page > 1:
        prev_page = f"{base_path}?page={page - 1}&per_page={per_page}"

    next_page = None
    if page < total_pages:
        next_page = f"{base_path}?page={page + 1}&per_page={per_page}"

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()

    if movie is None:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )

    return movie
