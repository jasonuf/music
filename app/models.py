from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import datetime, timezone

class Song(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    artist: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    album: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, nullable=True)
    album_picture: so.Mapped[str] = so.mapped_column(sa.String(120), nullable=True)
    album_release_date: so.Mapped[str] = so.mapped_column(sa.String(20), index=True, nullable=True)

    play_history: so.Mapped[list['PlayedHistory']] = so.relationship(
        back_populates='song', cascade='all, delete-orphan'
    )

    __table_args__ = (
        sa.UniqueConstraint('title', 'artist', name='_title_artist_uc'),
    )

    def __repr__(self):
        return f'<Song "{self.title}" by {self.artist}>'

class PlayedHistory(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    
    timestamp: so.Mapped[datetime] = so.mapped_column(
        sa.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )

    song_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('song.id'), index=True)
    song: so.Mapped[Song] = so.relationship(back_populates='play_history')
    
    def __repr__(self):
        return f'<PlayedHistory for Song ID {self.song_id} at {self.timestamp}>'
