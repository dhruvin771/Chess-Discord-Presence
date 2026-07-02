import asyncio
import time
from contextlib import asynccontextmanager
import json
import subprocess
import aiohttp
import requests
from reactivestreams.subscriber import Subscriber
from reactivestreams.subscription import DefaultSubscription, Subscription
from rsocket.extensions.helpers import composite, route
from rsocket.extensions.mimetypes import WellKnownMimeTypes
from rsocket.frame import MAX_REQUEST_N
from rsocket.helpers import single_transport_provider
from rsocket.payload import Payload
from rsocket.rsocket_client import RSocketClient
from rsocket.transports.aiohttp_websocket import TransportAioHttpClient

USER_ID = "YOUR_CHESS_COM_USER_ID"  # Replace with your Chess.com user ID
PRESENCE_URL = "https://www.chess.com/service/presence/users"
GAME_URL = "https://www.chess.com/service/play/games"
COOKIES = {}
HEADERS = {"User-Agent": "Mozilla/5.0"}


@asynccontextmanager
async def rsocket_connect(ws_url: str):
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(ws_url) as websocket:
            async with RSocketClient(
                single_transport_provider(TransportAioHttpClient(websocket=websocket)),
                metadata_encoding=WellKnownMimeTypes.MESSAGE_RSOCKET_COMPOSITE_METADATA,
                fragment_size_bytes=1_000_000,
            ) as client:
                yield client


class LiveMoveSubscriber(Subscriber, Subscription):
    def __init__(self, limit_rate=MAX_REQUEST_N) -> None:
        self._limit_rate = limit_rate
        self._received_count = 0
        self.is_done = asyncio.Event()
        self.error = None
        self.subscription = None

    def on_subscribe(self, subscription: DefaultSubscription):
        self.subscription = subscription
        self.subscription.request(self._limit_rate)

    def on_next(self, value, is_complete=False):
        print("Event payload:", value.data.decode("utf-8"))
        try:
            data = json.loads(value.data.decode("utf-8"))

            print("=" * 60)
            print("White Clock:", data["clocks"][0] / 1000)
            print("Black Clock:", data["clocks"][1] / 1000)

            # Convert moves array to one TCN string
            tcn = "".join(move[0] for move in data["moves"])

            # Decode using Node.js chess-tcn
            pgn = subprocess.check_output(
                ["node", "decoder.js", tcn],
                text=True
            ).strip()

            print("\nPGN:")
            print(pgn)

        except Exception as e:
            print("Decode error:", e)
            print(value.data.decode("utf-8"))

        self._received_count += 1

        if is_complete:
            self.is_done.set()
        elif self._received_count == self._limit_rate:
            self._received_count = 0
            self.subscription.request(self._limit_rate)

    def on_complete(self):
        self.is_done.set()

    def on_error(self, exception: Exception):
        self.error = exception
        self.is_done.set()

    def cancel(self):
        self.subscription.cancel()

    def request(self, n: int):
        self.subscription.request(n)

    async def run(self):
        await self.is_done.wait()
        if self.error:
            raise self.error


async def subscribe_live_moves(ws_url: str, route_name: str):
    print(f"Connecting to {ws_url} ...")
    try:
        async with rsocket_connect(ws_url) as client:
            print(f"Subscribed to {route_name}, waiting for moves...")
            payload = Payload(b"", composite(route(route_name)))
            subscriber = LiveMoveSubscriber()
            client.request_stream(payload).initial_request_n(MAX_REQUEST_N).subscribe(subscriber)
            await subscriber.run()
    except Exception as e:
        print("WebSocket/RSocket error:", e)


def main():
    while True:
        try:
            res = requests.get(
                f"{PRESENCE_URL}?ids={USER_ID}",
                headers=HEADERS,
                cookies=COOKIES,
            )
            res.raise_for_status()
            user = res.json()["users"][0]
        except Exception as ex:
            print("Error fetching presence:", ex)
            time.sleep(5)
            continue

        status = user.get("status", "offline")
        activity = user.get("activity")
        print(f"Status: {status}, Activity: {activity}")

        if activity == "playing":
            game = user["activityContext"]["games"][0]
            game_id = game["numericId"]
            print(
                "Detected game ID:",
                game_id,
                "| Variant:",
                game["variant"],
                "| TimeClass:",
                game["timeclass"],
            )

            info = requests.get(
                f"{GAME_URL}/{game_id}",
                headers=HEADERS,
                cookies=COOKIES,
            ).json()
            route_name = info["transports"]["rsocket"]["routes"]["watch"]
            rsocket_path = info["transports"]["rsocket"]["url"]
            ws_url = f"wss://www.chess.com{rsocket_path}"
            print("RSocket route:", route_name, "| URL:", ws_url)

            asyncio.run(subscribe_live_moves(ws_url, route_name))
            break

        time.sleep(5)

    print("Script finished.")


if __name__ == "__main__":
    main()
