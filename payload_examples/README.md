# Examples

- Base Payload, Factories 101 and 104

```json5
{
    "ts": 1729312551000, 
    "metadata": {
        "siteId": 101, 
        "deviceId": 1004, 
        "sensorId": 10034, 
        "unit": "BAR"
    }, 
    "measurement": 120
}
```

- Modified Payload, Factories 102 and 105

```json5
{
    "ts": 1713807946000, 
    "metadata": {
        "siteId": 102, 
        "deviceId": 1008, 
        "sensorId": 10073, 
        "unit": "Liter", 
        "ts_human": "2024-04-22T19:45:46.000000", 
        "location": {
            "latitude": -33.924869, 
            "longitude": 18.424055
        }
    }, 
    "measurement": 25
}
```

- Full Payload, Factories 103 and 106

```json5
{
    "ts": 1707882120000, 
    "metadata": {
        "siteId": 103, 
        "deviceId": 1014, 
        "sensorId": 10124, 
        "unit": "Amp", 
        "ts_human": "2024-02-14T05:42:00.000000", 
        "location": {
            "latitude": -33.9137, 
            "longitude": 25.5827
        }, 
        "deviceType": "Hoist_Motor"
    },
    "measurement": 24
}
```
