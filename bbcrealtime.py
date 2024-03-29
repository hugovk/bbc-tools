#!/usr/bin/env python3
# encoding: utf-8
"""
What's playing on BBC music radio?
A Python interface for BBC realtime JSONP.
"""
import json
import time
import datetime as dt
from pprint import pprint

import requests


TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


def _station_name(name):
    """Utility to convert station argument for the request URL"""
    if name in ["bbcradio1", "bbcmedia_radio1_mf_p"]:
        return "bbc_radio_one"
    elif name == "bbc1xtra":
        return "bbc_1xtra"
    elif name == "bbcradio2":
        return "bbc_radio_two"
    elif name == "bbcradio3":
        return "bbc_radio_three"
    elif name == "bbc_radio_fourfm":
        return "bbc_radio_four"
    elif name == "bbcmedia_radio4extra_mf_p":
        return "bbc_radio_four_extra"
    elif name == "bbcmedia_radio5live_mf_p":
        return "bbc_radio_five_live"
    elif name == "bbc6music":
        return "bbc_6music"


def _jsonp_to_json(jsonp):
    """Utility to convert JSONP to JSON"""
    output = jsonp
    prefix = "realtimeCallback("
    if output.startswith(prefix):
        output = output[len(prefix) :]
        output = output[:-1]  # Remove trailing ")"
    return output


def bbcrealtime(station):
    """Return JSON data or None if connection error"""
    station = _station_name(station)
    url = f"https://polling.bbc.co.uk/radio/realtime/{station}.jsonp"
    try:
        r = requests.get(url)
        response = _jsonp_to_json(r.text)
        realtime = json.loads(response)["realtime"]
    except requests.exceptions.ConnectionError:
        return None
    return realtime


def nowplaying(station):
    """Return bbcrealtime() or None if nothing playing now"""
    realtime = bbcrealtime(station)
    if realtime and realtime["start"] <= time.time() <= realtime["end"]:
        return realtime
    else:
        return None


def unix_to_utc(unix):
    """Convert Unix time to UTC timestamp"""
    return dt.datetime.fromtimestamp(unix, dt.timezone.utc).strftime(TIMESTAMP_FORMAT)


def output(realtime):
    """Simple way of printing"""
    pprint(realtime)
    if realtime:
        print("Artist:\t", realtime["artist"])
        print("Title:\t", realtime["title"])
        print("Start:\t", unix_to_utc(realtime["start"]))
        now = time.time()
        end = realtime["end"]
        if now <= end:
            print("Now:\t", unix_to_utc(now))
            print("End:\t", unix_to_utc(end))
        else:
            print("End:\t", unix_to_utc(end))
            print("Now:\t", unix_to_utc(now))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="What's playing on BBC music radio? "
        "A Python interface for BBC realtime JSONP.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "station",
        nargs="?",
        default="bbc6music",
        choices=("bbcradio1", "bbc1xtra", "bbcradio2", "bbcradio3", "bbc6music"),
        help="BBC radio station to check",
    )
    args = parser.parse_args()

    brt = bbcrealtime(args.station)
    np = nowplaying(args.station)

    if brt == np:
        print("\nRealtime == Now playing\n")
        output(brt)

    else:
        print("\nRealtime != Now playing")

        print("\nRealtime:")
        output(brt)

        print("\nNow playing:")
        output(np)

# End of file
