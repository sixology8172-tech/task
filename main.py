from rectangle import Rectangle
from quadtree import Quadtree

# Mock rendering function provided externally
def render_rectangle(rect):
    # In production, this would call a graphics API
    pass

class DocumentViewer:
    """
    Document Viewer controller, handles data loading and scrolling.
    """
    def __init__(self, total_width, total_height):
        self.total_width = total_width
        self.total_height = total_height
        self.tree = Quadtree(total_width, total_height)

    def load_widgets(self, widgets_data):
        """
        Load all widgets.
        Input format: List of tuples [(id, x, y, w, h), ...]
        """
        for data in widgets_data:
            # Unpack tuple: id, x, y, w, h
            id_val, x, y, w, h = data
            rect = Rectangle(id_val, x, y, w, h)
            self.tree.insert(rect)

    def on_scroll(self, offset_x, offset_y, screen_width, screen_height):
        """
        Scroll handler.
        Queries the Quadtree for visible rectangles, renders them, and returns their IDs.
        """
        visible_rects = self.tree.query(offset_x, offset_y, screen_width, screen_height)
        
        visible_ids = []
        for rect in visible_rects:
            # Performance critical section
            render_rectangle(rect)
            visible_ids.append(rect.id)
            
        return visible_ids

# ==========================================
# Test Cases
# ==========================================

if __name__ == "__main__":
    print("Starting tests...")

    # --- Example 1 ---
    # Input: totalWidth=1000, totalHeight=1000
    # rects=[(1,10,10,100,100),(2,200,50,150,80),(3,300,300,400,400)]
    # Viewport: (0,0,256,256)
    
    viewer = DocumentViewer(1000, 1000)
    input_rects = [
        (1, 10, 10, 100, 100),
        (2, 200, 50, 150, 80),
        (3, 300, 300, 400, 400)
    ]
    viewer.load_widgets(input_rects)
    
    result = viewer.on_scroll(0, 0, 256, 256)
    # Expected: [1, 2]
    print(f"Example 1 Output IDs: {sorted(result)}") 

    # --- Example 2 ---
    # Input: totalWidth=5000, totalHeight=5000
    # rects=[(1,4900,4900,200,200), (2,1000,1000,500,500), (3,2500,2500,10,10)]
    # Viewport: offsetX=4800, offsetY=4800, screenWidth=400, screenHeight=400
    
    viewer2 = DocumentViewer(5000, 5000)
    input_rects_2 = [
        (1, 4900, 4900, 200, 200),
        (2, 1000, 1000, 500, 500),
        (3, 2500, 2500, 10, 10)
    ]
    viewer2.load_widgets(input_rects_2)
    
    # Viewport slightly exceeds bounds (5200 > 5000), internal clipping expected
    result2 = viewer2.on_scroll(4800, 4800, 400, 400)
    # Expected: [1] (rect 2 and 3 are far away)
    print(f"Example 2 Output IDs: {sorted(result2)}")