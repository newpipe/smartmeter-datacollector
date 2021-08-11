#
# Copyright (C) 2021 Supercomputing Systems AG
# This file is part of smartmeter-datacollector.
#
# SPDX-License-Identifier: GPL-2.0-only
# See LICENSES/README.md for more information.
#
from abc import ABC, abstractmethod

from smartmeter.reader_data import ReaderDataPoint


class DataSink(ABC):
    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def stop(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def send(self, data_point: ReaderDataPoint) -> None:
        raise NotImplementedError()
