from app import db
from flask_login import current_user

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    category = db.Column(db.String(50), nullable = False)
    description = db.Column(db.Text, nullable = True)
    skill_type = db.Column(db.String(10), nullable = False) #'offer' or 'Learn'

    # Relationship: each skill belongs to one user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)

    def __repr__(self):
        return f'<skill {self.name} ({self.skill_type})>'