from __future__ import annotations  # for forward references if needed
from .db import engine, Base, database_create, session
from .models import ClipStack  # noqa: F401
from logger import logger
from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from typing import Optional, List


def init_db() -> None:
    database_create()
    logger.info("CREATING TABLE IF NOT EXIST")
    Base.metadata.create_all(bind=engine)
    get_all()


def get_all() -> List[ClipStack]:
    clips = (
        session.query(ClipStack)
        .order_by(desc(ClipStack.pinned), desc(ClipStack.updated_at))
        .all()
    )
    return clips


def create(text: str, star: bool = False, pinned: bool = False) -> Optional[ClipStack]:
    try:
        new_clip = ClipStack(clip=text, star=star, pinned=pinned)
        session.add(new_clip)
        session.commit()
        logger.info(f"Inserted clip ID {new_clip.id}")
        return new_clip

    except IntegrityError as e:
        session.rollback()
        logger.warning(f"Duplicate clip detected: {text} -- {e}")
        update(clip=text, star=star, pinned=pinned)
        return None

    except Exception as e:
        session.rollback()
        logger.error(f"Error inserting clip: {e}")
        raise


def update(
    clip: Optional[str] = None,
    star: Optional[bool] = None,
    pinned: Optional[bool] = None,
) -> Optional[ClipStack]:
    """Update fields for a ClipStack record based on provided parameters."""
    try:
        clip_obj = session.query(ClipStack).filter(ClipStack.clip == clip).first()
        if not clip_obj:
            logger.warning(f"No record found with clip {clip}")
            return None

        if clip is not None:
            clip_obj.clip = clip
        if star is not None:
            clip_obj.star = star
        if pinned is not None:
            clip_obj.pinned = pinned

        if not pinned or not star:
            clip_obj.updated_at = datetime.now(timezone.utc)

        session.commit()
        logger.info(f"Updated clip ID {clip}")
        return clip_obj

    except Exception as e:
        session.rollback()
        logger.error(f"Failed to update clip ID {clip}: {e}")
        raise


def delete(clip: str) -> None:
    try:
        clip_obj = session.query(ClipStack).filter(ClipStack.clip == clip).first()
        if clip_obj:
            session.delete(clip_obj)
            session.commit()
            logger.info(f"Deleted clip ID {clip_obj.id}")
    except Exception as e:
        session.rollback()
        logger.error(f"Error deleting clip {clip}: {e}")
        raise
