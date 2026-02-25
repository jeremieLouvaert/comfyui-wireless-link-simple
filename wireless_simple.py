"""
Simple Wireless Link Node for ComfyUI
Send stores a file path string. Get retrieves it.
No passthrough needed - Send is a terminal/sink node.
"""

# Global storage dictionary
WIRELESS_STORAGE = {}


class WirelessSend:
    """Store a file path string to a named channel. No output needed."""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "channel": ("STRING", {"default": "channel_1"}),
                "path":    ("STRING", {"default": ""}),
            }
        }

    RETURN_TYPES = ()       # No outputs — nothing to connect
    FUNCTION = "send"
    CATEGORY = "wireless"
    OUTPUT_NODE = True      # Tells ComfyUI to always execute this node
                            # even though it has no connected output

    def send(self, channel, path):
        WIRELESS_STORAGE[channel] = path
        print(f"[WirelessSend] Stored to '{channel}': {path}")
        return ()


class WirelessGet:
    """Retrieve a file path string from a named channel."""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "channel": ("STRING", {"default": "channel_1"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("path",)
    FUNCTION = "get"
    CATEGORY = "wireless"

    @classmethod
    def IS_CHANGED(cls, channel):
        # Always re-run so we never return a stale cached value
        import time
        return time.time()

    def get(self, channel):
        path = WIRELESS_STORAGE.get(channel, None)

        if path is None:
            available = list(WIRELESS_STORAGE.keys())
            raise ValueError(
                f"WirelessGet: channel '{channel}' is empty. "
                f"Available channels: {available}"
            )

        print(f"[WirelessGet] Retrieved from '{channel}': {path}")
        return (path,)


# Node mappings
NODE_CLASS_MAPPINGS = {
    "WirelessSend": WirelessSend,
    "WirelessGet": WirelessGet,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WirelessSend": "📤 Wireless Send",
    "WirelessGet": "📥 Wireless Get",
}
