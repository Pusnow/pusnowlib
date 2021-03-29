import asyncio
from datetime import datetime, timedelta
from xml.etree import cElementTree as ElementTree

from aiohttp import ClientSession

BASE_URL = "http://openapitraffic.daejeon.go.kr/api/rest/arrive/getArrInfoByUid?serviceKey=%s&arsId=%s"


async def fetch_bus(session, api_key, ars_id):
    url = BASE_URL % (api_key, ars_id)
    async with session.get(url) as response:
        assert response.status == 200
        body = await response.text()
        xml = ElementTree.fromstring(body)
        result = {"stop": "NO NAME", "bus": []}
        stop_name = None
        print(body)
        for bus in xml.find("msgBody").findall("itemList"):
            bus_no = bus.find("ROUTE_NO").text
            bus_dest = bus.find("DESTINATION").text
            if not stop_name:
                stop_name = bus.find("STOP_NAME").text
            elif stop_name != bus.find("STOP_NAME").text:
                stop_name += "/" + bus.find("STOP_NAME").text

            offer_time_str = bus.find("INFO_OFFER_TM").text
            ext_sec = int(bus.find("EXTIME_SEC").text)

            offer_time = datetime.strptime(offer_time_str,
                                           "%Y-%m-%d %H:%M:%S.%f")
            ext_time = offer_time + timedelta(seconds=ext_sec)
            print(ext_time)
            result["bus"].append({
                "bus": "%s (%s)" % (bus_no, bus_dest),
                "ext": ext_time,
            })
        result["stop"] = stop_name
        return result


async def future_get_buses(api_key, ars_ids=[]):
    async with ClientSession() as session:
        tasks = []
        for ars_id in ars_ids:
            task = asyncio.ensure_future(fetch_bus(session, api_key, ars_id))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
    return responses


def get_buses(api_key, ars_ids=[]):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(future_get_buses(api_key, ars_ids))
    buses = loop.run_until_complete(future)
    return buses


if __name__ == "__main__":
    API_KEY = "6Qxb2ApJ1MjCEhi0CKNhahMZVpJzYrPPTL57Cyj%2B6FYDf1n8gFvQlr8FV9ekyuD3KZyYrAyw6ZsXvfLTAZr7jA%3D%3D"
    ARS_IDS = ["43040", "42860", "42850"]
    for stop in get_buses(API_KEY, ARS_IDS):
        print(stop["stop"])
        for bus in stop["bus"]:
            cur = datetime.now()
            td = bus["ext"] - cur

            sec = td.total_seconds() // 1
            print(TEMPLATE_ENTRY % (bus["bus"], sec // 60, sec % 60))
        print("---")
