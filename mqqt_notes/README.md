## Mosquito Configuration.

For those that dont want to use authenfitication on the Mosquito / MQTT broker, copy the attach file into the `<root>/devlab/data/mqtt/<site>/config` directory. You can also delete the password file.

Note you can direct all the payloads via a single broker by changing the `export MQTT_BROKER_PORT=1883` port number in the 3 siteX.sh files located in `<root>/app_iot1/`

If you don't want to create the password file simply copy the `password_file` from this directory into the above mentioned config directory.


## MQTT Source and Sink connectors Notes

https://nightlies.apache.org/flink/flink-docs-master/docs/dev/table/sourcessinks/
https://nightlies.apache.org/flink/flink-docs-master/docs/dev/datastream/sources/



[davidfantasy](https://gitee.com/davidfantasy/flink-connector-mqtt)
[davidfantasy](https://github.com/davidfantasy/flink-connector-mqtt)
[Jar File](https://repo1.maven.org/maven2/com/github/davidfantasy/flink-connector-mqtt/1.1.0/flink-connector-mqtt-1.1.0.jar)



[BG shared](https://gist.github.com/Ugbot/7340025ff225283f56c3a8445f50348e)

[Git repo](https://github.com/kevin4936/kevin-flink-connector-mqtt3)
[Jar File](https://repo1.maven.org/maven2/io/github/kevin4936/kevin-flink-connector-mqtt3_2.12/1.14.4.1/kevin-flink-connector-mqtt3_2.12-1.14.4.1.jar)

