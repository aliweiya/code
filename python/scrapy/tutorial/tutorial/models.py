# -*- coding: utf-8 -*-

'''models will be defined here'''

from sqlalchemy import Column, Integer, String, create_engine, ForgienKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = None
session = None

class Singer(Base):
    __tablename__ = 'Singer'

    singerId = Column(String, primary_key=True)
    singerName = Column(String)

class Album(Base):
    __tablename__ = 'Album'

    albumId = Column(String, primary_key=True)
    albumSingerId = Column(String, ForgienKey('Singer.singerId'))

class Song(Base):
    __tablename__ = 'Song'

    songId = Column(String, primary_key=True)
    songAlbumId = Column(String, ForgienKey('Album.albumId'))
    songSingerId = Column(String, ForgienKey('Singer.singerId'))
    commentCount = Column(Integer, default=0)