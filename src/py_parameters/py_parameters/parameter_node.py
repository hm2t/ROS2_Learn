"""
ROS2 参数演示节点

本节点演示如何在 ROS2 中使用参数(Parameters)。
参数用于存储和修改节点的配置信息，可在运行时通过命令行修改。
"""

import rclpy
from rclpy.node import Node

# 导入参数类型和描述符
from rcl_interfaces.msg import ParameterType, ParameterDescriptor


class ParameterNode(Node):
    """ROS2 参数演示节点类"""

    def __init__(self):
        # 初始化节点，节点名为 "parameter_node"
        super().__init__("parameter_node")

        # =========================================================
        # 第1步：声明参数
        # =========================================================
        # 使用 declare_parameter() 声明参数，参数必须先声明才能使用
        # 语法：declare_parameter("参数名", 默认值, ParameterDescriptor(元数据))

        # 字符串类型参数：机器人名称
        self.declare_parameter(
            "robot_name",      # 参数名
            "turtle",          # 默认值
            ParameterDescriptor(
                name="robot_name",
                type=ParameterType.PARAMETER_STRING,  # 参数类型为字符串
                description="机器人的名称",           # 参数描述
                read_only=False,                       # 可读写
            ),
        )

        # 浮点类型参数：发布频率(Hz)
        self.declare_parameter(
            "publish_rate",
            10.0,
            ParameterDescriptor(
                name="publish_rate",
                type=ParameterType.PARAMETER_DOUBLE,
                description="状态发布频率 (Hz)",
                read_only=False,
            ),
        )

        # 布尔类型参数：调试模式开关
        self.declare_parameter(
            "enable_debug",
            False,
            ParameterDescriptor(
                name="enable_debug",
                type=ParameterType.PARAMETER_BOOL,
                description="是否启用调试输出",
                read_only=False,
            ),
        )

        # 整数类型参数：最大速度(只读)
        self.declare_parameter(
            "max_speed",
            100,
            ParameterDescriptor(
                name="max_speed",
                type=ParameterType.PARAMETER_INTEGER,
                description="机器人最大速度",
                read_only=True,  # 只读，运行时不可修改
            ),
        )

        # =========================================================
        # 第2步：读取参数的初始值
        # =========================================================
        robot_name = self.get_parameter("robot_name").get_parameter_value().string_value
        publish_rate = self.get_parameter("publish_rate").get_parameter_value().double_value
        enable_debug = self.get_parameter("enable_debug").get_parameter_value().bool_value
        max_speed = self.get_parameter("max_speed").get_parameter_value().integer_value

        # 打印获取到的参数值
        self.get_logger().info(f"机器人名称: {robot_name}")
        self.get_logger().info(f"发布频率: {publish_rate} Hz")
        self.get_logger().info(f"调试模式: {enable_debug}")
        self.get_logger().info(f"最大速度: {max_speed}")

        # =========================================================
        # 第3步：创建定时器，定期执行回调函数
        # =========================================================
        # create_timer(间隔时间, 回调函数)
        # 间隔 = 1.0 / publish_rate，每秒发布 publish_rate 次
        self.timer = self.create_timer(1.0 / publish_rate, self.timer_callback)

        # =========================================================
        # 第4步：注册参数修改回调
        # =========================================================
        # 当通过 ros2 param set 修改参数时，会触发此回调
        self.add_on_set_parameters_callback(self.parameter_callback)

    def timer_callback(self):
        """定时器回调函数，每秒执行一次"""
        # 获取当前的参数值(可能已被修改)
        robot_name = self.get_parameter("robot_name").get_parameter_value().string_value
        enable_debug = self.get_parameter("enable_debug").get_parameter_value().bool_value

        # 如果开启调试模式，打印调试信息
        if enable_debug:
            self.get_logger().debug(f"调试信息: {robot_name} 运行中")

        # 打印状态日志
        self.get_logger().info(f"{robot_name} 正在运行")

    def parameter_callback(self, params):
        """
        参数修改回调函数

        当使用 ros2 param set 修改参数时自动调用。
        可用于响应参数变化并执行相应操作。

        Args:
            params: 参数列表，包含被修改的参数信息

        Returns:
            SetParametersResult: 指示参数设置是否成功
        """
        for param in params:
            if param.name == "robot_name":
                self.get_logger().info(f"机器人名称已修改为: {param.value}")
            elif param.name == "publish_rate":
                self.get_logger().info(f"发布频率已修改为: {param.value} Hz")
                # 更新定时器间隔以应用新频率
                rate = param.value
                self.timer.cancel()  # 取消当前定时器
                # 创建新的定时器
                self.timer = self.create_timer(1.0 / rate, self.timer_callback)
            elif param.name == "enable_debug":
                self.get_logger().info(f"调试模式已修改为: {param.value}")

        # 返回成功结果，允许参数修改
        return rclpy.parameter.SetParametersResult(success=True)


def main(args=None):
    """程序入口函数"""
    # 初始化 rclpy
    rclpy.init(args=args)

    # 创建节点实例
    node = ParameterNode()

    # 打印使用说明
    print("\n" + "=" * 60)
    print("ROS2 参数演示")
    print("=" * 60)
    print("\n可用参数列表:")
    print("  - robot_name (字符串): 机器人名称")
    print("  - publish_rate (浮点数): 发布频率 (Hz)")
    print("  - enable_debug (布尔值): 是否启用调试输出")
    print("  - max_speed (整数): 最大速度 (只读)")
    print("\n修改参数命令:")
    print("  ros2 param set /parameter_node <参数名> <值>")
    print("=" * 60 + "\n")

    try:
        # 保持节点运行，持续处理回调
        rclpy.spin(node)
    except KeyboardInterrupt:
        # 收到 Ctrl+C 时优雅关闭
        node.get_logger().info("正在关闭参数节点")
    finally:
        # 清理资源
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
