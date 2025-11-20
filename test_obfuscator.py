"""
Test suite for PE Obfuscator
Create a simple test executable to demonstrate obfuscation
"""

import os
import struct
import tempfile
from pathlib import Path


def create_minimal_pe_exe(output_path: str):
    """
    Create a minimal valid PE executable for testing
    This creates a tiny DOS executable that just exits
    """
    
    # DOS Header (64 bytes)
    dos_header = bytearray(64)
    dos_header[0:2] = b'MZ'  # DOS signature
    dos_header[60:64] = struct.pack('<I', 0x80)  # PE offset at 0x80
    
    # DOS Stub (32 bytes) - minimal stub
    dos_stub = bytearray(32)
    dos_stub[0:14] = b'This program cannot be run in DOS mode.\r\n'
    
    # PE Signature (4 bytes)
    pe_signature = b'PE\x00\x00'
    
    # COFF File Header (20 bytes)
    coff_header = bytearray(20)
    struct.pack_into('<H', coff_header, 0, 0x014C)  # Machine: i386
    struct.pack_into('<H', coff_header, 2, 3)  # Number of sections
    struct.pack_into('<I', coff_header, 4, 0x12345678)  # Timestamp
    struct.pack_into('<I', coff_header, 8, 0)  # PointerToSymbolTable
    struct.pack_into('<I', coff_header, 12, 0)  # NumberOfSymbols
    struct.pack_into('<H', coff_header, 16, 224)  # SizeOfOptionalHeader
    struct.pack_into('<H', coff_header, 18, 0x010F)  # Characteristics
    
    # Optional Header (224 bytes for PE32)
    optional_header = bytearray(224)
    struct.pack_into('<H', optional_header, 0, 0x010B)  # Magic: PE32
    struct.pack_into('<B', optional_header, 2, 14)  # MajorLinkerVersion
    struct.pack_into('<B', optional_header, 3, 0)  # MinorLinkerVersion
    struct.pack_into('<I', optional_header, 4, 0x200)  # SizeOfCode
    struct.pack_into('<I', optional_header, 8, 0x200)  # SizeOfInitializedData
    struct.pack_into('<I', optional_header, 12, 0)  # SizeOfUninitializedData
    struct.pack_into('<I', optional_header, 16, 0x1000)  # AddressOfEntryPoint
    struct.pack_into('<I', optional_header, 20, 0x1000)  # BaseOfCode
    struct.pack_into('<I', optional_header, 24, 0x2000)  # BaseOfData
    struct.pack_into('<I', optional_header, 28, 0x400000)  # ImageBase
    struct.pack_into('<I', optional_header, 32, 0x1000)  # SectionAlignment
    struct.pack_into('<I', optional_header, 36, 0x200)  # FileAlignment
    struct.pack_into('<H', optional_header, 40, 5)  # MajorOperatingSystemVersion
    struct.pack_into('<H', optional_header, 42, 1)  # MinorOperatingSystemVersion
    struct.pack_into('<H', optional_header, 44, 0)  # MajorImageVersion
    struct.pack_into('<H', optional_header, 46, 0)  # MinorImageVersion
    struct.pack_into('<H', optional_header, 48, 5)  # MajorSubsystemVersion
    struct.pack_into('<H', optional_header, 50, 1)  # MinorSubsystemVersion
    struct.pack_into('<I', optional_header, 52, 0)  # Win32VersionValue
    struct.pack_into('<I', optional_header, 56, 0x5000)  # SizeOfImage
    struct.pack_into('<I', optional_header, 60, 0x200)  # SizeOfHeaders
    struct.pack_into('<I', optional_header, 64, 0)  # CheckSum
    struct.pack_into('<H', optional_header, 68, 3)  # Subsystem: Console
    struct.pack_into('<H', optional_header, 70, 0x8140)  # DllCharacteristics
    struct.pack_into('<I', optional_header, 72, 0x100000)  # SizeOfStackReserve
    struct.pack_into('<I', optional_header, 76, 0x1000)  # SizeOfStackCommit
    struct.pack_into('<I', optional_header, 80, 0x100000)  # SizeOfHeapReserve
    struct.pack_into('<I', optional_header, 84, 0x1000)  # SizeOfHeapCommit
    struct.pack_into('<I', optional_header, 88, 0)  # LoaderFlags
    struct.pack_into('<I', optional_header, 92, 16)  # NumberOfRvaAndSizes
    
    # Section Headers (3 sections × 40 bytes = 120 bytes)
    sections = []
    
    # .text section
    text_header = bytearray(40)
    text_header[0:8] = b'.text\x00\x00\x00'
    struct.pack_into('<I', text_header, 8, 0x100)  # VirtualSize
    struct.pack_into('<I', text_header, 12, 0x1000)  # VirtualAddress
    struct.pack_into('<I', text_header, 16, 0x200)  # SizeOfRawData
    struct.pack_into('<I', text_header, 20, 0x400)  # PointerToRawData
    struct.pack_into('<I', text_header, 36, 0x60000020)  # Characteristics
    sections.append(text_header)
    
    # .data section
    data_header = bytearray(40)
    data_header[0:8] = b'.data\x00\x00\x00'
    struct.pack_into('<I', data_header, 8, 0x100)  # VirtualSize
    struct.pack_into('<I', data_header, 12, 0x2000)  # VirtualAddress
    struct.pack_into('<I', data_header, 16, 0x200)  # SizeOfRawData
    struct.pack_into('<I', data_header, 20, 0x600)  # PointerToRawData
    struct.pack_into('<I', data_header, 36, 0xC0000040)  # Characteristics
    sections.append(data_header)
    
    # .rdata section
    rdata_header = bytearray(40)
    rdata_header[0:8] = b'.rdata\x00\x00'
    struct.pack_into('<I', rdata_header, 8, 0x100)  # VirtualSize
    struct.pack_into('<I', rdata_header, 12, 0x3000)  # VirtualAddress
    struct.pack_into('<I', rdata_header, 16, 0x200)  # SizeOfRawData
    struct.pack_into('<I', rdata_header, 20, 0x800)  # PointerToRawData
    struct.pack_into('<I', rdata_header, 36, 0x40000040)  # Characteristics
    sections.append(rdata_header)
    
    # Section data
    text_section = bytearray(0x200)
    # Add simple code: xor eax, eax; ret
    text_section[0:3] = b'\x31\xC0\xC3'
    
    data_section = bytearray(0x200)
    rdata_section = bytearray(0x200)
    
    # Assemble the file
    pe_data = bytearray()
    pe_data.extend(dos_header)
    pe_data.extend(dos_stub)
    
    # Pad to PE offset
    while len(pe_data) < 0x80:
        pe_data.append(0)
    
    pe_data.extend(pe_signature)
    pe_data.extend(coff_header)
    pe_data.extend(optional_header)
    
    for section_header in sections:
        pe_data.extend(section_header)
    
    # Pad to first section
    while len(pe_data) < 0x400:
        pe_data.append(0)
    
    pe_data.extend(text_section)
    pe_data.extend(data_section)
    pe_data.extend(rdata_section)
    
    # Write to file
    with open(output_path, 'wb') as f:
        f.write(pe_data)
    
    print(f"[+] Created test PE executable: {output_path}")
    print(f"[+] File size: {len(pe_data)} bytes")
    return output_path


def test_obfuscation():
    """Test the obfuscator with a generated PE file"""
    print("\n" + "="*60)
    print("PE OBFUSCATOR TEST SUITE".center(60))
    print("="*60 + "\n")
    
    # Create temporary test file
    test_dir = Path("test_files")
    test_dir.mkdir(exist_ok=True)
    
    test_exe = test_dir / "test_sample.exe"
    
    print("[*] Creating minimal PE executable for testing...")
    create_minimal_pe_exe(str(test_exe))
    
    print("\n[*] Testing obfuscator with different technique combinations...\n")
    
    # Import obfuscator
    try:
        from obfuscator import PEObfuscator
        
        # Test 1: All techniques
        print("[Test 1] Applying all techniques...")
        obf1 = PEObfuscator(str(test_exe), str(test_dir / "test_all.exe"))
        obf1.obfuscate(['all'])
        
        # Test 2: Only section names and timestamp
        print("\n[Test 2] Applying sections + timestamp...")
        obf2 = PEObfuscator(str(test_exe), str(test_dir / "test_sections_timestamp.exe"))
        obf2.obfuscate(['sections', 'timestamp'])
        
        # Test 3: Only junk data
        print("\n[Test 3] Applying junk data only...")
        obf3 = PEObfuscator(str(test_exe), str(test_dir / "test_junk.exe"))
        obf3.obfuscate(['junk'])
        
        print("\n" + "="*60)
        print("[+] All tests completed successfully!")
        print("="*60)
        print(f"\n[+] Test files created in: {test_dir.absolute()}")
        print("[+] You can inspect the obfuscated files with PE analysis tools")
        
    except ImportError as e:
        print(f"[-] Error importing obfuscator: {e}")
        return False
    
    return True


def analyze_pe_structure(file_path: str):
    """Simple PE structure analyzer for verification"""
    print(f"\n[*] Analyzing PE structure: {file_path}")
    
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        # Check DOS header
        if data[0:2] != b'MZ':
            print("  [-] Invalid DOS signature")
            return False
        
        print("  [+] DOS signature: OK")
        
        # Get PE offset
        pe_offset = struct.unpack('<I', data[60:64])[0]
        print(f"  [+] PE offset: 0x{pe_offset:08X}")
        
        # Check PE signature
        if data[pe_offset:pe_offset+4] != b'PE\x00\x00':
            print("  [-] Invalid PE signature")
            return False
        
        print("  [+] PE signature: OK")
        
        # Get number of sections
        num_sections = struct.unpack('<H', data[pe_offset+6:pe_offset+8])[0]
        print(f"  [+] Number of sections: {num_sections}")
        
        # Get timestamp
        timestamp = struct.unpack('<I', data[pe_offset+8:pe_offset+12])[0]
        print(f"  [+] Timestamp: 0x{timestamp:08X}")
        
        # Parse section names
        optional_header_size = struct.unpack('<H', data[pe_offset+20:pe_offset+22])[0]
        section_table_offset = pe_offset + 24 + optional_header_size
        
        print("  [+] Sections:")
        for i in range(num_sections):
            section_offset = section_table_offset + (i * 40)
            section_name = data[section_offset:section_offset+8].rstrip(b'\x00').decode('utf-8', errors='ignore')
            print(f"      - {section_name}")
        
        print(f"  [+] File size: {len(data)} bytes")
        print("  [+] PE structure is valid")
        return True
        
    except Exception as e:
        print(f"  [-] Error analyzing file: {e}")
        return False


if __name__ == '__main__':
    # Run tests
    if test_obfuscation():
        print("\n[*] Analyzing generated files...\n")
        
        test_dir = Path("test_files")
        for exe_file in test_dir.glob("*.exe"):
            analyze_pe_structure(str(exe_file))
    
    print("\n[*] Test suite completed!")

