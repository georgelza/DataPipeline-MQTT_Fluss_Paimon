
#######################################################################################################################
#
#
#  	Project     	    : 	TimeSeries Data generation via Python Application 
#
#   File                :   simulate.py
#
#   Description         :   
#
#   Original Created   	:   22 November 2024
#   Modified            :   12 April 2025
#
#   Changelog           :   Modified from original from previous blog that posted to Mongo and 2nd Previus posted to Kafka
#                       :   to now to post to
#
#   JSON Viewer         :   https://jsonviewer.stack.hu
#
#   Notes               :   Python Logging Package: 
#                       :   https://docs.python.org/3/library/logging.html
#                       :   https://realpython.com/python-logging/
#
########################################################################################################################

__author__      = "George Leonard"
__email__       = "georgelza@gmail.com"
__version__     = "3.1.0"
__copyright__   = "Copyright 2024, - G Leonard"


import utils
import connection
import time, random, sys
from datetime import datetime, timedelta, timezone
import random
import json
from time import perf_counter

# Function to check if the current time is within the specified time range for the site
# Business/operational hours or 24 hour site
def is_within_time_range(start_time_str, end_time_str, current_time=None):
    
    # Convert the string representations of start_time and end_time to time objects
    start_time  = datetime.strptime(start_time_str, "%H:%M").time()
    end_time    = datetime.strptime(end_time_str, "%H:%M").time()

    # just make sure we're not comparing against Null.
    if current_time is None:
        current_time = datetime.now().time()  # Get only the time part
        
    else:
        current_time = current_time.time()  # Ensure current_time is a time object

    # end if
    
    # Check if the current time is within the specified time range
    if start_time <= end_time:       # Return true... we're suppose to work/generate data between these times
        return start_time <= current_time <= end_time 
    
    else: # Check if end_time is less than start_time, meaning the time range spans midnight
        return current_time >= start_time or current_time <= end_time

    # end if
    return False    # Should never get here, but just in case

# end is_within_time_range


# Helper to convert local time with timezone to UTC
def convert_to_utc(local_time_with_tz):
    return local_time_with_tz.astimezone(timezone.utc)

# Example function to generate payloads with timezone in the timestamp
def generate_payload(site, device, sensor, current_time, time_zone_offset, config_params):
        
   # Adjust the timestamp to include the site's local timezone offset
    offset_hours, offset_minutes = map(int, time_zone_offset.split(":"))
    tz_offset                    = timezone(timedelta(hours=offset_hours, minutes=offset_minutes))
    local_time_with_tz           = current_time.replace(tzinfo=tz_offset)
    ts_human                     = local_time_with_tz.strftime("%Y-%m-%dT%H:%M:%S.%f")
    
    if site["data_persistence"] == 1:
        # If output to file then we passin a text formated date/time string.
        ts = ts_human

    else:   
#        ts = ts_human
        utc_time = convert_to_utc(local_time_with_tz) # Convert to UTC        
        ts = int(utc_time.timestamp() * 1000) # Convert to timestamp (milliseconds)
    #end 
    
    measurement = progress_value(sensor, current_time, device["sfd_start_time"], device["sfd_end_time"], device["stabilityFactor"])

    payload = {
        "ts": ts,  # Timestamp now includes the correct timezone
        "metadata": {
            "siteId":   site["siteId"],
            "deviceId": device["deviceId"],
            "sensorId": sensor["sensorId"],
            "unit":     sensor["unit"],
        },
        "measurement": measurement
    }

    if config_params["TSHUMAN"] == 1:
        payload["metadata"]["ts_human"] = ts_human
        
    if config_params["STRUCTMOD"] == 1:
        payload["metadata"]["location"] = site["location"]
        
    if config_params["DEVICETYPE"] == 1:
        payload["metadata"]["deviceType"] = device["deviceType"]
        
    return payload

# end generate_payload


"""
Generate a sensor value, 
Scaling sd based on stability_factor if the current time is within device start_time and end_time.
If start_time and end_time are not provided for the device, no scaling is applied.
"""
def progress_value(sensor, current_time_local, sfd_start_time_str, sfd_end_time_str, stabilityFactor):
 
    # Convert string time to datetime.time
    # sfd is Stabality Factor, which is used as a time start/end when we want to imply to scale/deviate from normal behaviour.
    sfd_start_time  = datetime.strptime(sfd_start_time_str, "%H:%M").time()
    sfd_end_time    = datetime.strptime(sfd_end_time_str, "%H:%M").time()

    # Ensure current_time_local is a time object
    current_time_local_time = current_time_local.time()

    # Proceed only if the current time is within the specified range
    if sfd_start_time <= current_time_local_time <= sfd_end_time:

        # Calculate the sensor value based on deviation_weight and stabilityFactor
        mean             = sensor['mean']
        sd               = sensor['sd']
        min_value        = sensor['min_range']
        max_value        = sensor['max_range']
        deviation_weight = sensor.get('deviation_weight', 5)  # Default to 5 if not specified
        
        # Adjust mean based on deviation_weight - 5 being stay stable, keep around defined mean
        if deviation_weight == 5:
            new_mean = mean
            
        elif deviation_weight > 5:      # when deviating scale it upwards - between 5 and 10
            weight_factor = (deviation_weight - 5) / 5.0
            new_mean = mean + weight_factor * (max_value - mean)
            
        else:                           # when deviating scale it downwards - between 5 and 0     
            weight_factor = (5 - deviation_weight) / 5.0
            new_mean = mean - weight_factor * (mean - min_value)

        # end if
        
        # Adjust for stabilityFactor < 50 => 50%
        if stabilityFactor < 50:
            if deviation_weight > 7:        # This increases the scaling
                new_mean = min(new_mean, max_value + (deviation_weight - 7) * sd)
                
            elif deviation_weight < 3:      # This increases the scaling
                new_mean = max(new_mean, min_value - (3 - deviation_weight) * sd)

            # end if
        # end if
        
        # Generate value based on the new mean and sd
        value = random.gauss(new_mean, sd)

        # Clamp the value to be within the min and max range
        value = max(min_value, min(value, max_value))

        return value
    else:
        # Return the default mean if outside the time range
        return sensor['mean']

    # end if
# end progress_value


""" 
Function to run simulation for a specific site, this is main body of the generator
"""
def run_simulation(site, current_time, config_params):
    
    topic   = config_params["MQTT_TOPIC"] + "/" + str(site["siteId"])

    # Create new site specific logger's
    logger = utils.logger(config_params["LOGGINGFILE"] + "_" + str(site["siteId"]) + ".log", site["console_debuglevel"], site["file_debuglevel"])
        
    logger.info("simulate.run_simulation - Starting Simulation")
    
    logger.debug('simulate.run_simulation - Printing Complete site seed record for site')
    
    utils.pp_json(site, logger)
    
    site_time_zone = site["time_zone"]
        
    # Parse the start_datetime and begin simulation
    if "historic_data_start_datetime" in site:
        oldest_time = datetime.strptime(site["historic_data_start_datetime"], "%Y-%m-%dT%H:%M")
        
    else:
        oldest_time = current_time

    # Determine time range for simulation, if we specify this then the site/device/sensor only create measurements
    # ... within the specified time range, otherwise we run the simulation for the full day range/24 hours.

    run_limited_time = False        
    if "operational_start_time" in site and "operational_end_time" in site:
        run_limited_time = True
        
        operational_start_time  = site["operational_start_time"]
        operational_end_time    = site["operational_end_time"]
        
    # end if

    historical_record_counter   = 0
    current_record_counter      = 0
    total_record_counter        = 0
    connection_saver            = None
                
    connection_saver = connection.mqtt_connect(config_params, site, logger)      
    
    print("errrrrrr ",connection_saver)
    
    if connection_saver == -1:
        logger.critical(f"SiteId: {str(site["siteId"])} - run_simulation.mqtt_connect Failed, exiting.")
        sys.exit(1)
                                
    # end if

    
    # Historical phase
    if "historic_data_start_datetime" in site and site["historic_data_start_datetime"]:

        step1starttime  = datetime.now()
        step1start      = perf_counter()
            
        logger.info("simulate.run_simulation - Execute Historical Phase,   Starting from {historic_data_start_datetime}".format(
            historic_data_start_datetime = site["historic_data_start_datetime"]
        ))
    
        
        while oldest_time < current_time:
            oldest_time += timedelta(milliseconds=site["sleeptime"])    
 
            # chec if we're specified a start end day for day
            if run_limited_time:
                # yes, so now check if current time is inside/outside, if outsice then we skip via continue call
                if not is_within_time_range(operational_start_time, operational_end_time, oldest_time):
                    continue
                
                    print("Skipping record outside time range, this should never happen/print")
                # end if
            # end if
            
            for device in site["devices"]:
                for sensor in device["sensors"]:
                    
                    payload = generate_payload(site, device, sensor, oldest_time, site_time_zone, config_params)
                    
                    if site["data_persistence"] > 1:
                        result  = connection.mqtt_publish(connection_saver, json.dumps(payload), topic, logger)

                    historical_record_counter   += 1
                    total_record_counter        += 1
                    
                    sensor["last_value"] = payload["measurement"]
                    
                # end for
            # end for
            
            oldest_time += timedelta(milliseconds=site["sleeptime"])

        # end while
        
        logger.info("simulate.run_simulation - COMPLETED Historical Phase, Started from {historic_data_start_datetime}, Created {historical_record_counter} records".format(
            historic_data_start_datetime = site["historic_data_start_datetime"],
            historical_record_counter    = historical_record_counter
        ))     

        step1endtime = datetime.now()
        step1end     = perf_counter()
        step1time    = step1end - step1start  
        histrate     = str( round(historical_record_counter/step2time, 2))

    # end Historical phase
    
    
    # Current phase  
    
    current_record_counter = 0
    if site["reccap"] > 0:
         
        step2starttime  = datetime.now()
        step2start      = perf_counter()
        oldest_time     = datetime.now()

        logger.info("simulate.run_simulation - Execute Current Phase")
        
        for loop in range(site["reccap"]):
            current_loop_time = oldest_time + timedelta(milliseconds=site["sleeptime"] * loop)

            if run_limited_time:
                if not is_within_time_range(operational_start_time, operational_end_time, current_loop_time):
                    continue
                
                    print("Skipping record outside time range, this should never happen/print")
                # end if
            # end if
            
            for device in site["devices"]:
                for sensor in device["sensors"]:
    
                    payload = generate_payload(site, device, sensor, current_loop_time, site_time_zone, config_params)

                    if site["data_persistence"] > 1:
                        result  = connection.mqtt_publish(connection_saver, json.dumps(payload), topic, logger)
            
                    current_record_counter  += 1
                    total_record_counter    += 1
            
                    logger.debug("simulate.run_simulation - Cur Ph: Payload {payload}".format(
                        payload = payload
                    ))
                    sensor["last_value"] = payload["measurement"]
                    
                # end for
            # end for
            
            time.sleep(site["sleeptime"] / 1000)  # Convert milliseconds to seconds


        # end for
     
        
        # Post last batch of records in our mydocs variable to our connection store
        if site["data_persistence"] > 0 :
            result = connection.mqtt_publish(connection_saver, payload, topic, logger)
                
        # end if
        
        step2endtime = datetime.now()
        step2end     = perf_counter()
        step2time    = step2end - step2start  
        currate      = str( round(current_record_counter/step2time, 2))
    # end if


    if site["data_persistence"] > 0:
        connection.mqtt_close(connection_saver, site, logger)

    # end if       


    # Historical phase stats
    if "historic_data_start_datetime" in site and site["historic_data_start_datetime"]:
        logger.info("simulate.run_simulation - Historical Record Process Stats - St: {start}, Et: {end}, Rt: {runtime}, Recs: {historical_record_counter} docs, Rate: {histrate} docs/s".format(
            start                     = str(step1starttime.strftime("%Y-%m-%d %H:%M:%S.%f")),
            end                       = str(step1endtime.strftime("%Y-%m-%d %H:%M:%S.%f")),
            runtime                   = str(round(step1time, 4)),
            historical_record_counte  = historical_record_counter,
            histrate                  = histrate
        ))
    # end if
    
    # Current phase stats
    if site["reccap"] > 0: 
        logger.info("simulate.run_simulation - Current Record Process Stats    - St: {start}, Et: {end}, Rt: {runtime}, Recs: {current_record_counter} docs,    Rate: {currate}  docs/s".format(
            start                  = str(step2starttime.strftime("%Y-%m-%d %H:%M:%S.%f")),
            end                    = str(step2endtime.strftime("%Y-%m-%d %H:%M:%S.%f")),
            runtime                = str(round(step2time, 4)),
            current_record_counter = current_record_counter,
            currate                = currate
        ))
    # end if
    
    # Final stats
    logger.info("simulate.run_simulation - COMPLETED Simulation       - Records: {historical_record_counter} + {current_record_counter} = {total_record_counter} records".format(
        historical_record_counter = historical_record_counter,
        current_record_counter    = current_record_counter,
        total_record_counter      = total_record_counter
    ))

# end run_simulation