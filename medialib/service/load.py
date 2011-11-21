from ..model import Tag, File, Media, Rating, Subrating

class ImportJson(object):

    def __init__(self, session):
        self.session = session
        self.subrating_list = dict()
        self.rating_list = dict()
        self.tag_list = dict()
        self.media_list = dict()

    def to_media_object(self, obj):
        if '__rating__' in obj:
            rating = Rating(name=obj['name'])

            if 'desc' in obj:
                rating.desc = obj['desc']

            if 'id' in obj:
                self.rating_list[obj['id']] = rating

            self.session.add(rating)
            return rating

        if '__subrating__' in obj:
            subrating = Subrating(name=obj['name'])

            if 'desc' in obj:
                subrating.desc = obj['desc']

            if 'id' in obj:
                self.subrating_list[obj['id']] = subrating

            self.session.add(subrating)
            return subrating

        if '__tag__' in obj:
            tag = Tag(name=obj['name'])

            if 'desc' in obj:
                tag.desc = obj['desc']

            if 'id' in obj:
                self.tag_list[obj['id']] = tag

            if 'parent' in obj:
                if obj['parent'] in self.tag_list:
                    tag.parent = self.tag_list[obj['parent']]

            self.session.add(tag)
            return tag

        if '__media__' in obj:
            media = Media(title=obj['title'], type=obj['type'])
            self.session.add(media)

            if 'files' in obj:
                for filename in obj['files']:
                    new_file = File(filename=filename)
                    self.session.add(new_file)
                    media.files.append(new_file)

            if 'cover' in obj:
                media.cover = obj['cover']

            if 'desc' in obj:
                media.desc = obj['desc']

            if 'release' in obj:
                media.release = int(obj['release'])

            if 'rating' in obj:
                if obj['rating'] in self.rating_list:
                    media.rating = self.rating_list[obj['rating']]
                else:
                    raise ValueError('Invalid rating "%s"' % obj['rating'])

            if 'subratings' in obj:
                for subrating in obj['subratings']:
                    if subrating in self.subrating_list:
                        media.subratings.append(self.subrating_list[subrating])
                    else:
                        raise ValueError('Invalid subrating "%s"' % obj['subrating'])

            if 'tags' in obj:
                for tag in obj['tags']:
                    if tag in self.tag_list:
                        media.tags.append(self.tag_list[tag])
                    else:
                        new_tag = Tag(name=tag)
                        self.session.add(new_tag)
                        self.tag_list[tag] = new_tag
                        media.tags.append(new_tag)

            if 'id' in obj:
                self.media_list[obj['id']] = media

            if 'parent' in obj:
                if obj['parent'] in self.media_list:
                    media.parent = self.media_list[obj['parent']]

            return media

        return obj
