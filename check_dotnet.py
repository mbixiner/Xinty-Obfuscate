"""
.NET Executable Detector
Check if a PE file is a .NET assembly before obfuscating
"""

import sys
import struct


def check_if_dotnet(file_path):
    """Check if a PE file is a .NET assembly"""
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        # Check DOS signature
        if data[0:2] != b'MZ':
            return False, "Not a valid PE file (no MZ signature)"
        
        # Get PE offset
        pe_offset = struct.unpack('<I', data[60:64])[0]
        
        # Check PE signature
        if data[pe_offset:pe_offset+4] != b'PE\x00\x00':
            return False, "Not a valid PE file (no PE signature)"
        
        # Get optional header offset
        optional_header_offset = pe_offset + 4 + 20
        
        # Check magic (32-bit or 64-bit)
        magic = struct.unpack('<H', data[optional_header_offset:optional_header_offset+2])[0]
        is_64bit = (magic == 0x20b)
        
        # Get number of data directories
        if is_64bit:
            num_dd_offset = optional_header_offset + 108
        else:
            num_dd_offset = optional_header_offset + 92
        
        num_directories = struct.unpack('<I', data[num_dd_offset:num_dd_offset+4])[0]
        
        # Check if there's a CLI header (data directory 14)
        if num_directories >= 15:
            # Data directories start right after NumberOfRvaAndSizes
            dd_start = num_dd_offset + 4
            
            # CLI header is at index 14 (0-based)
            cli_header_entry = dd_start + (14 * 8)
            
            if cli_header_entry + 8 <= len(data):
                cli_rva = struct.unpack('<I', data[cli_header_entry:cli_header_entry+4])[0]
                cli_size = struct.unpack('<I', data[cli_header_entry+4:cli_header_entry+8])[0]
                
                if cli_rva != 0 and cli_size != 0:
                    return True, f".NET assembly detected (CLI header at RVA 0x{cli_rva:X})"
        
        return False, "Native PE executable (not .NET)"
        
    except Exception as e:
        return None, f"Error checking file: {e}"


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("""
.NET Executable Detector

Usage:
    python check_dotnet.py your_file.exe

This tool checks if an executable is a .NET assembly or a native PE file.

Why this matters:
  - This obfuscator is for NATIVE PE files only
  - .NET assemblies require special .NET obfuscators
  - Using this obfuscator on .NET files WILL BREAK THEM
        """)
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    print("\n" + "="*70)
    print("PE FILE TYPE DETECTOR".center(70))
    print("="*70 + "\n")
    
    print(f"[*] Checking: {file_path}\n")
    
    is_dotnet, message = check_if_dotnet(file_path)
    
    if is_dotnet is None:
        print(f"[-] {message}")
        sys.exit(1)
    elif is_dotnet:
        print("="*70)
        print("[!] .NET ASSEMBLY DETECTED [!]".center(70))
        print("="*70)
        print(f"\n[!] {message}")
        print("\n[!] WARNING: This file is a .NET application!")
        print("\n[X] DO NOT use this obfuscator on .NET files!")
        print("   - It will BREAK the executable")
        print("   - .NET requires special obfuscators")
        print("\n[+] For .NET obfuscation, use:")
        print("   - ConfuserEx (free, open source)")
        print("   - .NET Reactor (commercial)")
        print("   - Obfuscar (free)")
        print("   - Eazfuscator.NET (commercial)")
        print("   - Dotfuscator (commercial)")
        print("\n" + "="*70 + "\n")
        sys.exit(2)
    else:
        print("="*70)
        print("[+] NATIVE PE EXECUTABLE".center(70))
        print("="*70)
        print(f"\n[+] {message}")
        print("\n[+] This file is compatible with the obfuscator!")
        print("\n[*] You can safely obfuscate this file:")
        print(f"    python obfuscator.py {file_path}")
        print(f"    python obfuscator_max.py {file_path}")
        print("\n" + "="*70 + "\n")
        sys.exit(0)


if __name__ == '__main__':
    main()

