# Mosquito Configuration.

For those that dont want to use authenfitication on the Mosquito / MQTT broker, copy the attach file into the <root>/devlab/data/mqtt/<site>/config directory. You can also delete the password file.

Note you can direct all the payloads via a single broker by changing the `export MQTT_BROKER_PORT=1883` port number in the 3 siteX.sh files located in <root>/app_iot1/

If you don't want to create the password file simply copy the `password_file` from this directory into the above mentioned config directory.