# ROS2 Workspace

这是一个 ROS2 (Robot Operating System 2) Python 工作空间，包含以下示例包：

## Packages

| Package | Description |
|---------|-------------|
| `py_pubsub` | Publisher/Subscriber 通信示例 |
| `py_srv` | Service/Client 通信示例 |
| `custom_interfaces` | 自定义消息和服务定义 |

## Quick Start

```bash
# 构建工作空间
colcon build

# 激活工作空间
source install/setup.bash

# 运行示例
ros2 run py_pubsub talker      # 发布者节点
ros2 run py_pubsub listener    # 订阅者节点
ros2 run py_srv server         # 服务端节点
ros2 run py_srv client         # 客户端节点
```

## 自定义消息/服务

- `custom_interfaces/msg/Person.msg` - Person 消息类型
- `custom_interfaces/srv/GetPerson.srv` - GetPerson 服务类型

编辑 `.msg`/`.srv` 文件后需重新 `colcon build`。

## 环境要求

- ROS2 (Foxy/Humble/Jazzy)
- Python 3.8+
