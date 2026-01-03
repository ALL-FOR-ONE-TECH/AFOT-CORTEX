# 🚀 CORTEX Demo - Get Started in 5 Minutes

**You just found CORTEX! This demo will show you what it can do.**

---

## 🤔 What is This?

**CORTEX** = An AI assistant that can run security tools for you.

**Think of it like this:**
- You: "Scan this website"
- AI: Writes code to do it
- You: Review and approve
- Computer: Runs the scan
- You: Get results!

**It's ChatGPT, but for hackers (ethical ones!).** 🛡️

---

## ✨ What Can It Do?

This demo comes with 2 tools:

1. **📁 Folder Creator** - Make directories anywhere
2. **🔍 Nmap Scanner** - Scan networks like a pro

But you can add ANY tool you want! (We'll show you how later)

---

## 🎯 First Time Setup

### Before You Start

You need these installed:

**1. Rust** (programming language)
```bash
# Windows/Mac/Linux:
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

**2. Ollama** (runs AI on your computer)
```bash
# Windows/Mac/Linux:
curl https://ollama.ai/install.sh | sh

# Download the AI model:
ollama pull llama3.2:3b
```

**3. (Optional) WSL Kali** (for nmap on Windows)
```bash
# Windows only:
wsl --install
# Then inside WSL:
sudo apt install nmap
```

**Don't worry!** These are one-time setups. Takes about 10 minutes total.

---

## 📦 Installation

### Step 1: Get CORTEX
```bash
# Download it
git clone https://github.com/karthikeyanV2K/AFOT-Coretex
cd AFOT-Coretex

# Or download ZIP from GitHub and extract it
```

### Step 2: Build It
```bash
# This compiles CORTEX (takes 2-5 minutes first time)
cargo build --release --bin cortex
```

**You'll see**: Lots of text scrolling. That's normal! Wait for "Finished"

### Step 3: Make It Easy to Use (Optional)
```bash
# Windows:
.\target\release\cortex.exe --install

# Mac/Linux:
./target/release/cortex --install
```

**What this does**: Lets you type `cortex` from anywhere instead of the full path.

---

## 🎮 Your First Session

### Go to the Demo Folder
```bash
cd Demo
```

**What's here?**
- `capabilities.yaml` - Tells CORTEX which tools to use
- `nmap.py` - Network scanner tool
- `README.md` - You're reading it! 👋

---

### Load the Tools
```bash
cortex bind capabilities.yaml
```

**You'll See**:
```
┌─ BINDING MANIFEST ───────────────────────────────────────
│ capabilities.yaml
└──────────────────────────────────────────────────────────

✓ Loaded: network_tools
✓ Model: llama3.2:3b
✓ Tools: 2

✅ Manifest bound successfully!
```

**What just happened?**
You told CORTEX: "I want to use folder creator and nmap scanner today."

---

### Check What You Loaded
```bash
cortex list
```

**You'll See**:
```
┌─ CORTEX STATUS ──────────────────────────────────────────
│ Bound Manifest
└──────────────────────────────────────────────────────────

Manifest: capabilities.yaml
Agent: network_tools
Model: llama3.2:3b

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BOUND TOOLS (2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  • create_folder (python)
    └─ Creates folders on the file system

  • nmap (python)
    └─ Direct nmap command execution via WSL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Perfect! You have 2 tools ready.

---

### Start Chatting!
```bash
cortex chat
```

**You'll See**:
```
┌─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┬─┐
│ A F O T   C O R T E X │
└─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┴─┘

          Interactive Chat with Sandboxed LLM
────────────────────────────────────────────────────────────────

✓ Bound manifest: capabilities.yaml
✓ Agent: network_tools
✓ Model: llama3.2:3b

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOOLS AVAILABLE:
  • create_folder (python)
  • nmap (python)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You: _
```

**🎉 You're in!** The AI is ready to help.

---

## 💬 Try It Out!

### Example 1: Say Hello
```
You: hi

LLM: Hello! I can help you with folder creation and network scanning.
     What would you like to do today?

You: _
```

**Notice**: It responded normally, didn't generate code. Smart!

---

### Example 2: Ask a Question
```
You: What is nmap?

LLM: Nmap (Network Mapper) is a free and open-source tool for network 
     discovery and security auditing. It's used to:
     - Discover devices on a network
     - Find open ports
     - Detect services and versions
     - Perform security scans
     
     Would you like me to run a scan?

You: _
```

**Still no code!** It knows when to explain vs when to execute.

---

### Example 3: Create a Folder
```
You: Create folder C:/temp/my_first_scan

LLM: I'll create that folder for you.

```python
from folder_creator import create_folder
result = create_folder('C:/temp/my_first_scan')
print(result['message'])
```

Execute? (yes/no): yes
```

**Wait! What's happening?**
1. You asked for something to be done
2. AI wrote Python code to do it
3. AI is asking YOUR permission to run it

**Type `yes` and press Enter:**

```
⚙️  Executing...
✅ Success!

Output:
Folder created successfully: C:/temp/my_first_scan

You: _
```

**Check your C:/temp folder - there's your new folder!** 🎉

---

### Example 4: Run Nmap (The Fun Part!)
```
You: Scan scanme.nmap.org

LLM: I'll scan that for you.

```python
import subprocess
result = subprocess.run(['python', 'nmap.py', '-sV', 'scanme.nmap.org'], 
                       capture_output=True, text=True)
print(result.stdout)
```

Execute? (yes/no): yes
```

**Type `yes` again:**

```
⚙️  Executing...
✅ Success!

Output:
Starting Nmap 7.95 ( https://nmap.org ) at 2026-01-03 01:30 IST
Nmap scan report for scanme.nmap.org (45.33.32.156)
Host is up (0.185s latency).

PORT    STATE SERVICE  VERSION
80/tcp  open  http     Apache httpd 2.4.7
22/tcp  open  ssh      OpenSSH 6.6.1p1
443/tcp open  ssl/http Apache httpd 2.4.7

Nmap done: 1 IP address (1 host up) scanned in 18.45 seconds

You: _
```

**YOU JUST RAN A REAL NMAP SCAN!** 🔥

The AI:
1. Understood your request
2. Wrote the code
3. Executed nmap
4. Showed you results

---

## 🧠 It Remembers!

Try this conversation:

```
You: Scan example.com

LLM: (runs basic scan)
✅ Scan complete!

You: Now scan ports 80 and 443 only

LLM: (remembers you're scanning example.com!)
✅ Running targeted port scan...
```

**It remembered the target from your first message!**

---

## 🎓 More Things to Try

### Different Nmap Scans
```
You: Scan localhost
You: Scan 192.168.1.1 for open ports
You: Scan google.com ports 80,443,8080
You: Find all devices on 192.168.1.0/24
```

### Multiple Actions
```
You: Scan scanme.nmap.org and save results to C:/temp/scan.txt
```

### Just Chat
```
You: What's the difference between TCP and UDP scan?
You: How do I scan for vulnerabilities?
You: Explain what -sV flag does in nmap
```

---

## 🛑 When You're Done

```
You: quit
```

**Simple!** You can always come back later.

---

## 🔄 Coming Back Later

Next time you want to use CORTEX:

```bash
# Go to Demo folder
cd path/to/AFOT-Coretex/Demo

# Check what's bound (optional)
cortex list

# If nothing bound, load tools again
cortex bind capabilities.yaml

# Start chatting
cortex chat
```

That's it!

---

## 🔐 Is This Safe?

**YES!** Here's why:

### You Control Everything
- ✅ **You see code before it runs** - No surprises
- ✅ **You approve each action** - Type yes/no
- ✅ **Runs on your computer** - No data sent to cloud
- ✅ **Sandboxed** - Can't access everything

### Limited Access
**Can create files in:**
- `C:/temp/*` ✅
- `C:/data/*` ✅

**Cannot touch:**
- System files ❌
- Your documents ❌  
- Anything you didn't allow ❌

### You're Always in Control
Exit anytime with `quit`!

---

## ❓ Common Questions

### "Do I need internet?"
- **For AI**: No! Runs locally via Ollama
- **For nmap scans**: Yes, if scanning internet targets

### "What AI does it use?"
- Llama 3.2 (3 billion parameters)
- Runs on YOUR computer
- Completely private

### "Can I add more tools?"
- **YES!** See the main README.md for how

### "Is this legal?"
- **Scanning YOUR OWN devices**: ✅ Yes
- **Scanning with PERMISSION**: ✅ Yes  
- **Scanning random websites**: ❌ NO! That's illegal!

---

## 🐛 Something Not Working?

### "cortex: command not found"
```bash
# Use full path instead:
../target/release/cortex bind capabilities.yaml
```

### "Ollama error"
```bash
# Start Ollama in another terminal:
ollama serve

# Check if model exists:
ollama list

# Download if needed:
ollama pull llama3.2:3b
```

### "Nmap not found"
```bash
# Windows - Install in WSL:
wsl -d kali-linux
sudo apt update && sudo apt install nmap

# Mac:
brew install nmap

# Linux:
sudo apt install nmap
```

### "Permission denied on folder creation"
```bash
# Make sure C:/temp exists:
mkdir C:/temp

# Or use different path that you own
```

---

## 🎯 What's Next?

### Learn More
1. Read the main `README.md` in parent folder
2. Check out `capabilities.yaml` to see how tools are defined
3. Read `nmap.py` to see how tools work

### Add Your Own Tools
See main README's "Creating Your Own Tools" section

### Try Other Models
```bash
# Larger, smarter AI (needs more RAM):
ollama pull llama3:70b

# Then edit capabilities.yaml:
base_model: "llama3:70b"
```

---

## 🎊 Congratulations!

**You've successfully:**
- ✅ Built CORTEX
- ✅ Bound security tools
- ✅ Chatted with AI
- ✅ Ran real network scans
- ✅ Created folders

**You now have your own AI security assistant!** 🚀

---

## 📞 Need Help?

- Main docs: `../README.md`
- Quick help: `cortex --help`
- Check tools: `cortex list`
- GitHub Issues: [Report a bug](https://github.com/karthikeyanV2K/AFOT-Coretex/issues)

---

## ⚠️ Remember

**Use CORTEX Responsibly:**
- ✅ Scan only systems you own
- ✅ Get permission in writing
- ✅ Follow laws in your country
- ❌ Never scan without authorization

---

**Welcome to the future of security testing!** 🎉

*Happy (ethical) hacking!* 🛡️
