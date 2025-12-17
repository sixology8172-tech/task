

## 1. Justification for Max Depth = 10

**Resolution vs. Diminishing Returns**

The choice of 10 for maximum depth is derived from the physical dimensions of the canvas and the resulting pixel resolution of the leaf nodes. I just assumed that the canvas size would be less than 5000 * 5000 as common monitor sizes on the market. Also an example said 5000. 

* **Spatial Resolution**: A Quadtree with a depth of 10 divides the global canvas width by a factor of 2^10 (1024)

* **Pixel Density**: For a large canvas typical of 5000 * 5000, a leaf node at depth 10 represents a physical width of approximately:

5000 / 1024 = 4.8 pixels

This is already reasonably small and splitting further won't make more sense cause most rectangles won't fall into that smaller division. However if we make this smaller, we cannot handle some reasonable border cases.

---

## 2. Justification for Bucket capacity = 16

**High level thought**

When picking a bucket capacity, the go-to is usually a power of 2 (like 8, 16, or 32). I'm just following the pattern that computers handle powers of 2 much more efficiently in terms of memory alignment.

Main goal is to keep the capacity large enough to avoid drowning in recursive calls (which are expensive in Python), but small enough that we don't waste time checking objects that aren't even on the screen.

I made a calculation based on the 500,000 constraint in the problem document. 


* **8: Not enough buffer**

Depth Calculation: $\log_4(500,000 / 8) \approx \mathbf{8}$Analysis: A capacity of 8 forces the tree to reach depth of 8 levels very quickly. Depends on the distribution of rectangles, this is not a safe buffer with depth 10.

* **16: The Balanced Choice**

Log Calculation: $\log_4(500,000 / 16) \approx \mathbf{7.4}$Analysis: This is more balanced. The tree grows to 7-8 levels, which is deep enough to provide surgical precision for queries, and allows more buffer to hold the whole capacity (500,000)

* **32: Too lazy / blurry**

Log Calculation: $\log_4(500,000 / 32) \approx \mathbf{6.9}$Analysis: With a capacity of 32, the tree becomes "lazy," stopping at only 6-7 levels. We are wasting more than 30% of available depth resolution. Nodes stay physically large, forcing the CPU to check 32 items even if only a tiny corner of the node is on screen.


----


Also as a side note, I did a memory analysis of nodes based on capacity. For example, assume each node in Python costs 256B, then with number of rects to be 500,000, capacity to be 16:
total leaf nodes to be approximately 500000/16 = 31250. The storage of nodes would be 8MB. It's not a problem in modern computers. So memory is not major concern here.