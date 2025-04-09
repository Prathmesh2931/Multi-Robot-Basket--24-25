#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node 
from service_handler.srv import RpmVel
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

class Velocity_ser(Node):
    def __init__(self):
        super().__init__('velocity')
        namespace = self.get_namespace()
        namespace_prefix = f"{namespace}/" if namespace and namespace != '/' else ""
        
        self.call_back=ReentrantCallbackGroup()
        self.create_service(RpmVel,f"{namespace_prefix}RPM",callback=self.calculate_rpm,callback_group=self.call_back)
        
        
    def calculate_rpm(self,request,response):
        self.dist=request.distance
        self.height=request.height
        self.wheel_rad=request.wheel_radius
        self.angle=request.angle
        
        vel,rpm=self.compute_rpm_for_shot(self.dist,self.height,self.angle,self.wheel_rad)
        
        response.vel=vel
        response.rpm=rpm
        response.success=True
        
        return response
    def compute_rpm_for_shot(self,x, y, angle_deg, wheel_radius_m):
        """
        Calculates the required flywheel RPM to shoot a ball into a basket.

        Parameters:
        - x: horizontal distance to the basket (in meters)
        - y: vertical height difference (basket height - launch height) in meters
        - angle_deg: launch angle in degrees
        - wheel_radius_m: radius of flywheel in meters (e.g., 0.05 for 5 cm)

        Returns:
        - required_velocity (m/s): the velocity the ball needs
        - rpm: the RPM for flywheels to achieve that velocity
        """
        g = 9.81  # gravity in m/s^2
        theta = math.radians(angle_deg)

        denominator = 2 * (math.cos(theta)**2) * (x * math.tan(theta) - y)
        
        if denominator <= 0:
            return None, None  # Not physically possible at this angle
        
        velocity = math.sqrt((g * x**2) / denominator)  # m/s

        # Tangential speed v = r * ω, where ω is in rad/s
        # Convert to RPM: rpm = (v / r) * (60 / 2π)
        rpm = (velocity / wheel_radius_m) * (60 / (2 * math.pi))

        return velocity, rpm

def main(args=None):
    rclpy.init(args=args)
    thread=MultiThreadedExecutor()
    node=Velocity_ser()
    thread.add_node(node)
    thread.spin()
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()