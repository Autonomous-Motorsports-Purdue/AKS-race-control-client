#usr/bin/env python3
import rclpy
import paho.mqtt.client as mqtt
from rclpy.node import Node

def on_message(client, userdata, message):
    RCS_Node.get_logger().info(str(message.payload.decode("utf-8")))

class RCS_Node(Node):
    def __init__(self):
        super().__init__("rs_relay")

        # self.broker_address= self.declare_parameter("~broker_ip_address", '127.0.0.1').value
        # self.MQTT_TOPIC = self.declare_parameter("~mqtt_topic", 'race_state').value
        self.mqttclient = mqtt.Client("rs_relay")
        # self.mqttclient.connect(self.broker_address)
        self.mqttclient.connect("127.0.0.1")
        self.mqttclient.on_message = on_message

        # self.get_logger().info('RS_Relay:: Started...')
        # self.get_logger().info(f'RS_Relay:: broker_address = {self.broker_address}')
        # self.get_logger().info(f'RS_Relay:: MQTT_PUB_TOPIC = {self.MQTT_TOPIC}')

        self.mqttclient.loop_forever()
        self.mqttclient.subscribe("race_state")
        self.mqttclient.publish("race_state", "1")

def main(args=None):
    rclpy.init(args=args)

    try:
        node = RCS_Node()
        rclpy.spin(node)
    except rclpy.exceptions.ROSInterruptException:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()