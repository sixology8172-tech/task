# rectangle.py

class Rectangle:
    """
    Base class representing a rectangular widget.
    """
    def __init__(self, id, x, y, width, height):
        self.id = id
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_right(self):
        """Get the coordinate of the right side (x + width)."""
        return self.x + self.width

    def get_bottom(self):
        """Get the coordinate of the bottom side (y + height)."""
        return self.y + self.height

    def intersects(self, other):
        """
        Check if the current rectangle intersects with another rectangle.
        Principle: If one rectangle is to the left, right, above, or below the other, they do not intersect.
        The inverse implies intersection.
        """
        # If self is to the right of other, or self is to the left of other
        if self.x >= other.get_right() or self.get_right() <= other.x:
            return False
        # If self is below other, or self is above other
        if self.y >= other.get_bottom() or self.get_bottom() <= other.y:
            return False
        
        return True

    def is_valid(self):
        """Check if the rectangle is valid"""
        return self.width > 0 and self.height > 0