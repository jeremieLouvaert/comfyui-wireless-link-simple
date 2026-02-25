# QUICK START GUIDE

## Installation (3 Steps)

### 1. Find Your ComfyUI Folder
```
ComfyUI/
  └── custom_nodes/  ← Go here
```

### 2. Copy the Folder
Copy the entire `comfyui_wireless_link_simple` folder into `custom_nodes/`:
```
ComfyUI/
  └── custom_nodes/
      └── comfyui_wireless_link_simple/  ← Paste here
          ├── __init__.py
          ├── wireless_simple.py
          └── README.md
```

### 3. Restart ComfyUI
Close ComfyUI completely and restart it.

---

## First Test (Do This First!)

### Step 1: Create This Simple Workflow
```
[Load Image] 
    ↓
[📤 Wireless Send]
    • channel: "test"
    • value: (connected to Load Image output)
    ↓ passthrough output
[Preview Image]  ← IMPORTANT: Connect this!


(In another part of canvas)

[📥 Wireless Get]
    • channel: "test"
    ↓ value output
[Save Image]
```

### Step 2: Run It
- If it works, you'll see the same image in Preview and Save
- Check console for: `[WirelessSend] Stored to 'test': Tensor`

### Step 3: What If It Doesn't Work?

#### You see: "Channel 'test' not found"
**Problem:** Send node didn't execute

**Fix:** Make sure the Send node's passthrough is connected to Preview!

```
❌ WRONG:
[Load Image] → [Send: "test"]
                  (no passthrough connected)

✅ RIGHT:
[Load Image] → [Send: "test"] → [Preview]
                                  ↑
                           (passthrough connected)
```

---

## Most Common Use Cases

### Use Case 1: Clean Up Messy Workflows
**Before:**
```
[Checkpoint] ────MODEL─────────────────────────→ [KSampler]
            ├────CLIP─────────────→ [Encode Pos]
            ├────CLIP─────→ [Encode Neg]
            └────VAE──→ [Decode]
```

**After:**
```
[Checkpoint]
   ├→ [Send: "model"] → [Preview]
   ├→ [Send: "clip"] → [Preview]
   └→ [Send: "vae"] → [Preview]

(Clean workspace, no long wires)

[Get: "model"] → [KSampler]
[Get: "clip"] → [Encode Pos]
[Get: "clip"] → [Encode Neg]
[Get: "vae"] → [Decode]
```

### Use Case 2: One Source, Many Destinations
```
[Load Image] → [Send: "input"] → [Preview]

[Get: "input"] → [Process A] → [Save A]
[Get: "input"] → [Process B] → [Save B]
[Get: "input"] → [Process C] → [Save C]
```

### Use Case 3: Share Settings Across Workflow
```
[Settings Node] → [Send: "config"] → [Preview]

[Get: "config"] → [Use in Section 1]
[Get: "config"] → [Use in Section 2]
[Get: "config"] → [Use in Section 3]
```

---

## The Golden Rule

### 🚨 ALWAYS CONNECT THE PASSTHROUGH OUTPUT! 🚨

The Send node's `passthrough` output MUST be connected to another node.

Common choices:
- ✅ Preview Image
- ✅ Save Image  
- ✅ Another Send node
- ✅ Any other node

If you don't connect it, the Send node won't execute, and you'll get "channel not found" errors.

---

## Troubleshooting Checklist

### ❌ Problem: "Channel not found"
- [ ] Is the Send node's passthrough connected?
- [ ] Are the channel names identical? (case-sensitive)
- [ ] Did the Send node execute? (check console)

### ❌ Problem: Getting None/empty data
- [ ] Do channel names match exactly?
- [ ] Did you spell them the same? (no typos)
- [ ] Check console for channel names

### ❌ Problem: Nodes don't appear in menu
- [ ] Files in correct location?
- [ ] Did you restart ComfyUI completely?
- [ ] Check console for Python errors

---

## Console Messages (What They Mean)

### ✅ Working:
```
[WirelessSend] Stored to 'my_channel': Tensor
[WirelessGet] Retrieved from 'my_channel': Tensor
```

### ❌ Not Working:
```
[WirelessGet] WARNING: Channel 'my_channel' not found or empty!
[WirelessGet] Available: []
```
This means the Send node never executed. Connect its passthrough!

---

## Tips

1. **Use descriptive channel names**: "input_image" not "temp1"
2. **Connect passthrough to Preview**: Easy way to verify Send executes
3. **One Send, Many Gets**: Distribute data to multiple locations
4. **Check console**: Debug messages tell you what's happening
5. **Test incrementally**: Add wireless links one at a time

---

## Need More Help?

See the full README.md for:
- Detailed examples
- Advanced usage
- Complete troubleshooting guide
- Technical details
