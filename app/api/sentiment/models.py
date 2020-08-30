from app import db


class Sentiment(db.Model):

    __tablename__ = "sentiment"

    job_id = db.Column(db.String(50), primary_key=True)
    keyword = db.Column(db.String(128), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="cascade"),
        nullable=False,
    )

    def __init__(self, job_id, keyword, user_id):
        self.job_id = job_id
        self.keyword = keyword
        self.user_id = user_id
