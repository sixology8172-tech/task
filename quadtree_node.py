from rectangle import Rectangle

class QuadtreeNode:
    """
    Quadtree node representing a rectangular region on the canvas.
    """
    def __init__(self, bounds, depth, max_depth, capacity):
        self.bounds = bounds          # Node coverage area
        self.depth = depth
        self.max_depth = max_depth
        self.capacity = capacity
        
        # Rectangles in this node (usually straddling child boundaries)
        self.objects = []
        
        # Children: NW, NE, SW, SE. None indicates a leaf node.
        self.children = None 

    def insert(self, rect):
        """
        Insert a rectangle into this node or its children.
        """
        # If divided, try to insert into a specific child
        if self.children is not None:
            index = self._get_quadrant_index(rect)
            if index != -1:
                self.children[index].insert(rect)
                return

        # Add to current node if it's a leaf or the rect straddles boundaries
        self.objects.append(rect)

        # Subdivide if capacity exceeded and max depth not reached
        if (len(self.objects) > self.capacity and 
            self.depth < self.max_depth and 
            self.children is None):
            self._subdivide()

    def _subdivide(self):
        """
        Split node into 4 quadrants and redistribute objects.
        """
        x = self.bounds.x
        y = self.bounds.y
        w = self.bounds.width
        h = self.bounds.height
        
        half_w = int(w / 2)
        half_h = int(h / 2)

        # Create 4 children: NW, NE, SW, SE
        self.children = []
        # NW
        self.children.append(QuadtreeNode(Rectangle(-1, x, y, half_w, half_h), self.depth + 1, self.max_depth, self.capacity))
        # NE
        self.children.append(QuadtreeNode(Rectangle(-1, x + half_w, y, half_w, half_h), self.depth + 1, self.max_depth, self.capacity))
        # SW
        self.children.append(QuadtreeNode(Rectangle(-1, x, y + half_h, half_w, half_h), self.depth + 1, self.max_depth, self.capacity))
        # SE
        self.children.append(QuadtreeNode(Rectangle(-1, x + half_w, y + half_h, half_w, half_h), self.depth + 1, self.max_depth, self.capacity))

        # Redistribute objects: push down fits, keep straddlers
        remaining_objects = []
        for rect in self.objects:
            index = self._get_quadrant_index(rect)
            if index != -1:
                self.children[index].insert(rect)
            else:
                remaining_objects.append(rect)
        
        self.objects = remaining_objects

    def _get_quadrant_index(self, rect):
        """
        Determine quadrant index.
        Returns: 0=NW, 1=NE, 2=SW, 3=SE, -1=Straddles boundary
        """
        vertical_midpoint = self.bounds.x + int(self.bounds.width / 2)
        horizontal_midpoint = self.bounds.y + int(self.bounds.height / 2)

        # Check vertical position
        top_quadrant = (rect.y < horizontal_midpoint and rect.get_bottom() <= horizontal_midpoint)
        bottom_quadrant = (rect.y >= horizontal_midpoint)

        # Check horizontal position
        if rect.x < vertical_midpoint and rect.get_right() <= vertical_midpoint:
            if top_quadrant: 
                return 0 # NW
            if bottom_quadrant: 
                return 2 # SW
        elif rect.x >= vertical_midpoint:
            if top_quadrant: 
                return 1 # NE
            if bottom_quadrant: 
                return 3 # SE

        return -1 # Straddles boundary

    def query(self, viewport, found_rects):
        """
        Recursively query for rectangles intersecting the viewport.
        """
        # Pruning: ignore if node doesn't intersect viewport
        if not self.bounds.intersects(viewport):
            return

        # Check objects in current node
        for rect in self.objects:
            if rect.intersects(viewport):
                found_rects.append(rect)

        # Recurse into children
        if self.children is not None:
            for child in self.children:
                # Optimization: check bounds before recursing
                if child.bounds.intersects(viewport):
                    child.query(viewport, found_rects)