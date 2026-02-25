# ComfyUI Wireless Link - Complete Package

## 📦 What's Included

This package contains everything you need to install wireless link nodes in ComfyUI.

### Files:
```
comfyui_wireless_link_simple/
├── __init__.py           (Required - Python package initialization)
├── wireless_simple.py    (Required - The node code)
├── README.md            (Documentation - Full guide)
├── QUICKSTART.md        (Documentation - Quick start)
└── INSTALL.md           (Documentation - Installation guide)
```

### Nodes Included:
- 📤 **Wireless Send** - Send data to a named channel
- 📥 **Wireless Get** - Receive data from a named channel

---

## 🚀 Quick Install (3 Steps)

### Step 1: Extract
Extract the `comfyui_wireless_link_simple` folder

### Step 2: Copy
Copy it to:
```
ComfyUI/custom_nodes/comfyui_wireless_link_simple/
```

### Step 3: Restart
Completely restart ComfyUI (close and reopen)

---

## ✅ Verify Installation

1. Open ComfyUI
2. Right-click on canvas → Add Node
3. Look for "wireless" category
4. You should see:
   - 📤 Wireless Send
   - 📥 Wireless Get

---

## 📖 Documentation

### Quick Start First!
Start with **QUICKSTART.md** for a simple test workflow

### Need Help Installing?
Read **INSTALL.md** for detailed installation steps and troubleshooting

### Full Documentation
Read **README.md** for complete usage guide, examples, and tips

---

## 🧪 First Test

Try this simple workflow to verify everything works:

```
[Load Image] 
    ↓
[📤 Wireless Send]
    • channel: "test"
    ↓ passthrough (CONNECT THIS!)
[Preview Image]

[📥 Wireless Get]
    • channel: "test"  
    ↓
[Save Image]
```

**Important:** The Send node's passthrough output MUST be connected!

---

## ⚠️ Most Common Issue

### Error: "Channel not found"

**Problem:** Send node isn't executing

**Solution:** Connect the Send node's passthrough output:

```
❌ WRONG:
[Load] → [Send] (no passthrough connected)

✅ CORRECT:
[Load] → [Send] → [Preview]
              ↑
         (passthrough connected)
```

---

## 💡 Usage Example

### Clean Up Messy Workflows

**Before:**
```
[Checkpoint] ──MODEL──→ [Far Away Node]
            └─CLIP───→ [Another Far Node]
```
(Long wires everywhere)

**After:**
```
[Checkpoint]
   ├→ [Send: "model"] → [Preview]
   └→ [Send: "clip"] → [Preview]

(Clean workspace)

[Get: "model"] → [Use Here]
[Get: "clip"] → [Use There]
```

---

## 📝 Key Points

1. ✅ Works with ANY ComfyUI data type (IMAGE, MODEL, LATENT, etc.)
2. ✅ One Send can feed multiple Get nodes
3. ✅ Channel names are case-sensitive
4. ⚠️ Send node's passthrough MUST be connected
5. ⚠️ Send must execute BEFORE Get

---

## 🔍 Check Console Output

When working correctly, you'll see:
```
[WirelessSend] Stored to 'channel': Tensor
[WirelessGet] Retrieved from 'channel': Tensor
```

When not working, you'll see:
```
[WirelessGet] WARNING: Channel 'channel' not found!
[WirelessGet] Available: []
```

---

## 📚 Where to Get Help

1. **QUICKSTART.md** - Start here for your first test
2. **INSTALL.md** - Detailed installation and troubleshooting  
3. **README.md** - Complete usage guide and examples
4. **Console output** - Always check for error messages

---

## 🎯 Installation Checklist

- [ ] Downloaded/extracted the package
- [ ] Copied folder to `ComfyUI/custom_nodes/`
- [ ] Folder is named `comfyui_wireless_link_simple`
- [ ] Contains `__init__.py` and `wireless_simple.py`
- [ ] Restarted ComfyUI completely (not just browser refresh)
- [ ] Nodes appear in "wireless" category
- [ ] Tested with simple workflow
- [ ] Console shows no errors

If all checked, you're ready to go! 🎉

---

## 🆘 Still Having Issues?

1. Read INSTALL.md troubleshooting section
2. Check console for error messages
3. Verify file locations match exactly
4. Ensure complete ComfyUI restart
5. Test with simple Load→Send→Get→Save workflow

---

**Version:** 1.0 Simple
**License:** Free for personal and commercial use
**Compatibility:** All ComfyUI versions

Enjoy cleaner workflows! 🚀
