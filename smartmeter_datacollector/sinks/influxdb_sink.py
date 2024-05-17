#
# Copyright (C) 2024 Supercomputing Systems AG
# This file is part of smartmeter-datacollector.
#
# SPDX-License-Identifier: GPL-2.0-only
# See LICENSES/README.md for more information.
#
import logging
from configparser import SectionProxy
from dataclasses import dataclass
from collections import deque
import datetime
import time

from influxdb import InfluxDBClient

from ..smartmeter.meter_data import MeterDataPoint
from .data_sink import DataSink

LOGGER = logging.getLogger("sink")


@dataclass
class InfluxdbConfig:
    db_host: str
    db_name: str

    @staticmethod
    def from_sink_config(config: SectionProxy) -> "InfluxdbConfig":
        influxdb_cfg = InfluxdbConfig(config.get("dbhost"), config.get("dbname"))
        return influxdb_cfg


class DataManagement:
    """Temporarily stores and uploads data points to the data base.
    Do not create multiple instances due to the serial interface being available only once."""

    def __init__(self, database_name, database_host, data_points=deque([])):
        self.data_points_deque = data_points
        self.dbname = database_name
        self.hostname = database_host
        self._client = InfluxDBClient(host=self.hostname, port=8086, database=self.dbname, timeout=1)

    def send_data(self):
        influx_writing_start_time = time.perf_counter()
        LOGGER.info("Trying to write '%i' items to DB.", len(self.data_points_deque))

        for i in range(len(self.data_points_deque)):
            temp_data = self.data_points_deque.popleft()
            try:
                influx_writing_single_start_time = time.perf_counter()
                self._client.write_points(temp_data)
                influx_writing_single_end_time = time.perf_counter()
                LOGGER.info("1 data point written within '%0.3f' seconds.",
                            (influx_writing_single_end_time - influx_writing_single_start_time))
                if ((time.perf_counter() - influx_writing_start_time) > 5.0) and len(self.data_points_deque) > 0:
                    LOGGER.warning("Writing to the database exceeded max allowed time. Keeping %i items for"
                                   "later transmission.", len(self.data_points_deque))
                    break
            except:
                self.data_points_deque.appendleft(temp_data)
                LOGGER.warning("Writing to the database did not work. Keeping %i items for later transmission.",
                               len(self.data_points_deque))
                break
        self._client.close()
        influx_writing_end_time = time.perf_counter()
        LOGGER.info("Total DB transmit time: '%0.3f' seconds",
                    (influx_writing_end_time - influx_writing_start_time))


class InfluxdbSink(DataSink):

    def __init__(self, config: InfluxdbConfig) -> None:
        self.dbname = config.db_name
        self.hostname = config.db_host
        self.timestamp_last_sent = time.time()
        self._data_manager = DataManagement(self.dbname, self.hostname)

    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        pass

    async def send(self, data_point: MeterDataPoint) -> None:
        LOGGER.debug("Preparing data point for InfluxDB")
        dp_json = self.data_point_to_influxdb_json(data_point)
        if bool(dp_json):
            LOGGER.debug("Json content: '%s'", dp_json)
            self._data_manager.data_points_deque.append(dp_json)

        if bool(len(self._data_manager.data_points_deque)):
            if ((time.time() - self.timestamp_last_sent) > 29.0) or len(self._data_manager.data_points_deque) > 20:
                self._data_manager.send_data()
                self.timestamp_last_sent = time.time()
                LOGGER.debug("Time of data sent: %s",
                             datetime.datetime.fromtimestamp(self.timestamp_last_sent))

    @staticmethod
    def data_point_to_influxdb_json(data_point: MeterDataPoint) -> list:

        if data_point.type.identifier == "ACTIVE_POWER_P":
            truncated_timestamp = round(data_point.timestamp.timestamp() / 5) * 5
            return [
                {
                    "measurement": "readings",
                    "tags": {
                        "device": "landisgyre450"
                    },
                    "time": datetime.datetime.fromtimestamp(truncated_timestamp,
                                                            tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "fields": {
                        "total_active_power": data_point.value
                    }
                }]
        elif data_point.type.identifier == "ACTIVE_POWER_N":
            truncated_timestamp = round(data_point.timestamp.timestamp() / 5) * 5
            return [
                {
                    "measurement": "readings",
                    "tags": {
                        "device": "landisgyre450"
                    },
                    "time": datetime.datetime.fromtimestamp(truncated_timestamp,
                                                            tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "fields": {
                        "total_active_power_export": data_point.value
                    }
                }]
        elif data_point.type.identifier == "ACTIVE_ENERGY_P":
            truncated_timestamp = round(data_point.timestamp.timestamp() / 5) * 5
            return [
                {
                    "measurement": "readings",
                    "tags": {
                        "device": "landisgyre450"
                    },
                    "time": datetime.datetime.fromtimestamp(truncated_timestamp,
                                                            tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "fields": {
                        "total_active_energy": data_point.value
                    }
                }]
        elif data_point.type.identifier == "ACTIVE_ENERGY_N":
            truncated_timestamp = round(data_point.timestamp.timestamp() / 5) * 5
            return [
                {
                    "measurement": "readings",
                    "tags": {
                        "device": "landisgyre450"
                    },
                    "time": datetime.datetime.fromtimestamp(truncated_timestamp,
                                                            tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "fields": {
                        "total_active_energy_export": data_point.value
                    }
                }]
        else:
            return []
