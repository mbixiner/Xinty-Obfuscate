"""
PE Executable Obfuscator - MAXIMUM STRENGTH VERSION
Advanced obfuscator with all techniques enabled for maximum protection
"""

import os
import sys
import struct
import random
import string
import argparse
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple


class MaxPEObfuscator:
    """Maximum strength PE obfuscator with advanced techniques"""
    
    DOS_HEADER_SIZE = 64
    PE_SIGNATURE_SIZE = 4
    FILE_HEADER_SIZE = 20
    OPTIONAL_HEADER_32_SIZE = 96
    OPTIONAL_HEADER_64_SIZE = 112
    SECTION_HEADER_SIZE = 40
    
    def __init__(self, input_file: str, output_file: str = None):
        self.input_file = input_file
        self.output_file = output_file or self._generate_output_name(input_file)
        self.data = None
        self.dos_header = None
        self.pe_offset = None
        self.file_header_offset = None
        self.optional_header_offset = None
        self.section_headers_offset = None
        self.is_64bit = False
        self.number_of_sections = 0
        self.sections = []
        self.entry_point = 0
        self.image_base = 0
        
    def _generate_output_name(self, input_file: str) -> str:
        """Generate obfuscated output filename"""
        path = Path(input_file)
        return str(path.parent / f"{path.stem}_max_obfuscated{path.suffix}")
    
    def load_file(self):
        """Load the PE file into memory"""
        try:
            with open(self.input_file, 'rb') as f:
                self.data = bytearray(f.read())
            print(f"[+] Loaded {len(self.data)} bytes from {self.input_file}")
            return True
        except Exception as e:
            print(f"[-] Error loading file: {e}")
            return False
    
    def parse_headers(self):
        """Parse PE headers"""
        try:
            if self.data[0:2] != b'MZ':
                print("[-] Invalid DOS signature")
                return False
            
            self.pe_offset = struct.unpack('<I', self.data[60:64])[0]
            
            if self.data[self.pe_offset:self.pe_offset+4] != b'PE\x00\x00':
                print("[-] Invalid PE signature")
                return False
            
            self.file_header_offset = self.pe_offset + self.PE_SIGNATURE_SIZE
            self.number_of_sections = struct.unpack('<H', 
                self.data[self.file_header_offset+2:self.file_header_offset+4])[0]
            
            self.optional_header_offset = self.file_header_offset + self.FILE_HEADER_SIZE
            magic = struct.unpack('<H', self.data[self.optional_header_offset:self.optional_header_offset+2])[0]
            self.is_64bit = (magic == 0x20b)
            
            # Get entry point and image base
            self.entry_point = struct.unpack('<I', self.data[self.optional_header_offset+16:self.optional_header_offset+20])[0]
            if self.is_64bit:
                self.image_base = struct.unpack('<Q', self.data[self.optional_header_offset+24:self.optional_header_offset+32])[0]
            else:
                self.image_base = struct.unpack('<I', self.data[self.optional_header_offset+28:self.optional_header_offset+32])[0]
            
            optional_header_size = struct.unpack('<H', 
                self.data[self.file_header_offset+16:self.file_header_offset+18])[0]
            self.section_headers_offset = self.optional_header_offset + optional_header_size
            
            for i in range(self.number_of_sections):
                section_offset = self.section_headers_offset + (i * self.SECTION_HEADER_SIZE)
                section_data = self._parse_section_header(section_offset)
                self.sections.append(section_data)
            
            print(f"[+] PE file parsed: {'64-bit' if self.is_64bit else '32-bit'}, {self.number_of_sections} sections")
            return True
            
        except Exception as e:
            print(f"[-] Error parsing headers: {e}")
            return False
    
    def _parse_section_header(self, offset: int) -> Dict:
        """Parse a single section header"""
        name = self.data[offset:offset+8].rstrip(b'\x00')
        virtual_size = struct.unpack('<I', self.data[offset+8:offset+12])[0]
        virtual_address = struct.unpack('<I', self.data[offset+12:offset+16])[0]
        raw_size = struct.unpack('<I', self.data[offset+16:offset+20])[0]
        raw_address = struct.unpack('<I', self.data[offset+20:offset+24])[0]
        characteristics = struct.unpack('<I', self.data[offset+36:offset+40])[0]
        
        return {
            'name': name,
            'offset': offset,
            'virtual_size': virtual_size,
            'virtual_address': virtual_address,
            'raw_size': raw_size,
            'raw_address': raw_address,
            'characteristics': characteristics
        }
    
    def obfuscate_section_names_advanced(self):
        """Advanced section name randomization with realistic fake names"""
        print("[*] Advanced section name obfuscation...")
        
        # Use realistic section names to blend in
        fake_names = [
            '.text', '.code', '.itext', '.text0', '.text1',
            '.data', '.rdata', '.idata', '.edata', '.pdata',
            '.rsrc', '.reloc', '.tls', '.bss', '.debug',
            '.init', '.fini', '.rodata', '.sdata', '.sbss'
        ]
        
        # Mix of obvious obfuscation and subtle mimicry
        strategy = random.choice(['realistic', 'random', 'mixed'])
        
        for section in self.sections:
            old_name = section['name'].decode('utf-8', errors='ignore')
            
            if strategy == 'realistic':
                # Use realistic but wrong section names
                new_name = random.choice(fake_names)
                while new_name == old_name:
                    new_name = random.choice(fake_names)
            elif strategy == 'random':
                # Completely random
                new_name = '.' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(5, 7)))
            else:
                # Mix: some realistic, some random
                if random.random() < 0.5:
                    new_name = random.choice(fake_names)
                else:
                    new_name = '.' + ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 7)))
            
            new_name_bytes = new_name.encode('utf-8').ljust(8, b'\x00')[:8]
            self.data[section['offset']:section['offset']+8] = new_name_bytes
            print(f"  [+] {old_name.ljust(10)} -> {new_name}")
    
    def remove_rich_header(self):
        """Remove or corrupt the Rich header"""
        print("[*] Removing Rich header...")
        
        # Rich header is between DOS stub and PE header
        # Look for 'Rich' signature
        rich_pos = self.data.find(b'Rich', 0, self.pe_offset)
        
        if rich_pos != -1:
            # Found Rich header, corrupt it
            # Rich header starts with 'DanS' (XOR encrypted) and ends with 'Rich'
            dans_pos = rich_pos - 4
            while dans_pos > 64:
                # Look backwards for potential start
                if dans_pos + 60 < rich_pos:
                    # Overwrite with random data
                    for i in range(dans_pos, rich_pos + 8):
                        if i < self.pe_offset:
                            self.data[i] = random.randint(0, 255)
                    print(f"  [+] Corrupted Rich header at offset 0x{rich_pos:X}")
                    return
                dans_pos -= 4
            
            # Just corrupt the Rich signature
            for i in range(rich_pos, min(rich_pos + 8, self.pe_offset)):
                self.data[i] = random.randint(0, 255)
            print(f"  [+] Corrupted Rich signature")
        else:
            print("  [i] No Rich header found")
    
    def modify_timestamps_advanced(self):
        """Advanced timestamp modification with realistic values"""
        print("[*] Advanced timestamp modification...")
        
        # Set multiple timestamps to confuse
        timestamp_offset = self.file_header_offset + 4
        
        # Choose a strategy
        strategies = ['zero', 'old', 'future', 'random']
        strategy = random.choice(strategies)
        
        if strategy == 'zero':
            timestamp = 0
            print("  [+] Set timestamp to 0 (stripped)")
        elif strategy == 'old':
            # Very old date (1990s)
            timestamp = random.randint(0x2A000000, 0x3A000000)
            print(f"  [+] Set timestamp to old date: 0x{timestamp:08X}")
        elif strategy == 'future':
            # Future date
            timestamp = random.randint(0x70000000, 0x7FFFFFFF)
            print(f"  [+] Set timestamp to future date: 0x{timestamp:08X}")
        else:
            # Random
            timestamp = random.randint(0, 0xFFFFFFFF)
            print(f"  [+] Set timestamp to random: 0x{timestamp:08X}")
        
        struct.pack_into('<I', self.data, timestamp_offset, timestamp)
    
    def add_junk_sections_advanced(self):
        """Add massive amounts of junk data with various patterns"""
        print("[*] Adding advanced junk data...")
        
        # Add multiple layers of different junk
        layers = random.randint(5, 10)
        total_added = 0
        
        for i in range(layers):
            junk_type = random.choice(['random', 'pattern', 'encrypted', 'compressed'])
            size = random.randint(2048, 8192)
            
            if junk_type == 'random':
                # Pure random
                junk = bytes([random.randint(0, 255) for _ in range(size)])
            elif junk_type == 'pattern':
                # Repeating pattern
                pattern = bytes([random.randint(0, 255) for _ in range(16)])
                junk = pattern * (size // 16)
            elif junk_type == 'encrypted':
                # XOR encrypted looking data
                key = random.randint(1, 255)
                junk = bytes([random.randint(0, 255) ^ key for _ in range(size)])
            else:
                # High entropy "compressed" looking data
                junk = hashlib.sha256(str(random.random()).encode()).digest() * (size // 32)
            
            self.data.extend(junk)
            total_added += len(junk)
        
        print(f"  [+] Added {total_added} bytes in {layers} layers")
    
    def fill_code_caves_advanced(self):
        """Advanced code cave filling with valid x86/x64 instructions"""
        print("[*] Advanced code cave filling...")
        
        # More sophisticated NOP-equivalent instructions
        nop_sequences = [
            b'\x90',                          # NOP
            b'\x66\x90',                      # 66 NOP
            b'\x0F\x1F\x00',                  # NOP DWORD PTR [EAX]
            b'\x0F\x1F\x40\x00',              # NOP DWORD PTR [EAX+0]
            b'\x0F\x1F\x44\x00\x00',          # NOP DWORD PTR [EAX+EAX+0]
            b'\x87\xC0',                      # XCHG EAX, EAX
            b'\x87\xDB',                      # XCHG EBX, EBX
            b'\x8B\xC0',                      # MOV EAX, EAX
            b'\x8D\x00',                      # LEA EAX, [EAX]
            b'\x8D\x40\x00',                  # LEA EAX, [EAX+0]
            b'\x8D\x49\x00',                  # LEA ECX, [ECX+0]
            b'\x8D\x52\x00',                  # LEA EDX, [EDX+0]
        ]
        
        for section in self.sections:
            characteristics = section['characteristics']
            if characteristics & 0x20000000:  # Executable section
                start = section['raw_address']
                size = section['raw_size']
                
                if start + size <= len(self.data):
                    caves_filled = 0
                    i = start
                    
                    while i < start + size - 32:
                        # Look for caves (at least 8 null bytes)
                        if self.data[i:i+8] == b'\x00' * 8:
                            cave_size = 8
                            while i + cave_size < start + size and self.data[i + cave_size] == 0:
                                cave_size += 1
                            
                            # Fill with varied NOP sequences
                            j = i
                            while j < i + cave_size:
                                seq = random.choice(nop_sequences)
                                for k, byte in enumerate(seq):
                                    if j + k < i + cave_size:
                                        self.data[j + k] = byte
                                j += len(seq)
                            
                            caves_filled += 1
                            i += cave_size
                        else:
                            i += 1
                    
                    if caves_filled > 0:
                        print(f"  [+] Filled {caves_filled} code caves in {section['name'].decode('utf-8', errors='ignore')}")
    
    def modify_dos_stub_advanced(self):
        """Advanced DOS stub modification"""
        print("[*] Advanced DOS stub modification...")
        
        stub_start = 0x40
        stub_end = self.pe_offset
        
        if stub_end - stub_start > 20:
            # Multiple strategies
            strategy = random.choice(['custom_message', 'junk', 'fake_code'])
            
            if strategy == 'custom_message':
                messages = [
                    b"Runtime error occurred.\r\n$",
                    b"Access denied in this mode.\r\n$",
                    b"Invalid system configuration.\r\n$",
                    b"Unsupported OS version.\r\n$",
                    b"Memory allocation failed.\r\n$",
                ]
                message = random.choice(messages)
            elif strategy == 'junk':
                # Fill with junk
                message = bytes([random.randint(32, 126) for _ in range(30)])
            else:
                # Fake code-like data
                message = bytes([random.randint(0, 255) for _ in range(30)])
            
            # Preserve DOS stub code structure but change message
            message_offset = stub_start + 14
            if message_offset + len(message) < stub_end - 4:
                self.data[message_offset:message_offset + len(message)] = message
                print(f"  [+] DOS stub modified with strategy: {strategy}")
    
    def corrupt_checksum_advanced(self):
        """Set checksum to specific misleading values"""
        print("[*] Advanced checksum corruption...")
        
        checksum_offset = self.optional_header_offset + 64
        
        # Different strategies
        strategies = ['zero', 'max', 'random', 'fake']
        strategy = random.choice(strategies)
        
        if strategy == 'zero':
            checksum = 0
            print("  [+] Checksum set to 0")
        elif strategy == 'max':
            checksum = 0xFFFFFFFF
            print("  [+] Checksum set to max value")
        elif strategy == 'fake':
            # Calculate a fake but realistic looking checksum
            checksum = len(self.data) ^ 0xDEADBEEF
            print(f"  [+] Checksum set to fake value: 0x{checksum:08X}")
        else:
            checksum = random.randint(0x10000000, 0xFFFFFFF0)
            print(f"  [+] Checksum set to random: 0x{checksum:08X}")
        
        struct.pack_into('<I', self.data, checksum_offset, checksum)
    
    def add_anti_debug_junk(self):
        """Add anti-debugging strings and patterns in overlay"""
        print("[*] Adding anti-debug patterns...")
        
        # Add various anti-debug markers
        markers = [
            b'IsDebuggerPresent',
            b'CheckRemoteDebuggerPresent',
            b'NtQueryInformationProcess',
            b'OutputDebugString',
            b'DebugBreakProcess',
            b'GetTickCount',
            b'QueryPerformanceCounter',
            b'ZwQueryInformationThread',
            b'NtSetInformationThread',
            b'SeDebugPrivilege',
            b'KERNEL32.DLL',
            b'NTDLL.DLL',
            b'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\AeDebug',
            b'INT 2D',
            b'INT 3',
            b'CPUID',
        ]
        
        # Shuffle and add with junk in between
        random.shuffle(markers)
        for marker in markers:
            self.data.extend(marker)
            self.data.extend(b'\x00' * random.randint(20, 100))
            # Add some fake code patterns
            self.data.extend(bytes([random.randint(0, 255) for _ in range(random.randint(10, 50))]))
        
        print(f"  [+] Added {len(markers)} anti-debug markers")
    
    def modify_characteristics(self):
        """Modify PE characteristics flags"""
        print("[*] Modifying PE characteristics...")
        
        # File characteristics offset
        char_offset = self.file_header_offset + 18
        characteristics = struct.unpack('<H', self.data[char_offset:char_offset+2])[0]
        
        # Add/modify flags
        # Set LINE_NUMS_STRIPPED, LOCAL_SYMS_STRIPPED, DEBUG_STRIPPED
        characteristics |= 0x0004  # LINE_NUMS_STRIPPED
        characteristics |= 0x0008  # LOCAL_SYMS_STRIPPED
        
        # Maybe flip some other flags
        if random.random() < 0.5:
            characteristics ^= 0x0001  # Toggle RELOCS_STRIPPED
        
        struct.pack_into('<H', self.data, char_offset, characteristics)
        print(f"  [+] Characteristics modified to: 0x{characteristics:04X}")
    
    def randomize_subsystem_version(self):
        """Randomize subsystem version numbers"""
        print("[*] Randomizing subsystem version...")
        
        # MajorSubsystemVersion at optional_header + 48
        # MinorSubsystemVersion at optional_header + 50
        major = random.choice([4, 5, 6, 10])  # Common Windows versions
        minor = random.randint(0, 3)
        
        struct.pack_into('<H', self.data, self.optional_header_offset + 48, major)
        struct.pack_into('<H', self.data, self.optional_header_offset + 50, minor)
        
        print(f"  [+] Subsystem version set to {major}.{minor}")
    
    def add_fake_data_directories(self):
        """Modify data directory entries to add confusion"""
        print("[*] Modifying data directories...")
        
        # Data directories start at optional_header + 96 (32-bit) or + 112 (64-bit)
        dd_offset = self.optional_header_offset + (112 if self.is_64bit else 96)
        
        # There are 16 data directories (128 bytes total)
        # Some are not commonly used, we can set them to fake values
        
        # Indexes of rarely used directories we can fake
        # 5 = Base Relocation (we'll leave alone)
        # 11 = Bound Import
        # 12 = IAT
        # 13 = Delay Import Descriptor
        
        modifications = 0
        
        # Bound Import (index 11) - set to zero or random
        if random.random() < 0.5:
            struct.pack_into('<II', self.data, dd_offset + (11 * 8), 0, 0)
            modifications += 1
        
        print(f"  [+] Modified {modifications} data directory entries")
    
    def insert_junk_at_headers(self):
        """Insert junk padding between headers"""
        print("[*] Inserting junk in header padding...")
        
        # Find padding space between section headers and first section
        if self.sections:
            first_section_offset = min(s['raw_address'] for s in self.sections if s['raw_address'] > 0)
            headers_end = self.section_headers_offset + (self.number_of_sections * self.SECTION_HEADER_SIZE)
            
            if first_section_offset > headers_end:
                padding_size = first_section_offset - headers_end
                # Fill padding with junk (but keep some structure)
                for i in range(headers_end, first_section_offset):
                    if random.random() < 0.7:  # 70% junk, 30% zeros
                        self.data[i] = random.randint(0, 255)
                
                print(f"  [+] Filled {padding_size} bytes of header padding")
    
    def obfuscate_max(self):
        """Apply maximum obfuscation"""
        print("\n" + "="*70)
        print("MAXIMUM STRENGTH PE OBFUSCATOR".center(70))
        print("="*70 + "\n")
        
        if not self.load_file():
            return False
        
        if not self.parse_headers():
            return False
        
        print(f"\n[*] Applying MAXIMUM obfuscation...\n")
        
        # Apply ALL techniques
        self.obfuscate_section_names_advanced()
        self.remove_rich_header()
        self.modify_timestamps_advanced()
        self.modify_dos_stub_advanced()
        self.corrupt_checksum_advanced()
        self.modify_characteristics()
        self.randomize_subsystem_version()
        self.add_fake_data_directories()
        self.insert_junk_at_headers()
        self.fill_code_caves_advanced()
        self.add_junk_sections_advanced()
        self.add_anti_debug_junk()
        
        print("\n" + "="*70)
        return self.save_file()
    
    def save_file(self):
        """Save the obfuscated file"""
        try:
            with open(self.output_file, 'wb') as f:
                f.write(self.data)
            print(f"[+] Maximum obfuscated file saved: {self.output_file}")
            print(f"[+] Original size: {os.path.getsize(self.input_file)} bytes")
            print(f"[+] Obfuscated size: {len(self.data)} bytes")
            size_increase = len(self.data) - os.path.getsize(self.input_file)
            print(f"[+] Size increase: {size_increase} bytes ({(size_increase/os.path.getsize(self.input_file)*100):.1f}%)")
            return True
        except Exception as e:
            print(f"[-] Error saving file: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description='Maximum Strength PE Obfuscator - Most aggressive obfuscation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
This is the MAXIMUM STRENGTH version with ALL obfuscation techniques enabled.

Techniques applied:
  ✓ Advanced section name obfuscation
  ✓ Rich header removal/corruption
  ✓ Advanced timestamp manipulation
  ✓ DOS stub advanced modification
  ✓ Checksum corruption with strategies
  ✓ PE characteristics modification
  ✓ Subsystem version randomization
  ✓ Data directory manipulation
  ✓ Header padding junk insertion
  ✓ Advanced code cave filling (varied NOPs)
  ✓ Multi-layer junk data (10+ KB)
  ✓ Anti-debug markers and strings
  
WARNING: This creates the most obfuscated output possible!
  - Significantly increases file size (10-50KB+)
  - May trigger more AV detection
  - Always test the output file
  
Examples:
  python obfuscator_max.py input.exe
  python obfuscator_max.py input.exe -o protected.exe
        '''
    )
    
    parser.add_argument('input', help='Input PE file (.exe)')
    parser.add_argument('-o', '--output', help='Output file (default: input_max_obfuscated.exe)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"[-] Error: Input file '{args.input}' not found")
        sys.exit(1)
    
    obfuscator = MaxPEObfuscator(args.input, args.output)
    success = obfuscator.obfuscate_max()
    
    if success:
        print("\n" + "="*70)
        print("[+] MAXIMUM OBFUSCATION COMPLETED!".center(70))
        print("="*70)
        print("\n[!] WARNING: Test the obfuscated file thoroughly!")
        print("[!] WARNING: May trigger antivirus detection")
        print("[!] WARNING: File size significantly increased")
        print("\n[*] Techniques applied:")
        print("    - Advanced section name obfuscation")
        print("    - Rich header removal")
        print("    - Timestamp manipulation")
        print("    - DOS stub modification")
        print("    - Checksum corruption")
        print("    - PE characteristics modification")
        print("    - Subsystem version randomization")
        print("    - Data directory manipulation")
        print("    - Header padding junk")
        print("    - Advanced code cave filling")
        print("    - Multi-layer junk data (10-50KB)")
        print("    - Anti-debug markers")
        print("\n[+] Ready for distribution (after testing!)\n")
        sys.exit(0)
    else:
        print("\n[-] Maximum obfuscation failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()

