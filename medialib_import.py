#!/usr/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from medialib.model import TableBase, Tag, Media, Rating, Subrating
import json
import os

subrating_list = dict()
rating_list = dict()
tag_list = dict()
media_list = dict()

def as_object(obj):
    if '__rating__' in obj:
        rating = Rating(name=obj['name'])

        if 'desc' in obj:
            rating.desc = obj['desc']

        if 'id' in obj:
            rating_list[obj['id']] = rating

        session.add(rating)
        return rating

    if '__subrating__' in obj:
        subrating = Subrating(name=obj['name'])

        if 'desc' in obj:
            subrating.desc = obj['desc']

        if 'id' in obj:
            subrating_list[obj['id']] = subrating

        session.add(subrating)
        return subrating

    if '__tag__' in obj:
        tag = Tag(name=obj['name'])

        if 'desc' in obj:
            tag.desc = obj['desc']

        if 'id' in obj:
            tag_list[obj['id']] = tag

        if 'parent' in obj:
            if obj['parent'] in tag_list:
                tag.parent = tag_list[obj['parent']]

        session.add(tag)
        return tag

    if '__media__' in obj:
        media = Media(title=obj['title'], type=obj['type'])

        if 'file' in obj:
            media.file = obj['file']

        if 'cover' in obj:
            media.cover = obj['cover']

        if 'desc' in obj:
            media.desc = obj['desc']

        if 'release' in obj:
            media.release = int(obj['release'])

        if 'rating' in obj:
            if obj['rating'] in rating_list:
                media.rating = rating_list[obj['rating']]
            else:
                raise ValueError('Invalid rating "%s"' % obj['rating'])

        if 'subratings' in obj:
            for subrating in obj['subratings']:
                if subrating in subrating_list:
                    media.subratings.append(subrating_list[subrating])
                else:
                    raise ValueError('Invalid subrating "%s"' % obj['subrating'])

        if 'tags' in obj:
            for tag in obj['tags']:
                if tag in tag_list:
                    media.tags.append(tag_list[tag])
                else:
                    new_tag = Tag(name=tag)
                    session.add(new_tag)
                    tag_list[tag] = new_tag
                    media.tags.append(new_tag)

        if 'id' in obj:
            media_list[obj['id']] = media

        if 'parent' in obj:
            if obj['parent'] in media_list:
                media.parent = media_list[obj['parent']]

        print(repr(media))
        session.add(media)
        return media

    return obj

try:
    os.unlink('medialib.db')
except OSError: pass

try:
    os.unlink('medialib.db-journal')
except OSError: pass

engine = create_engine('sqlite:///medialib.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

TableBase.metadata.create_all(engine)
session.flush()

datafile = open('medialib.json', 'r')
objects = json.load(datafile, object_hook=as_object)

session.flush()
session.commit()
