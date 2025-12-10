from rectangle import Rectangle
from quadtree_node import QuadtreeNode

class Quadtree:
    """
    Quadtree manager class.
    Responsible for initializing the root node and providing external insert and query interfaces.
    """
    def __init__(self, total_width, total_height, bucket_capacity=16):
        # Create the root node covering the entire canvas
        # id is -1 representing it's not a real widget
        root_bounds = Rectangle(-1, 0, 0, total_width, total_height)
        
        # Limit max depth to 8-10 layers, sufficient for large canvases
        self.root = QuadtreeNode(root_bounds, depth=0, max_depth=10, capacity=bucket_capacity)
        
        self.total_width = total_width
        self.total_height = total_height

    def insert(self, rect):
        """Insert a rectangle, internally handling invalid data."""
        if not rect.is_valid():
            return
        
        # Insert the rectangle into the root node, starting recursion
        self.root.insert(rect)

    def query(self, offset_x, offset_y, screen_width, screen_height):
        """
        Execute region query, returning a list of Rectangle objects.
        """
        # 1. Handle viewport boundaries (Clipping)
        # If viewport coordinates are negative, correct to 0
        valid_x = max(0, offset_x)
        valid_y = max(0, offset_y)
        
        # Calculate viewport bottom-right, ensuring it doesn't exceed total canvas width/height
        right_edge = min(self.total_width, offset_x + screen_width)
        bottom_edge = min(self.total_height, offset_y + screen_height)
        
        valid_w = right_edge - valid_x
        valid_h = bottom_edge - valid_y

        # If viewport is completely outside the canvas, width or height will be <= 0
        if valid_w <= 0 or valid_h <= 0:
            return []

        # Construct viewport rectangle object for querying
        viewport_rect = Rectangle(-1, valid_x, valid_y, valid_w, valid_h)
        
        results = []
        self.root.query(viewport_rect, results)
        return results