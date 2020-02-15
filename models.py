from exts import db


class ActivityInfo(db.Model):
    __tablename__='activity_info'
    activityId = db.Column(db.Integer, primary_key=True)
    activityType = db.Column(db.String)
    activitySubType = db.Column(db.String)
    group = db.Column(db.String)
    date = db.Column(db.Date)
    expiredAt = db.Column(db.DateTime)
    createdBy = db.Column(db.String)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)


class ActivityDetail(db.Model):
    __tablename__='activity_detail'
    activityDetailId = db.Column(db.Integer, primary_key=True)
    activityId = db.Column(db.String)
    employeeId = db.Column(db.String)
    quantity = db.Column(db.String)
    createdBy = db.Column(db.String)
    createdAt = db.Column(db.DateTime)
    updatedBy = db.Column(db.String)
    updatedAt = db.Column(db.DateTime)


class UserInfo(db.Model):
    __tablename__='user_info'
    employeeId = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    group = db.Column(db.String)
    role = db.Column(db.String)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)



