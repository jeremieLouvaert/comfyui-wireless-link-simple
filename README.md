# ComfyUI Wireless Link (Simple)

A minimal, working implementation of wireless data links for ComfyUI - similar to Blackmagic Fusion's wireless links.

## What It Does

Send data from one node to another without visible wire connections, keeping your workflow clean and organized.

## Features

- ✅ **Simple**: Just 2 nodes - Send and Get
- ✅ **Universal**: Works with ANY ComfyUI data type (IMAGE, MODEL, LATENT, etc.)
- ✅ **Reliable**: Minimal code = less to break
- ✅ **Pass-through**: Send node passes data through to ensure execution

## Installation

### Step 1: Locate Your ComfyUI Custom Nodes Folder

Navigate to your ComfyUI installation:
```
ComfyUI/
  └── custom_nodes/     ← You want this folder
```

### Step 2: Copy the Files

Copy the entire `comfyui_wireless_link_simple` folder into `custom_nodes/`:

```
ComfyUI/
  └── custom_nodes/
      └── comfyui_wireless_link_simple/
          ├── __init__.py
          ├── wireless_simple.py
          └── README.md
```

### Step 3: Restart ComfyUI

Completely close and restart ComfyUI (not just refresh the browser).

### Step 4: Verify Installation

1. Open ComfyUI
2. Right-click on the canvas → Add Node
3. Look for the "wireless" category
4. You should see:
   - 📤 Wireless Send
   - 📥 Wireless Get

## Usage

### Basic Example

**Step 1:** Add a Wireless Send node after your data source
```
[Load Image] → [📤 Wireless Send]
                  • channel: "my_image"
                  • value: (connected from Load Image)
```

**Step 2:** IMPORTANT - Connect the passthrough output
```
[Load Image] → [📤 Wireless Send] → [Preview Image]
                  channel: "my_image"   ↑
                                     (connect this!)
```

**Step 3:** Add Wireless Get nodes wherever you need the data
```
[📥 Wireless Get] → [Save Image]
   channel: "my_image"

[📥 Wireless Get] → [Another Process]
   channel: "my_image"
```

### Complete Example Workflow

```
┌─────────────────────────────────┐
│ Load and Send                    │
├─────────────────────────────────┤
│ [Load Image: "photo.jpg"]       │
│        ↓                         │
│ [📤 Send: "input"]               │
│        ↓ (passthrough)           │
│ [Preview Image]                  │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ Receive and Use (Section A)     │
├─────────────────────────────────┤
│ [📥 Get: "input"]                │
│        ↓                         │
│ [Image Process A]                │
│        ↓                         │
│ [Save Image: "output_a.png"]    │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ Receive and Use (Section B)     │
├─────────────────────────────────┤
│ [📥 Get: "input"]                │
│        ↓                         │
│ [Image Process B]                │
│        ↓                         │
│ [Save Image: "output_b.png"]    │
└─────────────────────────────────┘
```

### Model/Checkpoint Example

```
[Load Checkpoint]
   ├─ MODEL → [📤 Send: "model"] → [Preview/Any Node]
   ├─ CLIP → [📤 Send: "clip"] → [Preview/Any Node]
   └─ VAE → [📤 Send: "vae"] → [Preview/Any Node]

... elsewhere in workflow ...

[📥 Get: "model"] → [KSampler]
[📥 Get: "clip"] → [CLIP Text Encode]
[📥 Get: "vae"] → [VAE Decode]
```

## Important Rules

### ⚠️ CRITICAL: Always Connect the Passthrough!

The Send node MUST have its `passthrough` output connected to something, or ComfyUI won't execute it.

**❌ WRONG - This won't work:**
```
[Load Image] → [📤 Send: "img"]
                      (nothing connected to passthrough output)

[📥 Get: "img"] → [Save Image]  ← ERROR: channel not found!
```

**✅ CORRECT:**
```
[Load Image] → [📤 Send: "img"] → [Preview]
                                   (passthrough connected)

[📥 Get: "img"] → [Save Image]  ← Works!
```

### Channel Names

- Channel names are **case-sensitive**: "Image1" ≠ "image1"
- Use the **exact same name** on Send and Get nodes
- Choose descriptive names: "processed_image" not "temp1"

### Execution Order

- Send nodes must execute BEFORE Get nodes
- ComfyUI handles this automatically if you connect the passthrough
- Check the console for debug messages to verify execution

## Troubleshooting

### Problem: "Channel not found" error

**Check the console output:**
```
[WirelessGet] WARNING: Channel 'my_image' not found or empty!
[WirelessGet] Available: []
```

This means the Send node never executed.

**Solution:**
1. Connect the Send node's `passthrough` output to ANY other node
2. Common choices: Preview Image, Save Image, or another Send node
3. This forces ComfyUI to execute the Send node

### Problem: Getting None/empty data

**Check the console:**
```
[WirelessSend] Stored to 'my_image': Tensor
[WirelessGet] Retrieved from 'my_image': Tensor
```

If you see the Send message but not the Get message, check your channel names match exactly.

### Problem: Nodes don't appear in menu

**Solution:**
1. Verify files are in the correct location:
   ```
   ComfyUI/custom_nodes/comfyui_wireless_link_simple/__init__.py
   ComfyUI/custom_nodes/comfyui_wireless_link_simple/wireless_simple.py
   ```
2. Check `__init__.py` contains the correct import
3. Restart ComfyUI completely (close the window/process, don't just refresh browser)
4. Check the console for Python errors on startup

### Viewing Debug Messages

Open your ComfyUI console/terminal to see messages like:
```
[WirelessSend] Stored to 'input': Tensor
[WirelessGet] Retrieved from 'input': Tensor
```

These confirm the nodes are working correctly.

## How It Works

1. **Send node** stores data in a Python dictionary with the channel name as key
2. **Send node** passes the data through its output (ensures execution)
3. **Get node** retrieves data from the dictionary using the channel name
4. Data persists in memory during workflow execution
5. Data clears when ComfyUI restarts

## Tips & Best Practices

1. **Name your channels descriptively**
   - ✅ "base_model_checkpoint"
   - ✅ "preprocessed_input_image"
   - ❌ "temp1", "data", "x"

2. **Use Preview nodes to verify Send execution**
   ```
   [Send] → [Preview]  ← Quick way to ensure it runs
   ```

3. **One Send can feed many Gets**
   ```
   [Send: "data"] → [Preview]
   
   [Get: "data"] → [Use 1]
   [Get: "data"] → [Use 2]
   [Get: "data"] → [Use 3]
   ```

4. **Chain Send nodes for multiple channels**
   ```
   [Data] → [Send: "ch1"] → [Send: "ch2"] → [Preview]
   ```

5. **Organize your workflow visually**
   - Put all Send nodes in one area
   - Put all Get nodes near where they're used
   - Use different colors for Send/Get pairs

## Advantages Over Traditional Wiring

### Before (Traditional):
```
[Checkpoint] ──MODEL──────────────────────────┐
            ├─CLIP──────────────┐             │
            ├─CLIP──────┐       │             │
            └─VAE────┐  │       │             │
                     ↓  ↓       ↓             ↓
                 [Decode] [Enc1] [Enc2] [KSampler]
```
Messy, hard to reorganize, wires everywhere.

### After (Wireless):
```
[Checkpoint] → [Send: "model"] → [Preview]
              → [Send: "clip"] → [Preview]
              → [Send: "vae"] → [Preview]

... clean workspace ...

[Get: "model"] → [KSampler]
[Get: "clip"] → [Enc1]
[Get: "clip"] → [Enc2]
[Get: "vae"] → [Decode]
```
Clean, organized, easy to modify.

## Examples

### Example 1: Image Processing Pipeline
```
[Load Image] → [Send: "original"] → [Preview]

[Get: "original"] → [Blur] → [Send: "blurred"] → [Preview]
[Get: "original"] → [Sharpen] → [Send: "sharp"] → [Preview]

[Get: "blurred"] → [Save: "blur.png"]
[Get: "sharp"] → [Save: "sharp.png"]
```

### Example 2: Batch Processing
```
[Config] → [Send: "settings"] → [Preview]

[Get: "settings"] → [Process Batch 1]
[Get: "settings"] → [Process Batch 2]
[Get: "settings"] → [Process Batch 3]
```

### Example 3: Model Sharing
```
[Load Checkpoint]
   ├→ [Send: "model"] → [Preview]
   ├→ [Send: "clip"] → [Preview]
   └→ [Send: "vae"] → [Preview]

[Get: "model"] → [Sampler A]
[Get: "model"] → [Sampler B]
[Get: "clip"] → [All Encoders]
[Get: "vae"] → [All Decoders]
```

## Technical Details

- **Storage**: Global Python dictionary (`WIRELESS_STORAGE`)
- **Lifetime**: Data persists until ComfyUI restart
- **Performance**: Negligible overhead (dictionary lookup)
- **Thread-safe**: ComfyUI executes nodes sequentially
- **Type support**: Any ComfyUI data type via `("*",)` wildcard

## Comparison to Other Solutions

### vs. Traditional Wiring
- ✅ Cleaner visual layout
- ✅ Easier to reorganize
- ✅ Can distribute to multiple targets easily
- ❌ Requires understanding of execution order

### vs. Reroute Nodes
- ✅ No long reroute chains across canvas
- ✅ Better for many-to-many connections
- ✅ Clearer intent (named channels)
- ❌ Slightly more complex concept

### vs. Link/Unlink Nodes
- ✅ Simpler - just Send and Get
- ✅ Named channels make intent clear
- ✅ Easier to debug with console output
- ❌ Requires passthrough connection

## FAQ

**Q: Can I use multiple Get nodes with one Send?**
A: Yes! One Send can feed unlimited Get nodes.

**Q: What happens if I use Get before Send?**
A: You'll get None/empty data. Check console for warnings.

**Q: Do channels persist between workflow runs?**
A: No, they clear when ComfyUI restarts. They persist during a session.

**Q: Can I send multiple data types on one channel?**
A: No, one channel holds one value. Use multiple channels for multiple values.

**Q: Why do I need to connect the passthrough?**
A: ComfyUI only executes nodes that contribute to the final output. The passthrough ensures the Send node runs.

**Q: Can I rename channels?**
A: Yes, just change the channel name on both Send and Get nodes.

**Q: What's the performance impact?**
A: Minimal - just a dictionary lookup. No measurable slowdown.

## License

Free to use and modify for personal and commercial projects.

## Support

If you encounter issues:
1. Check the console for debug messages
2. Verify passthrough is connected
3. Confirm channel names match exactly
4. Test with a simple Load → Send → Get → Save workflow
5. Make sure you restarted ComfyUI after installation

## Credits

Inspired by Blackmagic Fusion's Wireless Link nodes.

---

**Version**: 1.0 Simple
**Last Updated**: 2024
**Compatibility**: ComfyUI (all versions)
#   c o m f y u i - w i r e l e s s - l i n k - s i m p l e  
 