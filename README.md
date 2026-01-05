# 🧠 AFOT CORTEX

**Sandbox-Embedded LLM with Tool Binding**

[![Rust](https://img.shields.io/badge/rust-1.70%2B-orange.svg)](https://www.rust-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)]()

> **Chat with AI that can execute your tools safely. Turn any CLI tool into an AI-powered agent.**

---

## 🎯 What is CORTEX?

CORTEX combines **Local LLMs** (via Ollama) with **sandboxed tool execution** for autonomous security testing and automation.

**Simple workflow**:
```
You: "Scan scanme.nmap.org with nmap"
  ↓
AI: Generates execution code
  ↓
You: Review and approve
  ↓
Sandbox: Executes safely
  ↓
Results: Displayed instantly
```

### Key Features

- 🤖 **Local LLM Integration** - Works with Ollama (llama3.2, llama3, etc.)
- 🔐 **Manifest-Controlled Security** - Define what tools can access
- 📦 **Sandboxed Execution** - Python, JavaScript, Shell support
- 🛠️ **Any Tool** - Bind nmap, custom scripts, anything CLI-based
- 💬 **Conversational** - Natural language → Tool execution
- 🧠 **Memory** - Remembers conversation context

---

## 🚀 Quick Start

### Prerequisites

**Install these first**:

1. **Ollama** (Required - runs the AI):
```bash
# Install Ollama
curl https://ollama.ai/install.sh | sh

# Download AI model
ollama pull llama3.2:3b
```

2. **Python 3** (Required for tool execution):
```bash
# Check if installed
python3 --version

# If not installed:
# - Ubuntu/Debian: sudo apt install python3
# - macOS: brew install python3
# - Windows: Download from python.org
```

3. **(Optional) WSL Kali** - For nmap on Windows:
```bash
wsl --install
wsl -d kali-linux sudo apt install nmap
```

---

### Installation

Choose your platform:

#### Linux (Debian/Ubuntu)

**Option 1: .deb Package (Recommended)**
```bash
# Download
curl -LO https://github.com/ALL-FOR-ONE-TECH/AFOT-CORTEX/releases/download/V1.0.0/cortex_1.0.0_amd64.deb

# Install
sudo dpkg -i cortex_1.0.0_amd64.deb

# Verify
cortex --help
```

**Option 2: Binary**
```bash
# Download
curl -LO https://github.com/ALL-FOR-ONE-TECH/AFOT-CORTEX/releases/download/V1.0.0/cortex-linux-x64.tar.gz

# Extract
tar xzf cortex-linux-x64.tar.gz

# Install
chmod +x cortex
sudo mv cortex /usr/local/bin/

# Verify
cortex --help
```

#### macOS

**For Intel Macs**:
```bash
# Download
curl -LO https://github.com/ALL-FOR-ONE-TECH/AFOT-CORTEX/releases/download/V1.0.0/cortex-macos-intel.tar.gz

# Extract
tar xzf cortex-macos-intel.tar.gz

# Install
chmod +x cortex
sudo mv cortex /usr/local/bin/

# Verify
cortex --help
```

**For Apple Silicon (M1/M2/M3)**:
```bash
# Download
curl -LO https://github.com/ALL-FOR-ONE-TECH/AFOT-CORTEX/releases/download/V1.0.0/cortex-macos-arm.tar.gz

# Extract
tar xzf cortex-macos-arm.tar.gz

# Install
chmod +x cortex
sudo mv cortex /usr/local/bin/

# Verify
cortex --help
```

#### Windows

**Pre-built binary**:
```bash
# Download from releases page
# https://github.com/ALL-FOR-ONE-TECH/AFOT-CORTEX/releases/tag/V1.0.0

# Extract cortex.exe
# Add to PATH or run from directory
```

---

## 📚 Usage

### 1. Try the Demo

```bash
# Clone the repository
git clone https://github.com/ALL-FOR-ONE-TECH/AFOT-CORTEX
cd AFOT-CORTEX/Demo

# Bind the demo tools
cortex bind capabilities.yaml

# Check what's loaded
cortex list

# Start chatting!
cortex chat
```

**Example conversation**:
```
You: hi
AI: Hello! I can help with folder creation and network scanning.

You: Create folder /tmp/test
AI: (generates Python code)
Execute? yes
✅ Folder created!

You: Scan scanme.nmap.org
AI: (generates nmap command)
Execute? yes
✅ Scan results displayed!
```

### 2. All Commands

```bash
# Bind tools from a manifest
cortex bind <manifest.yaml>

# Remove current binding
cortex unbind

# Show bound tools and status
cortex list

# Interactive chat with AI
cortex chat

# Validate a manifest file
cortex test <manifest.yaml>

# Create new agent template
cortex create -n <name> -m <model>

# Show help
cortex --help
```

---

## 🛠️ Creating Your Own Tools

### Step 1: Write Your Tool

**Python Example** (`my_tool.py`):
```python
#!/usr/bin/env python3
import sys

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "default"
    print(f"Processing {target}...")
    # Your logic here
    print(f"✅ Done!")

if __name__ == "__main__":
    main()
```

**Make it executable**:
```bash
chmod +x my_tool.py
```

### Step 2: Create Manifest

**`my_manifest.yaml`**:
```yaml
name: "my_agent"
version: "1.0.0"
base_model: "llama3.2:3b"

bindings:
  - name: "my_tool"
    language: "python"
    entrypoint: "my_tool.py"
    description: "My custom tool that processes targets"
    input_schema:
      type: "object"
      properties:
        target:
          type: "string"
          description: "Target to process"
      required: ["target"]
    output_schema:
      type: "object"
      properties:
        result:
          type: "string"

capabilities:
  file_system_write:
    enabled: true
    allowed_paths:
      - "/tmp/*"
      - "$HOME/data/*"
    blocked_paths:
      - "/etc"
      - "/usr/bin"
    require_confirmation: true
  
  network_access:
    enabled: false

description: "My custom automation agent"
```

### Step 3: Use It

```bash
# Test the manifest
cortex test my_manifest.yaml

# Bind it
cortex bind my_manifest.yaml

# Use it
cortex chat

You: Process example.com
AI: (calls my_tool.py with example.com)
```

**📖 Complete guide**: See [BINDING_FORMAT.md](BINDING_FORMAT.md)

---

## 🔐 Security

### Manifest-Controlled Access

CORTEX uses manifests to define what tools can and cannot do:

```yaml
capabilities:
  file_system_write:
    allowed_paths: ["/tmp/*"]     # Whitelist
    blocked_paths: ["/etc"]        # Blacklist
    require_confirmation: true     # User approves each write
  
  network_access:
    enabled: true
    allowed_domains: ["*.safe.com"]  # Domain restrictions
    max_timeout: 600                 # 10 min max
```

### Safety Layers

1. **Manifest Validation** - Tools must be explicitly defined
2. **Path Restrictions** - File access controlled by whitelist/blacklist
3. **User Confirmation** - Approve code before execution
4. **Sandbox Isolation** - Code runs in isolated environment
5. **Timeout Protection** - Max execution time enforced

---

## 💡 Example Use Cases

### Network Security Testing
```
You: Scan my server 192.168.1.100
→ AI generates nmap scan
→ You approve
→ Results displayed
```

### Workflow Automation
```
You: Scan target then create a results folder
→ AI generates multi-step workflow
→ Execute nmap
→ Create folder
→ Save results
```

### Custom Tools
```
You: Run my custom security audit script on example.com
→ AI calls your tool
→ Executes with proper arguments
→ Shows output
```

---

## 🎨 Features

### Conversation Memory
CORTEX remembers your last 5 exchanges:
```
You: Scan afot.in
→ Scans afot.in

You: Now check for vulnerabilities
→ Remembers afot.in, adds vuln scan
```

### Smart Code Generation
AI knows when to generate code vs chat:
```
You: What is nmap?          → Explains (no code)
You: Scan localhost         → Generates code ✅
You: Tell me about ports    → Explains (no code)
```

### Multi-Language Support
- **Python** - Most common, works everywhere
- **JavaScript** - Node.js based tools
- **Shell** - Bash scripts, WSL integration

---

## 🐛 Troubleshooting

### Ollama Not Found
```bash
# Check Ollama
ollama list

# If not installed
curl https://ollama.ai/install.sh | sh
ollama pull llama3.2:3b
```

### Nmap Command Not Found
```bash
# Linux
sudo apt install nmap

# macOS
brew install nmap

# Windows (WSL Kali)
wsl -d kali-linux sudo apt install nmap
```

### Permission Denied
```bash
# Make cortex executable
chmod +x cortex

# Add to PATH if needed
export PATH="/usr/local/bin:$PATH"
```

---

## ⚖️ Legal Notice

**IMPORTANT**: Use CORTEX only on systems you own or have explicit written permission to test.

- ❌ Unauthorized network scanning is **illegal**
- ✅ Always obtain **written authorization**
- ✅ Review **audit logs** regularly
- ✅ Follow **responsible disclosure**

**The authors assume NO liability for misuse.**

---

## 🤝 Contributing

Contributions welcome!

```bash
1. Fork the repo
2. Create feature branch: git checkout -b feature/amazing-feature
3. Commit changes: git commit -m 'Add amazing feature'
4. Push: git push origin feature/amazing-feature
5. Open Pull Request
```

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for details

---

## 🙏 Credits

**Created By**:
- 👨‍💻 **Mr.V2K** - Creator and Lead Developer

**Built With**:
- 🦀 **Rust** - Systems programming language
- 🤖 **Ollama** - Local LLM runtime
- 🐍 **Python** - Tool integration  
- 🐧 **WSL** - Linux tool support

**Special Thanks**:
- Ollama team for local LLM runtime
- Rust community for amazing ecosystem

---

## 📞 Contact

- **Creator**: Mr.V2K
- **GitHub**: [@ALL-FOR-ONE-TECH](https://github.com/ALL-FOR-ONE-TECH)
- **Project**: [AFOT-CORTEX](https://github.com/ALL-FOR-ONE-TECH/AFOT-CORTEX)
- **Issues**: [Report a bug](https://github.com/ALL-FOR-ONE-TECH/AFOT-CORTEX/issues)

---

## 🎉 Get Started Now!

```bash
# 1. Install Ollama
curl https://ollama.ai/install.sh | sh
ollama pull llama3.2:3b

# 2. Download CORTEX
curl -LO https://github.com/ALL-FOR-ONE-TECH/AFOT-CORTEX/releases/download/V1.0.0/cortex-linux-x64.tar.gz
tar xzf cortex-linux-x64.tar.gz
sudo mv cortex /usr/local/bin/

# 3. Try the demo
git clone https://github.com/ALL-FOR-ONE-TECH/AFOT-CORTEX
cd AFOT-CORTEX/Demo
cortex bind capabilities.yaml
cortex chat

You: Let's start! 🚀
```

---

**CORTEX - Your AI-Powered Security Toolkit** 🛡️

*Last Updated: January 2026*
*Version: 1.0.0-production*