# ComfyUI Wireless Link (Simple)

Wireless data transfer between nodes — no visible wires. Inspired by Blackmagic Fusion's Wireless Link.

## What It Does

Two nodes. **Send** stores any data to a named channel. **Get** retrieves it. No wires needed between them.

Works with every ComfyUI data type: IMAGE, MODEL, LATENT, VAE, CLIP, CONDITIONING, STRING, INT, FLOAT — anything.

## Nodes

### Wireless Send

| Input | Type | Description |
|-------|------|-------------|
| `value` | ANY | Data to send (connect any output here) |
| `channel` | STRING | Channel name (case-sensitive) |

| Output | Type | Description |
|--------|------|-------------|
| `passthrough` | ANY | Same data, passed through for execution order |

### Wireless Get

| Input | Type | Description |
|-------|------|-------------|
| `channel` | STRING | Channel name to retrieve from |

| Output | Type | Description |
|--------|------|-------------|
| `value` | ANY | Data from the matching Send node |

## Usage

### Basic: Image Transfer

```
[Load Image] -> [Wireless Send] -> [Preview Image]
                  channel: "photo"   (passthrough)

... elsewhere in workflow ...

[Wireless Get] -> [Save Image]
  channel: "photo"
```

### Model Sharing

```
[Load Checkpoint]
   MODEL -> [Send: "model"] -> [Preview]
   CLIP  -> [Send: "clip"]  -> [Preview]
   VAE   -> [Send: "vae"]   -> [Preview]

... elsewhere ...

[Get: "model"] -> [KSampler]
[Get: "clip"]  -> [CLIP Text Encode]
[Get: "vae"]   -> [VAE Decode]
```

### One Send, Many Gets

```
[Send: "base_image"] -> [Preview]

[Get: "base_image"] -> [Process A]
[Get: "base_image"] -> [Process B]
[Get: "base_image"] -> [Process C]
```

## Important

**Connect the passthrough.** The Send node's passthrough output should be connected to a downstream node (Preview, Save, another node). This guarantees Send executes before Get. Without it, Send still runs (it's marked as an output node) but execution order isn't guaranteed.

**Channel names are case-sensitive.** "MyImage" and "myimage" are different channels.

**Data persists in memory** during a ComfyUI session. Restarting ComfyUI clears all channels. Stale data from previous runs is detected and warned about in the console.

## Installation

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/jeremieLouvaert/comfyui-wireless-link-simple.git
```

Restart ComfyUI. Nodes appear under the **wireless** category.

No additional dependencies required.

## Troubleshooting

**"Channel not found" error** — The Send node didn't execute before Get. Connect the Send node's passthrough output to any downstream node.

**Stale data warning in console** — A channel contains data from a previous execution. Check that the Send node is still in your workflow and connected.

## License

MIT

## Credits

Inspired by Blackmagic Fusion's Wireless Link nodes.
