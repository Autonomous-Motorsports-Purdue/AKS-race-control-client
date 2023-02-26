#usr/bin/env python3
import rclpy
import logging
import paho.mqtt.client as mqtt
from rclpy.node import Node

def on_message(client, userdata, message):
    print(str(message.payload.decode("utf-8")))

def on_disconnect(client, userdata, rc):
    client.loop_stop()
    client.disconnect()

class RCS_Node(Node):
    def __init__(self):
        super().__init__("rs_relay")
        
        client_name = "rcs_node"
        mqtt_host = "10.42.0.1"
        mqtt_topic = "race_state"

        self.mqttclient = mqtt.Client("rcs_node")
        self.mqttclient.on_disconnect = on_disconnect
        self.mqttclient.on_message = on_message
        self.mqttclient.connect(mqtt_host)
        self.mqttclient.loop_start()
        self.mqttclient.subscribe(mqtt_topic)
        self.mqttclient.publish(mqtt_topic, "Data Recieved!")

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