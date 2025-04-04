
## ROS2 template repository for development and deployment

Absolutely! Here's a clear, concise, and professional `README.md` section you can directly use in your GitHub repo:

---

## 🚀 How to Launch the Simulation

Follow the steps below to set up and run the simulation with multiple bots, localization, and control features:

---

### 🔧 1. Launch Arena and Spawn Bots

This command launches Gazebo with the arena and spawns multiple robots with TFs configured for RViz:

```bash
ros2 launch rbcon_sim launch_and_spawn.launch.py
```

---

### 📍 2. Run Localization (SLAM-based)

Run SLAM on a pre-built map to localize all bots:

```bash
ros2 launch zeus_init locate.launch.py
```

---

### 🎮 3. Control the Robots Manually

#### Control Bot 1:
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/r1/cmd_vel
```

#### Control Bot 2:
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/r2/cmd_vel
```

---

### 📏 4. Monitor Distances & Orientation

#### Check distance and orientation of basket with respect to both bots:
```bash
ros2 run sim_controller dist_basket
```

#### Check distance and orientation between bots:
```bash
ros2 run sim_controller relative_dist_bot
```

---

### 🏀 5. Spawn Balls in Arena

Spawn balls relative to the first bot for simulation:

```bash
ros2 run sim_controller ball_spawner
```
