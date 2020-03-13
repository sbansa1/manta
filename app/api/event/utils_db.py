from app.extensions import db


class ResourceMixin(object):
    def save(self):

        db.session.add(self)
        db.session.commit()
        return self
