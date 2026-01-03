# CORTEX Tool Binding Format

Complete reference for creating tool manifests in AFOT CORTEX.

---

## 📋 Manifest Structure

Every CORTEX manifest follows this structure:

```yaml
name: "agent_name"
version: "1.0.0"
base_model: "llama3.2:3b"

bindings:
  - name: "tool_name"
    language: "python"
    entrypoint: "script.py"
    description: "What this tool does"
    input_schema:
      type: "object"
      properties:
        param_name:
          type: "string"
          description: "Parameter description"
      required: ["param_name"]
    output_schema:
      type: "object"
      properties:
        result:
          type: "string"

capabilities:
  file_system_write:
    enabled: true
    allowed_paths:
      - "C:/temp/*"
    blocked_paths:
      - "C:/Windows"
    require_confirmation: true
  
  network_access:
    enabled: true
    unrestricted: false
    allowed_domains:
      - "*.example.com"
    require_confirmation: true
    max_timeout: 300

description: "Agent description"
```

---

## 🔑 Required Fields

### Manifest Level
- **`name`** - Unique identifier for your agent (alphanumeric + underscore)
- **`version`** - Semantic version (e.g., "1.0.0")
- **`base_model`** - LLM model to use (e.g., "llama3.2:3b")
- **`bindings`** - Array of tool definitions

### Tool Binding Level
- **`name`** - Unique tool name
- **`language`** - `python`, `javascript`, or `shell`
- **`entrypoint`** - Script file path (relative to manifest)
- **`description`** - Clear explanation of tool purpose
- **`input_schema`** - JSON Schema for input validation
- **`output_schema`** - JSON Schema for output validation

---

## 🛠️ Tool Languages

### Python Tools
```yaml
- name: "my_python_tool"
  language: "python"
  entrypoint: "tools/script.py"
  description: "Does something cool"
  input_schema:
    type: "object"
    properties:
      target:
        type: "string"
        description: "Target to process"
    required: ["target"]
```

**Python script format**:
```python
#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv) < 2:
        print("Error: Missing argument")
        sys.exit(1)
    
    target = sys.argv[1]
    # Your logic here
    print(f"Processed: {target}")

if __name__ == "__main__":
    main()
```

### JavaScript Tools
```yaml
- name: "my_js_tool"
  language: "javascript"
  entrypoint: "tools/script.js"
  description: "JavaScript tool"
  input_schema:
    type: "object"
    properties:
      input:
        type: "string"
```

**JavaScript script format**:
```javascript
#!/usr/bin/env node
const arg = process.argv[2];
console.log(`Result: ${arg}`);
```

### Shell Tools
```yaml
- name: "my_shell_tool"
  language: "shell"
  entrypoint: "tools/script.sh"
  description: "Shell script tool"
```

**Shell script format**:
```bash
#!/bin/bash
echo "Processing: $1"
# Your logic here
```

---

## 🔐 Capabilities

### File System Write
```yaml
file_system_write:
  enabled: true
  allowed_paths:
    - "C:/temp/*"           # Windows
    - "/tmp/*"              # Linux/Mac
    - "~/data/*"            # User home
  blocked_paths:
    - "C:/Windows"
    - "C:/Program Files"
    - "/etc"
    - "/usr/bin"
  require_confirmation: true
```

**Rules**:
- Paths use glob patterns (`*` for any)
- Blocked paths take precedence
- `require_confirmation: true` = User approves each write
- `require_confirmation: false` = Auto-approve (dangerous!)

### Network Access
```yaml
network_access:
  enabled: true
  unrestricted: false
  allowed_domains:
    - "api.example.com"
    - "*.github.com"
    - "scanme.nmap.org"
  require_confirmation: false
  max_timeout: 600          # 10 minutes
```

**Rules**:
- `unrestricted: true` = Allow ANY domain (for tools like nmap)
- `unrestricted: false` = Only `allowed_domains`
- Use `*` for subdomains: `*.example.com`
- `max_timeout` in seconds

---

## 📊 Input/Output Schemas

### JSON Schema Format
```yaml
input_schema:
  type: "object"
  properties:
    required_param:
      type: "string"
      description: "This is required"
    optional_param:
      type: "number"
      description: "This is optional"
    flag:
      type: "boolean"
      description: "True or false"
  required: ["required_param"]

output_schema:
  type: "object"
  properties:
    success:
      type: "boolean"
    message:
      type: "string"
    data:
      type: "object"
```

**Supported Types**:
- `string` - Text
- `number` - Integer or float
- `boolean` - true/false
- `object` - Nested structure
- `array` - List of items

---

## ✅ Best Practices

### 1. Clear Descriptions
```yaml
# ❌ Bad
description: "Tool"

# ✅ Good
description: "Scans network targets with nmap for open ports and services"
```

### 2. Specific Paths
```yaml
# ❌ Too permissive
allowed_paths:
  - "C:/*"

# ✅ Specific
allowed_paths:
  - "C:/temp/scans/*"
  - "C:/data/results/*"
```

### 3. Required vs Optional
```yaml
# ✅ Clear requirements
input_schema:
  type: "object"
  properties:
    target:
      type: "string"
      description: "Target to scan (required)"
    ports:
      type: "string"
      description: "Port range (optional, defaults to common ports)"
  required: ["target"]  # Only target is required
```

### 4. Descriptive Names
```yaml
# ❌ Generic
name: "tool1"

# ✅ Descriptive
name: "nmap_scanner"
```

---

## 📝 Complete Examples

### Example 1: Folder Creator
```yaml
name: "file_tools"
version: "1.0.0"
base_model: "llama3.2:3b"

bindings:
  - name: "create_folder"
    language: "python"
    entrypoint: "folder_creator.py"
    description: "Creates folders on the file system"
    input_schema:
      type: "object"
      properties:
        folder_path:
          type: "string"
          description: "Path where folder should be created"
      required: ["folder_path"]
    output_schema:
      type: "object"
      properties:
        success:
          type: "boolean"
        path:
          type: "string"
        message:
          type: "string"

capabilities:
  file_system_write:
    enabled: true
    allowed_paths:
      - "C:/temp/*"
      - "C:/data/*"
    blocked_paths:
      - "C:/Windows"
    require_confirmation: true

description: "File system utilities"
```

### Example 2: Network Scanner
```yaml
name: "network_tools"
version: "1.0.0"
base_model: "llama3.2:3b"

bindings:
  - name: "nmap"
    language: "python"
    entrypoint: "nmap.py"
    description: "Network scanning with nmap - pass any nmap arguments"
    input_schema:
      type: "object"
      properties:
        args:
          type: "string"
          description: "Nmap arguments (e.g., '-sV -p 80,443 192.168.1.1')"
      required: ["args"]
    output_schema:
      type: "object"
      properties:
        output:
          type: "string"

capabilities:
  network_access:
    enabled: true
    unrestricted: true          # Allow any target
    require_confirmation: false  # No confirmation needed
    max_timeout: 600

description: "Network security scanning tools"
```

---

## 🚨 Security Guidelines

### DO ✅
- List only specific paths you need
- Use `require_confirmation: true` for dangerous operations
- Block system directories
- Set reasonable timeouts
- Validate all inputs in your scripts

### DON'T ❌
- Use `allowed_paths: ["C:/*"]` or `["/"]`
- Set `require_confirmation: false` without good reason
- Allow write access to system directories
- Use `unrestricted: true` unless absolutely necessary
- Trust user input without validation

---

## 🔍 Validation

### Test Your Manifest
```bash
cortex test -m your_manifest.yaml
```

### Common Errors

**Invalid YAML**:
```yaml
# ❌ Missing quotes
name: my agent

# ✅ Quoted strings
name: "my_agent"
```

**Missing Required Fields**:
```yaml
# ❌ Missing description
bindings:
  - name: "tool"
    language: "python"
    entrypoint: "script.py"

# ✅ Complete
bindings:
  - name: "tool"
    language: "python"
    entrypoint: "script.py"
    description: "Tool description"
```

---

## 📚 Quick Reference

| Field | Type | Required | Example |
|-------|------|----------|---------|
| `name` | string | Yes | `"my_agent"` |
| `version` | string | Yes | `"1.0.0"` |
| `base_model` | string | Yes | `"llama3.2:3b"` |
| `bindings` | array | Yes | `[{...}]` |
| `capabilities` | object | No | `{file_system_write: {...}}` |
| `description` | string | No | `"My agent"` |

### Binding Fields

| Field | Type | Required | Example |
|-------|------|----------|---------|
| `name` | string | Yes | `"my_tool"` |
| `language` | string | Yes | `"python"` |
| `entrypoint` | string | Yes | `"script.py"` |
| `description` | string | Yes | `"Does X"` |
| `input_schema` | object | Yes | `{type: "object"}` |
| `output_schema` | object | Yes | `{type: "object"}` |

---

## 🎯 Next Steps

1. **Create your tools** - Write Python/JS/Shell scripts
2. **Write manifest** - Follow format above
3. **Test it** - `cortex test -m manifest.yaml`
4. **Bind it** - `cortex bind manifest.yaml`
5. **Use it** - `cortex chat`

---

**Need help?** See [Demo/README.md](Demo/README.md) for complete examples!
