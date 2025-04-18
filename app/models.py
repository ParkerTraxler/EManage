from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association table for users and roles
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True))

# Role model
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return f"<Role {self.name}>"

# User model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    azure_id = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy='dynamic'))
    active = db.Column(db.Boolean(), default=True)

    ferpa_requests = db.relationship('FERPARequest', back_populates='user', lazy=True)
    infochange_requests = db.relationship('InfoChangeRequest', back_populates='user', lazy=True)
    withdrawal_requests = db.relationship('MedicalWithdrawalRequest', back_populates='user', lazy=True)
    drop_requests = db.relationship('StudentDropRequest', back_populates='user', lazy=True)

    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)

    def __repr__(self):
        return f"<User {self.name}>"

class FERPARequest(db.Model):
    __tablename__ = 'ferpa_requests'

    id = db.Column(db.Integer, primary_key=True)
    
    # Meta data
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    time = db.Column(db.DateTime, server_default=db.func.now())
    pdf_link = db.Column(db.String(100), nullable=False)
    sig_link = db.Column(db.String(100))

    # Name and campus
    name = db.Column(db.String(25))
    campus = db.Column(db.String(25))

    # Officials
    official_choices = db.Column(db.String(100)) # comma-separated string
    official_other = db.Column(db.String(100))

    # Information
    info_choices = db.Column(db.String(100)) # comma-separated string
    info_other = db.Column(db.String(100))

    # Release
    release_choices = db.Column(db.String(100)) # comma-separated string
    release_other = db.Column(db.String(100))

    # Release and purpose
    release_to = db.Column(db.String(50))
    purpose = db.Column(db.String(25))
    additional_names = db.Column(db.String(50))

    # Essential info
    password = db.Column(db.String(25), nullable=False)
    peoplesoft_id = db.Column(db.String(25), nullable=False)
    date = db.Column(db.Date(), nullable=False)

    # Relationship to User model
    user = db.relationship('User', back_populates='ferpa_requests')

class InfoChangeRequest(db.Model):
    __tablename__ = 'infochange_requests'

    id = db.Column(db.Integer, primary_key=True)

    # Meta data
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    time = db.Column(db.DateTime, server_default=db.func.now())
    pdf_link = db.Column(db.String(100), nullable=False)
    sig_link = db.Column(db.String(100))
    
    # Name and ID
    name = db.Column(db.String(25), nullable=False)
    peoplesoft_id = db.Column(db.String(6), nullable=False)

    # Choice for Name/SSN
    choice = db.Column(db.String(25), nullable=False)

    # Section A: Name Change
    fname_old = db.Column(db.String(25))
    mname_old = db.Column(db.String(25))
    lname_old = db.Column(db.String(25))
    sfx_old = db.Column(db.String(25))

    fname_new = db.Column(db.String(25))
    mname_new = db.Column(db.String(25))
    lname_new = db.Column(db.String(25))
    sfx_new = db.Column(db.String(25))

    # Reason for name change
    nmchg_reason = db.Column(db.String(25))

    # Section B: SSN Change
    ssn_old = db.Column(db.String(11))
    ssn_new = db.Column(db.String(11))

    # Reason for SSN change
    ssnchg_reason = db.Column(db.String(25))

    # Signature/Date
    date = db.Column(db.Date(), nullable=False)

    # Relationship to User model
    user = db.relationship('User', back_populates='infochange_requests')

class MedicalWithdrawalRequest(db.Model):
    __tablename__ = 'withdrawal_requests'

    id = db.Column(db.Integer, primary_key=True)

    # Meta data
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    time = db.Column(db.DateTime, server_default=db.func.now())
    pdf_link = db.Column(db.String(100), nullable=False)
    sig_link = db.Column(db.String(100))
    
    # Name and ID
    name = db.Column(db.String(25), nullable=False)
    peoplesoft_id = db.Column(db.String(6), nullable=False)
    college = db.Column(db.String(50), nullable=False)
    degree = db.Column(db.String(50), nullable=False)
    
    # Address/Personal Info
    city = db.Column(db.String(25), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    zip_code = db.Column(db.String(25), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    
    # Semester Info
    term_year = db.Column(db.String(10), nullable=False)
    last_attended = db.Column(db.Date(), nullable=False)

    # Reason
    reason = db.Column(db.String(25), nullable=False)
    details = db.Column(db.String(100))

    # Additional Information
    financial_assistance = db.Column(db.String(3))
    uh_health_insurance = db.Column(db.String(3))
    campus_housing = db.Column(db.String(3))
    visa_status = db.Column(db.String(3))
    gi_bill_benefits = db.Column(db.String(3))

    # Course to be Withdrawn
    subject = db.Column(db.String(25), nullable=False)
    number = db.Column(db.String(4), nullable=False)
    section = db.Column(db.String(10), nullable=False)

    # Date and Initial
    date = db.Column(db.Date(), nullable=False)
    initial = db.Column(db.String(5), nullable=False)

    # Relationship to User model
    user = db.relationship('User', back_populates='withdrawal_requests')

class StudentDropRequest(db.Model):
    __tablename__ = 'drop_requests'

    id = db.Column(db.Integer, primary_key=True)

    # Meta data
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(10), nullable=False)
    time = db.Column(db.DateTime, server_default=db.func.now())
    pdf_link = db.Column(db.String(100), nullable=False)
    sig_link = db.Column(db.String(100))
    
    # Name and ID
    name = db.Column(db.String(25), nullable=False)
    peoplesoft_id = db.Column(db.String(6), nullable=False)
    
    # Semester Info
    term_year = db.Column(db.String(10), nullable=False)

    # Course to be Withdrawn
    subject = db.Column(db.String(25), nullable=False)
    number = db.Column(db.String(4), nullable=False)
    section = db.Column(db.String(10), nullable=False)

    # Date and Initial
    date = db.Column(db.Date(), nullable=False)
    birthdate = db.Column(db.Date(), nullable=False)

    # Relationship to User model
    user = db.relationship('User', back_populates='drop_requests')