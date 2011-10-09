#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from medialib.model import Base, Tag, Media
import json
import os

tag_list = dict()
media_list = dict()

def as_object(obj):
    if '__tag__' in obj:
        tag = Tag(obj['name'])

        if 'desc' in obj:
            tag.description = obj['desc']

        if 'id' in obj:
            tag_list[obj['id']] = tag

        if 'parent' in obj:
            if obj['parent'] in tag_list:
                tag.parent = tag_list[obj['parent']]

        session.add(tag)
        return tag

    if '__media__' in obj:
        media = Media(obj['title'], obj['type'])

        if 'file' in obj:
            media.file = obj['file']

        if 'cover' in obj:
            media.cover = obj['cover']

        if 'description' in obj:
            media.description = obj['description']

        if 'release' in obj:
            media.release = int(obj['release'])

        if 'rated' in obj:
            media.rated = obj['rated']

        if 'tags' in obj:
            for tag in obj['tags']:
                if tag in tag_list:
                    media.tags.append(tag_list[tag])
                else:
                    new_tag = Tag(tag)
                    session.add(new_tag)
                    tag_list[tag] = new_tag
                    media.tags.append(new_tag)

        if 'id' in obj:
            media_list[obj['id']] = media

        if 'parent' in obj:
            if obj['parent'] in media_list:
                media.parent = media_list[obj['parent']]

        session.add(media)
        return media

    return obj

try:
    os.unlink('medialib.db')
except OSError: pass

try:
    os.unlink('medialib.db-journal')
except OSError: pass

engine = create_engine('sqlite:///medialib.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
session.flush()

datafile = open('medialib.json', 'r')
objects = json.load(datafile, object_hook=as_object)

session.flush()
session.commit()
