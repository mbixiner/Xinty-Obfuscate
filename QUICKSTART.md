# Quick Start Guide

Get started with PE Obfuscator in 5 minutes!

## Installation

```bash
# Clone or download the repository
cd obfu

# No dependencies required! Uses Python standard library only
python --version  # Requires Python 3.7+
```

## Basic Usage

### 1. Simple Obfuscation

```bash
python obfuscator.py your_program.exe
```

This creates `your_program_obfuscated.exe` with all safe obfuscation techniques applied.

### 2. Specify Output File

```bash
python obfuscator.py input.exe -o protected.exe
```

### 3. Choose Specific Techniques

```bash
python obfuscator.py input.exe -t sections timestamp junk
```

### 4. See All Options

```bash
python obfuscator.py --help
```

## Try It Out

### Step 1: Create a Test File

```bash
python test_obfuscator.py
```

This creates sample PE files in the `test_files/` directory.

### Step 2: Obfuscate the Test File

```bash
python obfuscator.py test_files/test_sample.exe
```

### Step 3: Check the Results

The obfuscated file will be created with a detailed report showing:
- Which techniques were applied
- Section name changes
- File size changes
- Any warnings or issues

## Example Output

```
============================================================
                      PE OBFUSCATOR                        
============================================================

[+] Loaded 73728 bytes from test.exe
[+] PE file parsed: 32-bit, 5 sections

[*] Starting obfuscation with techniques: all

[*] Obfuscating section names...
  [+] .text      -> .xmkpqr
  [+] .data      -> .nvwxy
  [+] .rdata     -> .ghijk

[*] Modifying timestamp...
  [+] Set timestamp to 0xA3F2B891

[*] Adding junk sections...
  [+] Added 2048 bytes of junk overlay data

============================================================
[+] Obfuscated file saved to: test_obfuscated.exe
[+] File size: 75776 bytes
============================================================

[✓] Obfuscation completed successfully!
```

## Obfuscation Techniques

### Safe Techniques (Recommended)

| Technique | Command | Description |
|-----------|---------|-------------|
| All Safe | `-t all` | Apply all safe techniques (default) |
| Sections | `-t sections` | Randomize PE section names |
| Timestamp | `-t timestamp` | Modify compilation timestamp |
| DOS Stub | `-t dos-stub` | Change DOS stub message |
| Junk Data | `-t junk` | Add random overlay data |
| Checksum | `-t checksum` | Modify PE checksum |

### Advanced Techniques (Test First)

| Technique | Command | Description | Risk |
|-----------|---------|-------------|------|
| Anti-Debug | `-t anti-debug` | Add anti-debug markers | Low |
| Code Caves | `-t caves` | Fill empty code regions | Medium |

## Common Use Cases

### Protect a Release Build

```bash
# Build your application first
# Then obfuscate the release version
python obfuscator.py MyApp.exe -o MyApp_Protected.exe -t all
```

### Light Obfuscation (No Size Increase)

```bash
python obfuscator.py app.exe -t sections timestamp checksum
```

### Maximum Obfuscation

```bash
python obfuscator.py app.exe -t all
```

### Batch Process Multiple Files

```bash
# Windows
for %f in (*.exe) do python obfuscator.py "%f"

# PowerShell
Get-ChildItem *.exe | ForEach-Object { python obfuscator.py $_.Name }

# Linux/Mac
for f in *.exe; do python obfuscator.py "$f"; done
```

## What to Expect

### ✅ The Obfuscated File Will:
- Have randomized section names
- Have different timestamp and checksum
- Be slightly larger (due to junk data)
- Run the same as the original
- Be harder to analyze with static tools

### ⚠️ The Obfuscated File May:
- Trigger antivirus false positives
- Have invalidated digital signatures
- Need testing before distribution
- Require code signing for distribution

### ❌ The Obfuscator Will NOT:
- Protect against determined reverse engineers
- Make malware undetectable
- Break the executable (when using safe techniques)
- Add runtime protection

## Testing Your Obfuscated File

Always test before distribution!

```bash
# 1. Run the obfuscated executable
obfuscated_app.exe

# 2. Test all features
# - Check basic functionality
# - Test with different inputs
# - Verify performance
# - Check for crashes

# 3. Scan with antivirus (optional)
# Some AVs may flag obfuscated files

# 4. Compare behavior with original
# Should work identically
```

## Troubleshooting

### "Invalid DOS signature" Error
- Make sure the input is a valid Windows PE (.exe) file
- The file must have MZ signature (DOS header)

### "Error parsing headers" Error
- The PE file may be corrupted
- Try with a different executable

### Obfuscated File Doesn't Run
- Use only safe techniques first: `-t sections timestamp junk`
- Test each technique individually
- Check if original file is already packed/protected

### Antivirus Detects Obfuscated File
- This is expected behavior with obfuscation
- Code sign your executable
- Submit to AV vendors for whitelisting
- Use fewer techniques if needed

## Advanced Usage

See `examples.py` for code examples:
```bash
python examples.py
```

See `advanced_obfuscator.py` for demonstration of advanced techniques:
```bash
python advanced_obfuscator.py
```

## Next Steps

1. ✅ Read the full [README.md](README.md)
2. ✅ Review [SECURITY.md](SECURITY.md) for responsible use
3. ✅ Check [examples.py](examples.py) for code examples
4. ✅ Experiment with different technique combinations
5. ✅ Always test obfuscated executables before deployment

## Tips for Best Results

1. **Start Simple**: Begin with just section name obfuscation
2. **Test Often**: Test after each technique addition
3. **Keep Originals**: Always keep unobfuscated backups
4. **Document Changes**: Keep track of what techniques you used
5. **Code Sign**: Sign your obfuscated executables for distribution
6. **Be Transparent**: Let users know if executables are obfuscated

## Support

- Check [README.md](README.md) for detailed documentation
- Run test suite: `python test_obfuscator.py`
- View examples: `python examples.py`
- Open GitHub issues for bugs or questions

## Safety Reminder

⚠️ **Always test obfuscated executables before distribution!**

✅ **Only obfuscate files you have rights to modify!**

📚 **Use for legitimate software protection only!**

---

Happy obfuscating! 🔒

