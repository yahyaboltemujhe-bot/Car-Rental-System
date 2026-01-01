"""
Input validation utilities for the application
"""
import re
from app.utils.exceptions import ValidationException


class Validator:
    """Centralized validation class"""
    
    # Regex patterns
    PHONE_PATTERN = re.compile(r'^(\+92|0)?3\d{9}$')
    CNIC_PATTERN = re.compile(r'^\d{5}-\d{7}-\d{1}$')
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    LICENSE_PLATE_PATTERN = re.compile(r'^[A-Z]{2,3}-\d{1,4}$|^[A-Z0-9]{3,10}$')
    
    @staticmethod
    def validate_phone(phone):
        """
        Validate Pakistani phone number
        Formats: 03001234567, +923001234567, 3001234567
        """
        if not phone:
            raise ValidationException('phone', 'Phone number is required')
        
        phone = phone.strip().replace(' ', '').replace('-', '')
        
        if not Validator.PHONE_PATTERN.match(phone):
            raise ValidationException(
                'phone',
                'Invalid phone format. Use: 03XX-XXXXXXX'
            )
        
        return phone
    
    @staticmethod
    def validate_cnic(cnic):
        """
        Validate Pakistani CNIC number
        Format: 12345-1234567-1
        """
        if not cnic:
            raise ValidationException('cnic', 'CNIC is required')
        
        cnic = cnic.strip()
        
        if not Validator.CNIC_PATTERN.match(cnic):
            raise ValidationException(
                'cnic',
                'Invalid CNIC format. Use: 12345-1234567-1'
            )
        
        return cnic
    
    @staticmethod
    def validate_email(email):
        """Validate email address"""
        if not email:
            raise ValidationException('email', 'Email is required')
        
        email = email.strip().lower()
        
        if not Validator.EMAIL_PATTERN.match(email):
            raise ValidationException('email', 'Invalid email format')
        
        return email
    
    @staticmethod
    def validate_license_plate(plate):
        """
        Validate license plate
        Formats: ABC-123, LEA-1234, ABC123
        """
        if not plate:
            raise ValidationException('license_plate', 'License plate is required')
        
        plate = plate.strip().upper()
        
        if not Validator.LICENSE_PLATE_PATTERN.match(plate):
            raise ValidationException(
                'license_plate',
                'Invalid license plate format'
            )
        
        return plate
    
    @staticmethod
    def validate_name(name, field_name='name'):
        """Validate person name"""
        if not name:
            raise ValidationException(field_name, f'{field_name} is required')
        
        name = name.strip()
        
        if len(name) < 2:
            raise ValidationException(field_name, 'Name too short')
        
        if len(name) > 100:
            raise ValidationException(field_name, 'Name too long')
        
        if not re.match(r'^[a-zA-Z\s]+$', name):
            raise ValidationException(
                field_name,
                'Name should contain only letters'
            )
        
        return name
    
    @staticmethod
    def validate_category(category):
        """Validate vehicle category"""
        valid_categories = ['economy', 'luxury', 'suv']
        
        if not category:
            raise ValidationException('category', 'Category is required')
        
        category = category.strip().lower()
        
        if category not in valid_categories:
            raise ValidationException(
                'category',
                f'Invalid category. Must be one of: {", ".join(valid_categories)}'
            )
        
        return category
    
    @staticmethod
    def sanitize_string(text, max_length=None):
        """Sanitize user input to prevent XSS"""
        if not text:
            return text
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';']
        for char in dangerous_chars:
            text = text.replace(char, '')
        
        # Apply max length if specified
        if max_length and len(text) > max_length:
            text = text[:max_length]
        
        return text
