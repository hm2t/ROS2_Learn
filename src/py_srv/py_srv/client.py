import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class Client(Node):
    def __init__(self):
        super().__init__('client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        return self.future


def main(args=None):
    rclpy.init(args=args)
    client = Client()
    client.get_logger().info('Calling service')

    future = client.send_request(int(4), int(3))
    rclpy.spin_until_future_complete(client, future)

    result = future.result()
    client.get_logger().info(f'Result: {result.sum}')

    client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
