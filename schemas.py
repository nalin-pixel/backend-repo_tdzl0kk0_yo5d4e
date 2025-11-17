"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Portfolio project schema
class Project(BaseModel):
    """
    Portfolio projects schema
    Collection name: "project"
    """
    title: str = Field(..., description="Project title")
    subtitle: Optional[str] = Field(None, description="Short subtitle or tagline")
    description: str = Field(..., description="Detailed description of the app")
    image_url: Optional[HttpUrl] = Field(None, description="Cover image URL")
    tags: List[str] = Field(default_factory=list, description="Tech stack or categories")
    playstore_url: Optional[HttpUrl] = Field(None, description="Google Play Store link")
    mediafire_url: Optional[HttpUrl] = Field(None, description="MediaFire download link")
    website_url: Optional[HttpUrl] = Field(None, description="Optional website/demo link")
    featured: bool = Field(False, description="Mark as featured to show first")
