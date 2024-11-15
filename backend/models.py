from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = id.Column(db.String(100), nullbase = True)
    quantity = db.Column(db.Integer, default = 0)