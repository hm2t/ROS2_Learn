"""
ROS2 Parameters Demo Node

This node demonstrates how to use parameters in ROS2.
"""

import rclpy
from rclpy.node import Node

from rcl_interfaces.msg import ParameterType, ParameterDescriptor


class ParameterNode(Node):
    def __init__(self):
        super().__init__("parameter_node")

        # Declare parameters with descriptors
        self.declare_parameter(
            "robot_name",
            "turtle",
            ParameterDescriptor(
                name="robot_name",
                type=ParameterType.PARAMETER_STRING,
                description="Name of the robot",
                read_only=False,
            ),
        )

        self.declare_parameter(
            "publish_rate",
            10.0,
            ParameterDescriptor(
                name="publish_rate",
                type=ParameterType.PARAMETER_DOUBLE,
                description="Rate at which to publish status (Hz)",
                read_only=False,
            ),
        )

        self.declare_parameter(
            "enable_debug",
            False,
            ParameterDescriptor(
                name="enable_debug",
                type=ParameterType.PARAMETER_BOOL,
                description="Enable debug output",
                read_only=False,
            ),
        )

        self.declare_parameter(
            "max_speed",
            100,
            ParameterDescriptor(
                name="max_speed",
                type=ParameterType.PARAMETER_INTEGER,
                description="Maximum robot speed",
                read_only=True,
            ),
        )

        # Read parameters
        robot_name = self.get_parameter("robot_name").get_parameter_value().string_value
        publish_rate = self.get_parameter("publish_rate").get_parameter_value().double_value
        enable_debug = self.get_parameter("enable_debug").get_parameter_value().bool_value
        max_speed = self.get_parameter("max_speed").get_parameter_value().integer_value

        self.get_logger().info(f"Robot name: {robot_name}")
        self.get_logger().info(f"Publish rate: {publish_rate} Hz")
        self.get_logger().info(f"Debug mode: {enable_debug}")
        self.get_logger().info(f"Max speed: {max_speed}")

        # Create a timer to periodically display parameters
        self.timer = self.create_timer(1.0 / publish_rate, self.timer_callback)

        # Add parameter change callback
        self.add_on_set_parameters_callback(self.parameter_callback)

    def timer_callback(self):
        robot_name = self.get_parameter("robot_name").get_parameter_value().string_value
        enable_debug = self.get_parameter("enable_debug").get_parameter_value().bool_value

        if enable_debug:
            self.get_logger().debug(f"Debug info: {robot_name} is running")

        self.get_logger().info(f"{robot_name} is active at rate")

    def parameter_callback(self, params):
        for param in params:
            if param.name == "robot_name":
                self.get_logger().info(f"Robot name changed to: {param.value}")
            elif param.name == "publish_rate":
                self.get_logger().info(f"Publish rate changed to: {param.value} Hz")
                # Update timer rate
                rate = param.value
                self.timer.cancel()
                self.timer = self.create_timer(1.0 / rate, self.timer_callback)
            elif param.name == "enable_debug":
                self.get_logger().info(f"Debug mode changed to: {param.value}")
        return rclpy.parameter.SetParametersResult(success=True)


def main(args=None):
    rclpy.init(args=args)
    node = ParameterNode()

    print("\n" + "=" * 60)
    print("ROS2 Parameters Demo")
    print("=" * 60)
    print("\nAvailable parameters:")
    print("  - robot_name (string): Name of the robot")
    print("  - publish_rate (double): Publish rate in Hz")
    print("  - enable_debug (bool): Enable debug output")
    print("  - max_speed (int): Maximum robot speed (read-only)")
    print("\nTo change parameters, use:")
    print("  ros2 param set /parameter_node <param_name> <value>")
    print("=" * 60 + "\n")

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down parameter node")
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
