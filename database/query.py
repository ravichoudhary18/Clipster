from .db import engine, Base, database_create, session
from .models import ClipStack  # noqa: F401
from logger import logger
from datetime import datetime, timezone


def init_db():
    database_create()
    logger.info("CREATING TABLE IF NOT EXIST")
    Base.metadata.create_all(bind=engine)
    get_all()


def get_all():
    return session.query(ClipStack).all()


def create(text: str, star: bool = False, pinned: bool = False):
    try:
        new_clip = ClipStack(clip=text, star=star, pinned=pinned)
        session.add(new_clip)
        session.commit()
        logger.info(f"Inserted clip ID {new_clip.id}")
        return new_clip

    except Exception as e:
        session.rollback()
        logger.error(f"Error inserting clip: {e}")
        raise


def update(clip_id: int, clip: str = None, star: bool = None, pinned: bool = None):
    """Update fields for a ClipStack record based on provided parameters."""
    try:
        clip_obj = session.query(ClipStack).filter(ClipStack.id == clip_id).first()
        if not clip_obj:
            logger.warning(f"No record found with ID {clip_id}")
            return None

        # Conditionally update fields if provided
        if clip is not None:
            clip_obj.clip = clip
        if star is not None:
            clip_obj.star = star
        if pinned is not None:
            clip_obj.pinned = pinned

        # Always update the timestamp
        clip_obj.updated_at = datetime.now(timezone.utc)

        session.commit()
        logger.info(f"Updated clip ID {clip_id}")
        return clip_obj

    except Exception as e:
        session.rollback()
        logger.error(f"Failed to update clip ID {clip_id}: {e}")
        raise
