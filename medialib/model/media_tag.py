from storm.locals import Int

class MediaTag(object):
    __storm_table__ = 'media_tag'
    __storm_primary__ = 'media_id', 'tag_id'
    media_id = Int()
    tag_id = Int()
