import turtle
import random
import math

class Particle:
    def __init__(self, target_x, target_y, particle_id):
        self.x = random.uniform(-300, 300)
        self.y = random.uniform(-300, 300)
        self.vx = 0
        self.vy = 0
        self.target_x = target_x
        self.target_y = target_y
        self.id = particle_id
        self.locked = False
        self.precision_mode = False  # Switch to slow precise mode near target
        
        self.dot = turtle.Turtle()
        self.dot.shape("circle")
        self.dot.color("cyan")
        self.dot.shapesize(0.4)
        self.dot.penup()
        self.dot.goto(self.x, self.y)
    
    def distance(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx*dx + dy*dy)
    
    def distance_to_target(self):
        dx = self.x - self.target_x
        dy = self.y - self.target_y
        return math.sqrt(dx*dx + dy*dy)
    
    def update(self, particles):
        if self.locked:
            self.dot.color("lime")
            return
        
        dist_to_target = self.distance_to_target()
        
        # LOCKED: Reached exact position
        if dist_to_target < 2:
            self.locked = True
            self.x = self.target_x
            self.y = self.target_y
            self.vx = 0
            self.vy = 0
            self.dot.goto(self.x, self.y)
            self.dot.color("lime")
            return
        
        # Switch to precision mode when close
        if dist_to_target < 30:
            self.precision_mode = True
            self.dot.color("orange")  # Visual indicator
        
        # Calculate direction to target
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        
        if dist_to_target > 0:
            # Normalized direction
            dir_x = dx / dist_to_target
            dir_y = dy / dist_to_target
            
            # Speed based on mode
            if self.precision_mode:
                # SLOW and precise
                move_speed = min(1.5, dist_to_target * 0.3)  # Proportional to distance
                target_force = 0.8
            else:
                # FAST movement
                move_speed = 6
                target_force = 1.0
            
            # Apply force toward target
            self.vx += dir_x * target_force
            self.vy += dir_y * target_force
        
        # Collision avoidance
        sep_x, sep_y = 0, 0
        
        for other in particles:
            if other == self or other.locked:
                continue
            
            dist = self.distance(other)
            
            # Avoid collision
            if dist < 25 and dist > 0:
                push_strength = (25 - dist) / dist  # Stronger when closer
                sep_x += (self.x - other.x) * push_strength
                sep_y += (self.y - other.y) * push_strength
        
        # Apply separation (stronger in precision mode)
        if self.precision_mode:
            self.vx += sep_x * 2.0
            self.vy += sep_y * 2.0
        else:
            self.vx += sep_x * 1.0
            self.vy += sep_y * 1.0
        
        # Damping (friction) - stronger in precision mode
        if self.precision_mode:
            self.vx *= 0.85
            self.vy *= 0.85
        else:
            self.vx *= 0.95
            self.vy *= 0.95
        
        # Speed limit
        speed = math.sqrt(self.vx**2 + self.vy**2)
        
        if self.precision_mode:
            max_speed = 3  # Slow limit
        else:
            max_speed = 8  # Fast limit
        
        if speed > max_speed:
            self.vx = (self.vx / speed) * max_speed
            self.vy = (self.vy / speed) * max_speed
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Keep in bounds
        self.x = max(-400, min(400, self.x))
        self.y = max(-300, min(300, self.y))
        
        self.dot.goto(self.x, self.y)

# Setup
screen = turtle.Screen()
screen.setup(800, 600)
screen.bgcolor("black")
screen.tracer(0)
screen.title("Self-Assembly: Fast → Precise")

# Create target positions
particles = []
num_particles = 50
radius = 150

for i in range(num_particles):
    angle = (i / num_particles) * 2 * math.pi
    target_x = math.cos(angle) * radius
    target_y = math.sin(angle) * radius
    particles.append(Particle(target_x, target_y, i))

# Draw targets
target_drawer = turtle.Turtle()
target_drawer.hideturtle()
target_drawer.penup()
target_drawer.color("yellow")
for p in particles:
    target_drawer.goto(p.target_x, p.target_y)
    target_drawer.dot(5)

# Info text
info = turtle.Turtle()
info.hideturtle()
info.penup()
info.color("white")
info.goto(-350, 250)
info.write("CYAN = Fast mode | ORANGE = Precision mode | GREEN = Locked", font=("Arial", 10))

# Main loop
frame = 0
while True:
    all_locked = True
    for particle in particles:
        particle.update(particles)
        if not particle.locked:
            all_locked = False
    
    screen.update()
    frame += 1
    
    if all_locked:
        print(f"✓ Assembly complete in {frame} frames!")
        break
    
    if frame > 3000:
        print("Timeout")
        break

turtle.done()