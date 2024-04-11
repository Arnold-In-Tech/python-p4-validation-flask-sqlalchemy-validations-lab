from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 

    #  All authors have a name.
    @validates('name')
    def validate_name(self, key, name):
        if len(name) == False:
            raise ValueError("Failed name validation. All authors have a name")

        elif Author.query.filter(Author.name == name).first():
            raise ValueError("Author already exists")
        
        return name
    
    #   Author phone numbers are exactly ten digits.
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone numbers are exactly ten digits")
        return phone_number


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    
    #   Post content is at least 250 characters long.
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters long.")
        return content

    # Post summary is a maximum of 250 characters. db.String(250)
    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Summary must be a maximum of 250 characters.")
        return summary


    # Post category is either Fiction or Non-Fiction.
    @validates('category') 
    def validate_category(self, key, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError("Category must be Fruit or Vegetable.")
        return category 
    
    # Post title is sufficiently clickbait-y 
    @validates('title')
    def validates_title(self, key, title):
        titles = ["Won't Believe", "Secret","Top","Guess"]
        if not any(phrase in title for phrase in titles):
            raise ValueError("Title should be sufficiently clickbait-y and must contain 'Won't Believe', 'Secret', 'Top', or 'Guess'.")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
