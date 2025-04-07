
---

# 🏀 Multi-Robot Basketball Controller System

This project simulates and controls **two basketball-playing robots** (`robot1` and `robot2`) using a game controller (e.g., Redgear). Each robot is independently controlled, with live dynamic tuning of:

- 🔄 Bot movement (using analog stick)
- ⚙️ Flywheel speed (for shooting)
- 🎯 Frame angle (for aiming)
- 🟠 Ball spawning with a button press

---

## 📦 Requirements

- Game Controller (e.g., Redgear with `joy` driver)
---

## 🚀 Launch Instructions

### 1️⃣ Spawn Both Robots in the Arena

```bash
ros2 launch rbcon_sim launch_and_spawn.launch.py
```

This loads the arena and places both `robot1` and `robot2`.

---

### 2️⃣ Control Robot 1 (`r1`) Using Controller

```bash
ros2 launch controls r1_drive.launch.py
```

### 3️⃣ Control Robot 2 (`r2`) Using Controller

```bash
ros2 launch controls r2_drive.launch.py
```

Each launch file connects the controller to the respective robot and exposes control over movement, aiming, flywheel power, and ball spawn.

---

## 🎮 Controller Mapping

| Controller Input     | Action                               |
|----------------------|--------------------------------------|
| **Left Hat X/Y**     | Control movement (linear X/Y)        |
| **Right Hat X**      | Yaw rotation (angular Z)             |
| **L1**               | Enable movement control              |
| **L2**               | Control flywheel speed (analog)      |
| **R1**               | Spawn ball (`ros2 run sim_controller ball_spawner`) |
| **X**                | Increase frame (turret) angle        |
| **B**                | Decrease frame (turret) angle        |

> 📌 Movement is only enabled when L1 is held.  
> 🏀 Ball is spawned only on R1 press (once per press).  
> 🎯 Frame angle adjustment is discrete and mapped to X/B buttons.

---


## 🛠️ Features

- ✅ Real-time control of two robots using a single controller setup
- ✅ Independent drive, shoot, and angle control for each bot
- ✅ Ball spawn trigger integrated into control flow
- ✅ ROS 2 modular architecture for quick expansion

---

## 🚧 To-Do

- [ ] Improve robot defense detection (opponent proximity)
- [ ] Integrate score tracking logic using vision

---
