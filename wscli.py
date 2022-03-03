import json
import websocket


class WSRemote:
    def __init__(self):
        self._ws = websocket.WebSocket()
        self._ws.connect("ws://localhost:9000")

    def send(self, message: dict):
        pkt = json.dumps(message)
        self._ws.send(pkt)

    def recv(self) -> dict:
        return json.loads(self._ws.recv())

    # def set_posture(
    #     self, pitch: float, yaw: float, roll: float, x: float, y: float, z: float
    # ):
    #     self._ws_send(dict(pitch=pitch, yaw=yaw, roll=roll, x=x, y=y, z=z))
