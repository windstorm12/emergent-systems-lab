import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class Boid:
    def __init__(self, width, height):
        self.x = np.random.uniform(0, width)
        self.y = np.random.uniform(0, height)
        self.vx = np.random.uniform(-2, 2)
        self.vy = np.random.uniform(-2, 2)
        self.width = width
        self.height = height
    
    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return np.sqrt(dx*dx + dy*dy)
    
    def update(self, boids):
        separation_weight = 1.5
        alignment_weight = 1.0
        cohesion_weight = 0.5
        perception = 50
        
        sep_x, sep_y = 0, 0
        align_x, align_y = 0, 0
        coh_x, coh_y = 0, 0
        neighbors = 0
        
        for other in boids:
            if other == self:
                continue
            
            dist = self.distance(other)
            
            if dist < perception and dist > 0:
                neighbors += 1
                sep_x += (self.x - other.x) / dist
                sep_y += (self.y - other.y) / dist
                align_x += other.vx
                align_y += other.vy
                coh_x += other.x
                coh_y += other.y
        
        if neighbors > 0:
            align_x = (align_x / neighbors - self.vx) * alignment_weight
            align_y = (align_y / neighbors - self.vy) * alignment_weight
            coh_x = ((coh_x / neighbors - self.x) * cohesion_weight) * 0.01
            coh_y = ((coh_y / neighbors - self.y) * cohesion_weight) * 0.01
            sep_x *= separation_weight
            sep_y *= separation_weight
        
        self.vx += sep_x + align_x + coh_x
        self.vy += sep_y + align_y + coh_y
        
        speed = np.sqrt(self.vx**2 + self.vy**2)
        max_speed = 4
        if speed > max_speed:
            self.vx = (self.vx / speed) * max_speed
            self.vy = (self.vy / speed) * max_speed
        
        self.x += self.vx
        self.y += self.vy
        
        if self.x < 0: self.x = self.width
        if self.x > self.width: self.x = 0
        if self.y < 0: self.y = self.height
        if self.y > self.height: self.y = 0

# Setup
width, height = 800, 600
boids = [Boid(width, height) for _ in range(100)]

fig, ax = plt.subplots(figsize=(10, 7))
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.set_facecolor('black')
scatter = ax.scatter([], [], c='white', s=20)

def animate(frame):
    for boid in boids:
        boid.update(boids)
    
    positions = np.array([[b.x, b.y] for b in boids])
    scatter.set_offsets(positions)
    return scatter,

ani = animation.FuncAnimation(fig, animate, frames=200, interval=50, blit=True)
plt.show()