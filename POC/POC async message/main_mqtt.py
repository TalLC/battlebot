# python3

from time import sleep
from paho.mqtt import client as mqtt_client
import threading

class User():
    def __init__(self):
        pass

    @property
    def username(self):
        return self.__username
    
    @property
    def client(self):
        return self.__client
    
    @property
    def broker(self):
        return self.__broker

    @property
    def topic(self):
        return self.__topic
    
    @property
    def password(self):
        return self.__password
    
    @property
    def port(self):
        return self.__port

    @username.setter
    def username(self, username):
        self.__username = username

    @password.setter
    def password(self, password):
        self.__password = password

    @broker.setter
    def broker(self, broker):
        self.__broker = broker
        
    @port.setter
    def port(self, port):
        self.__port = port

    @topic.setter
    def topic(self, topic):
        self.__topic = topic

    def __str__(self):
        return self.username

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        self.__client = mqtt_client.Client()
        # self.__client.username_pw_set(self.username, self.password)
        self.__client.on_connect = on_connect
        self.__client.connect(self.broker, self.port)
        
    def subscribe(self, topic):
        def on_message(client, userdata, msg):
            print(f"{self.username} - Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        self.__client.subscribe(topic)
        self.__client.on_message = on_message
    
    def run(self):
        self.connect_mqtt()
        self.subscribe(self.topic)
        self.__client.loop_forever()    
    
    def stop(self):
        self.__client.disconnect()
        self.__client.loop_stop()
        print("Disconnected from MQTT Broker!")

class Publisher():
    def __init__(self):
        pass

    @property
    def username(self):
        return self.__username
    
    @property
    def password(self):
        return self.__password
    
    @property
    def broker(self):
        return self.__broker
    
    @property
    def port(self):
        return self.__port
    
    @property
    def topic(self):
        return self.__topic
    
    @property
    def client(self):
        return self.__client
    
    @username.setter
    def username(self, username):
        self.__username = username

    @password.setter
    def password(self, password):
        self.__password = password

    @broker.setter
    def broker(self, broker):
        self.__broker = broker
        
    @port.setter
    def port(self, port):
        self.__port = port

    @topic.setter
    def topic(self, topic):
        self.__topic = topic

    def __str__(self):
        return self.username

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        self.__client = mqtt_client.Client()
        self.__client.username_pw_set(self.username, self.password)
        self.__client.on_connect = on_connect
        self.__client.connect(self.broker, self.port)
        
    def publish(self):
        msg_count = 0
        while True:
            sleep(2)
            msg = f"{msg_count}"
            message = f"compteur={msg}"
            res = self.__client.publish(self.topic, message)

            # result: [0, 1]
            status = res[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{self.topic}`")
            else:
                print(f"Failed to send message to topic {self.topic}")
            msg_count += 1
    
    def run(self):
        self.connect_mqtt()
        self.__client.loop_start()
        self.publish()

    def stop(self):
        self.__client.disconnect()
        self.__client.loop_stop()



if __name__ == '__main__':
    userpass1 = "John"
    # USER 1
    user1 = User()
    user1.username = userpass1
    user1.password = userpass1
    user1.broker = 'localhost'
    user1.port = 1883
    user1.topic = [("hello", 0)]

    # USER 2
    userpass2 = "Fitz"
    user2 = User()
    user2.username = userpass2
    user2.password = userpass2
    user2.broker = 'localhost'
    user2.port = 1883
    user2.topic = [("hello", 0)]

    # USER 3
    userpass3 = "Gerald"
    user3 = User()
    user3.username = userpass3
    user3.password = userpass3
    user3.broker = 'localhost'
    user3.port = 1883
    user3.topic = [("hello", 0)]

    # PUBLISHER
    userpass_pub = "admin"
    publisher = Publisher()
    publisher.username = userpass_pub
    publisher.password = userpass_pub
    publisher.broker = 'localhost'
    publisher.port = 1883
    publisher.topic = 'hello'

    # START
    user1_thread = threading.Thread(target=user1.run)
    user1_thread.start()

    user2_thread = threading.Thread(target=user2.run)
    user2_thread.start()

    user3_thread = threading.Thread(target=user3.run)
    user3_thread.start()

    # user2_thread = threading.Thread(target=user2.run)
    # user2_thread.start()

    publisher_thread = threading.Thread(target=publisher.run)
    publisher_thread.start()




