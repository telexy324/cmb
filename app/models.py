from app import db


class Type9users1(db.Model):
    __tablename__ = 'type9users1'

    id = db.Column(db.Integer, primary_key=True)
    isp_username = db.Column(db.String(64, 'utf8_bin'))
    state = db.Column(db.Integer)
    isp_password = db.Column(db.String(64, 'utf8_bin'))


