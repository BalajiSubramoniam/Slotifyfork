# app/models/course.py
# 
# Author: Indrajit Ghosh
# Created On: May 17, 2025
# 
import uuid

# Local application imports
from app.extensions import db

class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=lambda: uuid.uuid4().hex)

    # Identifiers
    code = db.Column(db.String(20), unique=True, nullable=False)  # e.g., "PhD-MATH", "MStat"
    name = db.Column(db.String(100), nullable=False)              # Full name of the course
    short_name = db.Column(db.String(50), nullable=True)          # Optional short name, e.g., "PhD Math"

    # Classification
    level = db.Column(db.String(20), nullable=False)              # e.g., "UG", "PG", "PhD"
    department = db.Column(db.String(100), nullable=False)        # e.g., "Mathematics", "Statistics"

    # Duration and timing
    duration_years = db.Column(db.Integer, nullable=True)         # e.g., 2, 5

    # Administrative
    is_active = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text, nullable=True)

    # Relationships
    users = db.relationship('User', back_populates='course', lazy=True)

    def __repr__(self):
        return f"<Course {self.code}: {self.name}>"
    
    def to_json(self):
        """
        Convert the Course instance into a JSON-serializable dictionary.
    
        Returns:
            dict: A dictionary representation of the course, including:
                - uuid (str): UUID of the course.
                - code (str): Unique code identifier of the course.
                - name (str): Full name of the course.
                - short_name (str | None): Optional short name.
                - level (str): Course level, e.g., 'UG', 'PG', 'PhD'.
                - department (str): Department offering the course.
                - duration_years (int | None): Duration in years.
                - is_active (bool): Whether the course is currently active.
                - description (str | None): Optional description.
        """
        return {
            "uuid": self.uuid,
            "code": self.code,
            "name": self.name,
            "short_name": self.short_name,
            "level": self.level,
            "department": self.department,
            "duration_years": self.duration_years,
            "is_active": self.is_active,
            "description": self.description,
        }
    
    
    @classmethod
    def from_json(cls, data):
        """
        Create a Course instance from a JSON dictionary.
    
        Args:
            data (dict): JSON dictionary typically generated by `to_json()`.
    
        Returns:
            Course: A new Course instance with attributes populated from `data`.
                    The instance is not yet added to the database session.
    
        Raises:
            ValueError: If required fields are missing or invalid.
        """
        required_fields = ["uuid", "code", "name", "level", "department"]
        missing = [field for field in required_fields if field not in data or data[field] is None]
        if missing:
            raise ValueError(f"Missing required fields for Course import: {missing}")
    
        return cls(
            uuid=data.get("uuid"),
            code=data.get("code"),
            name=data.get("name"),
            short_name=data.get("short_name"),
            level=data.get("level"),
            department=data.get("department"),
            duration_years=data.get("duration_years"),
            is_active=data.get("is_active", True),
            description=data.get("description"),
        )
    