# Networking-Final-Python

```python
sendEveryUpdate = {
    "position": (float, float),
    "bullets": [
        (float, float),
        (float, float)
    ]
}

receiveEveryUpdate = {
    "players": {
        "<id0>": (float, float),
        "<id1>": (float, float)
    },
    "bullets": [
        (float, float),
        (float, float)
    ]
}

receiveWhenNewJoin = {
    "name": str,
    "id": int
}

sendWhenYouJoin = {
    "name": str,
    "coords": (float, float)
}

receiveWhenYouJoin = {
    "players": {
        "<id0>": (float, float),
        "<id1>": (float, float)
    },
    "bullets": [
        (float, float),
        (float, float)
    ]
}
```
