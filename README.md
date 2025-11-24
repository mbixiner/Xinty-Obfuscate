# PE Executable Obfuscator

A comprehensive obfuscator for Windows PE (.exe) files with multiple protection layers and anti-reverse engineering techniques.
<p align="center">
    <a href="https://python.org">
    <img src="https://img.shields.io/badge/Python-3.7-green.svg">
  </a>
  <a href="https://github.com/mbixiner/Xinty-Obfuscate/blob/master/LICENSE">
    <img src="https://img.shields.io/badge/License-BSD%203-lightgrey.svg">
  </a>
  <a href="https://github.com/mbixiner/Xinty-Obfuscate/releases">
    <img src="https://img.shields.io/badge/Release-1.0-blue.svg">
  </a>
    <a href="https://github.com/mbixiner/Xinty-Obfuscate">
    <img src="https://img.shields.io/badge/Open%20Source-%E2%9D%A4-brightgreen.svg">
  </a>
</p>
## ⚠️ Legal Disclaimer

This tool is provided for educational and legitimate software protection purposes only. Users are responsible for:
- Ensuring compliance with all applicable laws and regulations
- Having proper authorization for any files they obfuscate
- Not using this tool for malicious purposes

Obfuscated executables may be flagged by antivirus software as potentially suspicious.

## 🚀 Features

### Basic Obfuscation (`obfuscator.py`)
- **Section Name Randomization**: Randomizes PE section names to confuse static analysis
- **Timestamp Modification**: Changes compilation timestamp
- **DOS Stub Randomization**: Modifies the DOS stub message
- **Junk Data Injection**: Adds random data to file overlay
- **Checksum Modification**: Invalidates/modifies PE checksum
- **Anti-Debug Markers**: Adds markers to trigger anti-debugging tools
- **Code Cave Filling**: Fills null byte regions with junk instructions

## 📋 Requirements

```bash
pip install -r requirements.txt
```

Or simply:
- Python 3.7+
- No external dependencies (uses only standard library)

## 💻 Usage

### Basic Obfuscator

```bash
# Obfuscate with all techniques
python obfuscator.py
```

### Available Techniques

| Technique | Description | Safety |
|-----------|-------------|--------|
| `all` | Apply all safe techniques | ✅ Safe |
| `sections` | Randomize section names | ✅ Safe |
| `timestamp` | Modify PE timestamp | ✅ Safe |
| `dos-stub` | Randomize DOS stub | ✅ Safe |
| `junk` | Add junk overlay data | ✅ Safe |
| `checksum` | Modify checksum | ✅ Safe |
| `anti-debug` | Add anti-debug markers | ✅ Safe |
| `caves` | Fill code caves | ⚠️ Test First |

The advanced obfuscator is a demonstration of sophisticated techniques that would require full implementation with disassembly/reassembly capabilities.

## 📊 Example Output

```
============================================================
                      PE OBFUSCATOR                        
============================================================

[+] Loaded 73728 bytes from input.exe
[+] PE file parsed: 32-bit, 5 sections

[*] Starting obfuscation with techniques: all

[*] Obfuscating section names...
  [+] .text      -> .xmkpqr
  [+] .data      -> .nvwxy
  [+] .rdata     -> .ghijk
  [+] .rsrc      -> .pqrst
  [+] .reloc     -> .abcde

[*] Modifying timestamp...
  [+] Set timestamp to 0xA3F2B891

[*] Randomizing DOS stub...
  [+] DOS stub message randomized

[*] Adding junk sections...
  [+] Added 2048 bytes of junk overlay data

[*] Modifying checksum...
  [+] Checksum set to 0 (will be recalculated by loader)

[*] Adding anti-debug markers...
  [+] Added anti-debug string markers

[*] Filling code caves with junk...
  [+] Filled code caves in .xmkpqr

============================================================
[+] Obfuscated file saved to: input_obfuscated.exe
[+] File size: 75776 bytes
============================================================

[✓] Obfuscation completed successfully!

[!] Warning: The obfuscated file may be detected by antivirus software
[!] Warning: Always test the obfuscated executable before distribution
[!] Warning: Some techniques may break executable functionality
```

## 🔬 How It Works

### PE File Structure
The obfuscator parses the Windows Portable Executable (PE) format:
1. DOS Header (MZ signature)
2. DOS Stub
3. PE Header (PE signature)
4. COFF File Header
5. Optional Header
6. Section Headers
7. Sections (.text, .data, .rsrc, etc.)

### Obfuscation Process
1. **Parse**: Load and parse PE headers
2. **Transform**: Apply selected obfuscation techniques
3. **Rebuild**: Write modified PE file

### Anti-Reverse Engineering Techniques

#### Static Analysis Resistance
- Randomized section names confuse tools expecting standard names
- Modified timestamps hide compilation patterns
- Junk data increases analysis time
- Modified checksums require recalculation

#### Dynamic Analysis Resistance
- Anti-debug markers may trigger debugger detection
- Dead code confuses control flow analysis
- Opaque predicates hide true execution paths

#### Code Analysis Resistance
- Instruction substitution changes byte patterns
- Control flow flattening obscures program logic
- String encryption hides sensitive data
- API obfuscation hides Windows API usage

## 🛡️ Limitations

### Current Limitations
- Does not perform full code disassembly/reassembly
- Import table obfuscation is limited (stability reasons)
- Resource encryption would break functionality without decryption stub
- Some techniques are demonstrated in `advanced_obfuscator.py` but not fully implemented

### What This Does NOT Do
- ❌ Protect against determined reverse engineers
- ❌ Make malware undetectable
- ❌ Provide runtime packing/unpacking
- ❌ Add virtualization or emulation layers
- ❌ Guarantee 100% AV evasion

## 🧪 Testing

**ALWAYS test obfuscated executables before distribution!**

```bash
# Test basic functionality
obfuscated.exe

# Test with different techniques
python obfuscator.py
```

### Verification Steps
1. ✅ Run obfuscated executable
2. ✅ Verify expected behavior
3. ✅ Test on target systems
4. ✅ Check file integrity
5. ✅ Monitor for crashes

## 🔧 Advanced Usage

### Custom Obfuscation Pipeline

```python
from obfuscator import PEObfuscator

# Create custom obfuscation
obf = PEObfuscator('input.exe', 'output.exe')
obf.load_file()
obf.parse_headers()

# Apply specific techniques
obf.obfuscate_section_names()
obf.modify_timestamps()
obf.add_junk_sections()

# Save result
obf.save_file()
```

### Integration with Build Process

```bash
# In your build script
python obfuscator.py release/app.exe -o release/app_protected.exe -t all
```

## 🎯 Use Cases

### Legitimate Uses
- ✅ Protecting intellectual property
- ✅ Preventing unauthorized modification
- ✅ Adding anti-tampering measures
- ✅ Software licensing protection
- ✅ Security research and education

### DO NOT Use For
- ❌ Hiding malware
- ❌ Evading legitimate security tools
- ❌ Unauthorized software modification
- ❌ Any illegal activities

## 📚 Technical References

- [PE Format Specification](https://docs.microsoft.com/en-us/windows/win32/debug/pe-format)
- [x86 Instruction Set Reference](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)
- [Code Obfuscation Techniques](https://en.wikipedia.org/wiki/Obfuscation_(software))

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Full x86/x64 disassembler integration
- Import table obfuscation
- Resource encryption with decryption stub
- Control flow graph analysis
- More anti-debugging techniques
- GUI interface

## 📝 License

MIT License - See LICENSE file for details

## ⚖️ Responsible Use

This tool is powerful. Use it responsibly:
- Only obfuscate files you have rights to modify
- Understand that obfuscation ≠ security
- Test thoroughly before deployment
- Be transparent with users about obfuscation
- Comply with all applicable laws

## 🔍 Detection & Analysis

Security researchers can analyze obfuscated files using:
- PE analysis tools (PE Explorer, CFF Explorer)
- Disassemblers (IDA Pro, Ghidra)
- Debuggers (x64dbg, OllyDbg)
- Hex editors (HxD, 010 Editor)

This obfuscator makes analysis more time-consuming but not impossible.

---

**Remember**: Obfuscation is not a substitute for proper security practices. It's one layer in a defense-in-depth strategy.



