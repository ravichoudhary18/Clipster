from sqlalchemy import Column, Integer, Text, Boolean, DateTime, func, text
from .db import Base


class ClipStack(Base):
    __tablename__ = "clipstack"

    id = Column(Integer, primary_key=True)
    clip = Column(Text, nullable=False, unique=True)

    star = Column(Boolean, default=False, server_default=text("0"))
    pinned = Column(Boolean, default=False, server_default=text("0"))

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        server_default=func.now(),
    )

    def __repr__(self):
        return f"<ClipStack id={self.id} pinned={self.pinned} start={self.star}>"
