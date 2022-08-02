# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import getpass
import json
from typing import List, NamedTuple, Optional, Tuple

from pathpicker import state_files

# This file just outputs some simple log events that are consumed by
# another service for internal logging at Facebook. Use it if you want
# to, or disable it if you want.


class LoggingEvent(NamedTuple):  # TypedDict from Python 3.8 needs to be used here.
    unixname: str
    num: Optional[int]
    eventname: str


def write_to_file(content: str) -> None:
    with open(state_files.get_logger_file_path(), "w") as file:
        file.write(content)


def clear_file() -> None:
    write_to_file("")


events: List[Tuple[str, Optional[int]]] = []


def add_event(event: str, number: Optional[int] = None) -> None:
    events.append((event, number))


def get_logging_dicts() -> List[LoggingEvent]:
    unixname = getpass.getuser()
    return [LoggingEvent(unixname, number, event) for event, number in events]


def output() -> None:
    dicts = get_logging_dicts()
    json_output = json.dumps(
        [
            {"unixname": e.unixname, "num": e.num, "eventname": e.eventname}
            for e in dicts
        ]
    )
    write_to_file(json_output)
