import rclpy 
from  rclpy.node import Node 
import time
import math    
from rcl_interfaces.msg import Parameter, SetParametersResult
from std_msgs.msg import Float32

class map_bot(Node):
    def __init__(self):
        super().__init__('shoot')
     
        self.min_dis=0.3
        self.get_logger().info(f'Node is Intialized')
        self.control_speed=self.create_publisher(Float32,'/dhanush/shoot',15)
        self.create_timer(0.1,self.time)

        self.declare_parameter("control_dhanush_shoot",150.00)
        self.control_shoot=self.get_parameter("control_dhanush_shoot").get_parameter_value().double_value

       
        self.add_on_set_parameters_callback(self.param_call)
       
        self.get_logger().info(f'shoot control is intialized')
       
    
   
    def param_call(self,params:list[Parameter]):
        for param in params:
            param_name=param.name
            param_value=param.value
            setattr(self,param_name,param_value)
            self.control_speed.publish(Float32(data=self.control_shoot))
        return SetParametersResult(successful=True)
    

    def time(self):
        time.sleep(0.1)
        self.control_shoot=self.get_parameter("control_dhanush_shoot").get_parameter_value().double_value

       
        self.add_on_set_parameters_callback(self.param_call)
        msg=Float32()
        msg.data=self.control_shoot
        self.control_speed.publish(msg)
        print(msg)


    
def main(args=None):
    rclpy.init(args=args)
    bot=map_bot()
    rclpy.spin(bot)
    
    rclpy.shutdown()

if __name__=='__main__':
    main()