#usr/bin/env python3
import rclpy
import logging
import paho.mqtt.client as mqtt
from rclpy.node import Node
from std_msgs.msg import String

class RS_relay(Node):
    def __init__(self):
        super().__init__("RS_relay")

        self.declare_parameters(
            namespace='',
            parameters=[
                ('mqtt_host', "127.0.0.1"),                     # ADDRESS TO MQTT BROKER
                ('mqtt_port', 1883),                            # PORT TO MQTT BROKER
                ('team_id', "AMP"),                             # USED FOR CLIENT NAME AND MQTT KART STATE TOPIC
                ('mqtt_track_state_topic', "track_state"),
                ('mqtt_kart_state_topic', "kart_state/"),
                ('ros_topic', "race_state")                     # TOPIC TO PUBLISH STATE DATA WITHIN ROS
            ]
        )

        client_name = self.get_parameter('team_id')
        mqtt_host = self.get_parameter('mqtt_host')
        mqtt_port = self.get_parameter('mqtt_port')
        mqtt_track_topic = self.get_parameter('mqtt_track_state_topic')
        mqtt_kart_topic = str(self.get_parameter('mqtt_kart_state_topic').value) + str(self.get_parameter('team_id').value) # STRING NOT PARAMETER OBJECT LIKE OTHERS

        self.race_state_pub = self.create_publisher(String, str(mqtt_track_topic.value), 1)

        def on_message(client, userdata, message):
            msg = String()
            msg.data = str(message.payload.decode("utf-8"))
            self.get_logger().info(msg.data)
            self.race_state_pub.publish(msg)


        def on_disconnect(client, userdata, rc):
            client.loop_stop()
            client.disconnect()

        # TODO: ADAPT PUBLISH TO PUBLISH KART STATE 
        self.mqttclient = mqtt.Client(client_name.value)
        self.mqttclient.on_disconnect = on_disconnect
        self.mqttclient.on_message = on_message
        self.mqttclient.connect(mqtt_host.value, port = mqtt_port.value)
        self.mqttclient.loop_start()
        self.mqttclient.subscribe(mqtt_track_topic.value)
        self.mqttclient.publish(mqtt_track_topic.value, "Data Recieved!") # WHERE DOES KART STATE COME FROM

def main(args=None):
    rclpy.init(args=args)

    try:
        node = RS_relay()
        rclpy.spin(node)
    except rclpy.exceptions.ROSInterruptException:
        pass

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()