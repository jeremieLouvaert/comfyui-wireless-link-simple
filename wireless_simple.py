"""
ComfyUI Wireless Link (Simple)
Wireless data transfer between nodes — any type, named channels.
Inspired by Blackmagic Fusion's Wireless Link.
"""

import time

# ---------------------------------------------------------------------------
# Universal type — passes ComfyUI's type-checking for any connection
# ---------------------------------------------------------------------------

class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

any_type = AnyType("*")

# ---------------------------------------------------------------------------
# Global channel storage — shared between Send and Get nodes
# ---------------------------------------------------------------------------

WIRELESS_STORAGE = {}

# Execution generation tracker — detects new prompt executions
# so Get nodes can distinguish stale data from fresh data.
_EXEC_GENERATION = [0]
_CHANNEL_GENERATION = {}


def _mark_fresh(channel):
    """Mark a channel as freshly written in this execution."""
    _CHANNEL_GENERATION[channel] = _EXEC_GENERATION[0]


def _is_fresh(channel):
    """Check if a channel was written in the current execution."""
    return _CHANNEL_GENERATION.get(channel) == _EXEC_GENERATION[0]


# ---------------------------------------------------------------------------
# Hook: clear stale data at the start of each prompt execution
# ---------------------------------------------------------------------------

try:
    from server import PromptServer
    from aiohttp import web

    _original_post_prompt = None

    @PromptServer.instance.routes.post("/wireless/clear")
    async def _clear_wireless(request):
        """Manual clear endpoint for debugging."""
        WIRELESS_STORAGE.clear()
        _CHANNEL_GENERATION.clear()
        return web.json_response({"status": "cleared"})

    # Increment generation counter when a new prompt is queued
    # This lets Get nodes detect if their data is from the current run
    if hasattr(PromptServer, 'instance') and PromptServer.instance:
        original_send_sync = PromptServer.instance.send_sync

        def _patched_send_sync(event, data, sid=None):
            if event == "execution_start":
                _EXEC_GENERATION[0] += 1
            return original_send_sync(event, data, sid)

        PromptServer.instance.send_sync = _patched_send_sync

except (ImportError, AttributeError):
    # Running outside ComfyUI — skip hooks
    pass


# ============================================================================
# NODE: WIRELESS SEND
# ============================================================================

class WirelessSend:
    """Store any data to a named wireless channel.
    Connect the passthrough output to guarantee execution order."""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "value": (any_type, {
                    "tooltip": "Any data to send wirelessly (IMAGE, MODEL, LATENT, CLIP, VAE, STRING, etc.)",
                }),
                "channel": ("STRING", {
                    "default": "channel_1",
                    "tooltip": "Channel name — must match exactly on the Get node (case-sensitive)",
                }),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("passthrough",)
    FUNCTION = "send"
    CATEGORY = "wireless"
    OUTPUT_NODE = True

    def send(self, value, channel):
        WIRELESS_STORAGE[channel] = value
        _mark_fresh(channel)

        type_name = type(value).__name__
        if hasattr(value, 'shape'):
            type_name = f"Tensor {list(value.shape)}"

        print(f"[Wireless Send] '{channel}' <- {type_name}")
        return (value,)


# ============================================================================
# NODE: WIRELESS GET
# ============================================================================

class WirelessGet:
    """Retrieve data from a named wireless channel.
    The channel must have been written by a Send node in the same execution."""

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "channel": ("STRING", {
                    "default": "channel_1",
                    "tooltip": "Channel name — must match the Send node exactly (case-sensitive)",
                }),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("value",)
    FUNCTION = "get"
    CATEGORY = "wireless"

    @classmethod
    def IS_CHANGED(cls, channel):
        # Always re-execute to get the latest value
        return time.time()

    def get(self, channel):
        value = WIRELESS_STORAGE.get(channel)

        if value is None:
            available = list(WIRELESS_STORAGE.keys())
            hint = ""
            if available:
                hint = f" Available channels: {available}"
            else:
                hint = " No channels have been sent yet."

            raise ValueError(
                f"[Wireless Get] Channel '{channel}' not found.{hint}\n"
                f"Make sure a Wireless Send node with channel '{channel}' exists "
                f"and has its passthrough output connected."
            )

        if not _is_fresh(channel):
            print(
                f"[Wireless Get] WARNING: '{channel}' contains data from a "
                f"previous execution — it may be stale."
            )

        type_name = type(value).__name__
        if hasattr(value, 'shape'):
            type_name = f"Tensor {list(value.shape)}"

        print(f"[Wireless Get] '{channel}' -> {type_name}")
        return (value,)


# ============================================================================
# MAPPINGS
# ============================================================================

NODE_CLASS_MAPPINGS = {
    "WirelessSend": WirelessSend,
    "WirelessGet": WirelessGet,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "WirelessSend": "Wireless Send",
    "WirelessGet": "Wireless Get",
}
