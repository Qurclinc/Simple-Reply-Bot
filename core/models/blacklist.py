from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class Blacklist(Base):
    __tablename__ = "blacklists"
    
    user_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    reason: Mapped[str] = mapped_column(nullable=True)