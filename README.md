
---

# 🏀 Multi-Robot Basketball Controller System

A ROS 2-based control system for simulating **two basketball-playing robots** — `robot1` and `robot2`. This system enables dynamic, real-time control using a game controller like Redgear. Each robot can:

- 🔄 Move in all directions  
- ⚙️ Adjust flywheel speed for shooting  
- 🎯 Aim by changing turret angle  
- 🟠 Spawn a ball with a button press  
- 🎯 Automatically align with baskets using service calls  

---

## 📦 Requirements
- Game Controller (e.g., Redgear or Xbox Controller)

---

## 🚀 Launch Instructions

### 1️⃣ Spawn Both Robots in the Arena

```bash
ros2 launch rbcon_sim launch_and_spawn.launch.py
```

This loads the basketball arena and places both `robot1` and `robot2`.

---

### 2️⃣ Control Robot 1 (`r1`) Using the Controller

```bash
ros2 launch controls r1_drive.launch.py
```

### 3️⃣ Control Robot 2 (`r2`) Using the Controller

```bash
ros2 launch controls r2_drive.launch.py
```

Each robot is mapped to its own joystick instance and service namespace.

---

## 🎮 Controller Mapping

| Controller Input     | Action                                                     |
|----------------------|------------------------------------------------------------|
| **Left Stick (X/Y)** | Drive robot (linear X and Y velocity)                      |
| **Right Stick X**    | Rotate robot (angular Z velocity / yaw)                    |
| **L1**               | Enable movement (must be held for any motion to occur)     |
| **L2 (Analog)**      | Control flywheel speed (for shooting)                      |
| **R1**               | Spawn ball (`ros2 run sim_controller ball_spawner`)        |
| **X**                | Increase frame/turret angle                                 |
| **B**                | Decrease frame/turret angle                                 |
| **Y**                | Align with Basket 1 (calls a custom service)               |
| **A**                | Align with Basket 2 (calls a custom service)               |

> 🛑 Movement only occurs when **L1** is held down  
> 🟠 Ball is spawned **once per R1 press**  
> 🎯 Turret angle adjusts incrementally with **X** and **B**  
> 🎯 Basket alignment is triggered via **custom service calls** using **Y** or **A**

---

## ⚙️ Architecture

- ✅ Real-time joystick input using `joy` package  
- ✅ Each robot operates in its own **ROS 2 namespace** (`/r1`, `/r2`)  
- ✅ Flywheel and aiming are fully adjustable  
- ✅ Basket alignment is performed using **custom services**  
- ✅ ROS 2 modular design for clean expansion and debugging  

---

## 📈 Custom Service Integration

| Service Trigger | Description                          |
|-----------------|--------------------------------------|
| **Y Button**     | Align with **Basket 1** via service |
| **A Button**     | Align with **Basket 2** via service |

These services are launched automatically within `r1_drive.launch.py` and `r2_drive.launch.py`, ensuring each robot can self-align based on court position.

---

## 🧪 Example Workflow

```bash
# Launch simulation
ros2 launch rbcon_sim launch_and_spawn.launch.py

# Start controller interface for Robot 1
ros2 launch controls r1_drive.launch.py

# Control robot using joystick
# Press R1 to spawn ball
# Hold L1 + Left Stick to move
# Use Y/A to align with baskets
```

---

## 🛠️ Features

- ✅ Two-robot basketball simulation
- ✅ Individual control over each robot
- ✅ Dynamic tuning for shooting, angle, and ball handling
- ✅ Service-based alignment with baskets
- ✅ Works with any standard game controller

---

## 🚧 To-Do

- [ ] Add defense mechanism based on opponent proximity  
- [ ] Integrate score tracking with vision-based detection  
- [ ] Add camera feed overlay for court vision

---
