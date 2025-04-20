########################################################################################################################
#
#
#  	Project     	: 	MQTT Related functionality
#
#   File            :   connection.py
#
#	By              :   George Leonard ( georgelza@gmail.com )
#
#   Created     	:   28 Dec 2024
#
#   Notes       	:
#
#######################################################################################################################
__author__      = "George Leonard"
__email__       = "georgelza@gmail.com"
__version__     = "1.0.0"
__copyright__   = "Copyright 2025, George Leonard"


#Libraries
import paho.mqtt.client as mqtt
import sys
from datetime import datetime
import socket



def on_connect(client, userdata, flags, rc):
    rc_messages = {
        0: "Connection successful",
        1: "Connection refused – incorrect protocol version",
        2: "Connection refused – invalid client identifier",
        3: "Connection refused – server unavailable",
        4: "Connection refused – bad username or password",
        5: "Connection refused – not authorized"
    }

    print(f"Connection result: {rc} – {rc_messages.get(rc, 'Unknown error')}")
    
    if rc == 0:
        try:
            client.subscribe("test/topic")
            print("Subscribed to topic: test/topic")
            
        except Exception as e:
            print(f"Failed to subscribe: {e}")

        #end try
    #end if
#end on_connect


# Define the callback for when a message is published
def on_publish(client, userdata, mid):
    print(f"Message published with ID:{mid}")

#end on_publish

    
############# Instantiate a connection to the MQTT Server ##################
def mqtt_connect(config_params, site, logger):

    
    # Configure the Mqtt connection etc.
    broker          = config_params["MQTT_BROKER_HOST"]
    port            = config_params["MQTT_BROKER_PORT"]
    clienttag       = config_params["MQTT_CLIENTTAG"] + "_" + str(site["siteId"])
    username        = config_params["MQTT_USERNAME"]
    password        = config_params["MQTT_PASSWORD"]

    logger.info("")
    logger.info("#####################################################################")
    logger.info("")
    
        
    logger.info('{time}, connection.connect - ch: {clienttag} Creating connection to MQTT for {siteId}... '.format(
        time        = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")),
        siteId      = site["siteId"],
        clienttag   = clienttag,
    ))
        
    try:
        
        mqtt.Client.connected_flag      = False                     # this creates the flag in the class
        mqtt.Client.bad_connection_flag = False                     # this creates the flag in the class

        mqttc = mqtt.Client(clienttag)                              # create client object client1.on_publish = on_publish #assign function to callback
                                                                    # client1.connect(broker,port) #establish connection client1.publish("house/bulb1","on")            
        
        mqttc.on_connect    = on_connect   
#        mqttc.on_publish    = on_publish   
        mqttc.on_disconnect = on_disconnect                         # Bind callback functions
        
        mqttc.username_pw_set(username, password)
        mqttc.connect(broker, port)                                 # Action connect
        
        
        logger.info("{time}, connection.connect - Connection to MQTT Configured Successfully... Client: {clienttag}, Broker: {broker}, Port: {port}".format(
            time        = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")),
            clienttag   = clienttag,
            broker      = broker,
            port        = port,
        ))

    except socket.gaierror:
        logger.info("{time}, connection.connect - Error - DNS resolution failed – is the broker hostname correct?... Client: {clienttag}, Broker: {broker}, Port: {port}".format(
            time        = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")),
            clienttag   = clienttag,
            broker      = broker,
            port        = port,
        ))
        return -1

    except ConnectionRefusedError:
        logger.info("{time}, connection.connect - Error - Connection was refused – is the port open? Is the broker running... Client: {clienttag}, Broker: {broker}, Port: {port}".format(
            time        = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")),
            clienttag   = clienttag,
            broker      = broker,
            port        = port,
        ))  
        return -1

    except TimeoutError:
        logger.info("{time}, connection.connect - Error - Connection timed out – broker might be unreachable... Client: {clienttag}, Broker: {broker}, Port: {port}".format(
            time        = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")),
            clienttag   = clienttag,
            broker      = broker,
            port        = port,
        ))  
        return -1

    except OSError as e:
        logger.info("{time}, connection.connect - Error - OS error occurred... Client: {clienttag}, Broker: {broker}, Port: {port}, Error: {err}".format(
            time        = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")),
            clienttag   = clienttag,
            broker      = broker,
            port        = port,
            err         = err
        ))  
        return -1

    except Exception as err:
        logger.critical("{time}, connection.connect - Error - Unexpected Connection Err to Broker Failed... Client: {clienttag}, Broker: {broker}, Port: {port}, Err: {err}".format(
            time        = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")),
            clienttag   = clienttag,
            broker      = broker,
            port        = port,
            err         = err,
        ))
        return -1

    finally:

        logger.debug("")
        logger.debug("#####################################################################")
        logger.debug("")

        return mqttc
        
    # end try
#end mqtt_connect


def on_disconnect(client, userdata, flags, rc=0):

    client.connected_flag = False
    
#end on_disconnect


def mqtt_publish(client, payload, topic, logger):
            
    try:

        result = client.publish(topic, str(payload), 0)           # QoS = 0
            
        logger.debug("{time}, connection.publish - MQTT Publish topic: {topic}, Completed: {result}".format(
            time        = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")),
            topic       = topic,
            result      = result,
        ))  
        
        return result
    
    except Exception as err:
        logger.critical('{time}, connection.publish - MQTT Publish topic: {topic}, Failed !!!: {err}'.format(
            time        = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")),
            topic       = topic,
            err         = mqtt.error_string(result.rc)
        ))
    
        return 0
        
    # end try
#end publish


def mqtt_close(client, siteId, logger):

    try:

        client.disconnect()
        
        logger.debug('{time},  connection.close - Connection to MQTT for Site: {siteId} to MQTT Closed... '.format(
            time    = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")),
            siteId  = siteId
        ))
        
    except Exception as err:
        logger.critical('{time}, connection.close - Connection Close for Site: {siteId} to MQTT Failed... {err}'.format(
            time    = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")),
            siteId  = siteId,
            err     = err
        ))

        sys.exit(-1)
        
    # end try
#end close