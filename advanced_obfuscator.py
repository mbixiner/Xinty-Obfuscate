"""
Advanced PE Obfuscator with Code Mutation
Includes more sophisticated obfuscation techniques
"""

import os
import struct
import random
import hashlib
from typing import List, Tuple


class AdvancedPEObfuscator:
    """Advanced obfuscation with code-level transformations"""
    
    def __init__(self, data: bytearray):
        self.data = data
    
    def insert_dead_code(self, section_data: bytearray, offset: int) -> bytearray:
        """Insert dead code that never executes"""
        dead_code_patterns = [
            # JMP +5, then 3 bytes junk, continues execution
            b'\xEB\x03\x90\x90\x90',
            # Push/Pop pair (no effect)
            b'\x50\x58',  # push eax, pop eax
            b'\x51\x59',  # push ecx, pop ecx
            # XOR reg, reg; XOR reg, reg (stays zero)
            b'\x31\xC0\x31\xC0',  # xor eax, eax; xor eax, eax
            # CLC, STC, CLC (flag manipulation, no effect if flags unused)
            b'\xF8\xF9\xF8',
        ]
        
        pattern = random.choice(dead_code_patterns)
        return section_data[:offset] + pattern + section_data[offset:]
    
    def add_stack_manipulation(self) -> bytes:
        """Generate stack manipulation instructions that have no net effect"""
        operations = [
            b'\x54\x5C',  # push esp, pop esp (unnecessary but valid)
            b'\x9C\x9D',  # pushf, popf
            b'\x50\x58',  # push eax, pop eax
            b'\x51\x59',  # push ecx, pop ecx
            b'\x52\x5A',  # push edx, pop edx
        ]
        return random.choice(operations)
    
    def create_junk_function(self, size: int = 32) -> bytes:
        """Create a junk function that looks valid but does nothing useful"""
        # Function prologue
        junk = b'\x55\x89\xE5'  # push ebp; mov ebp, esp
        
        # Random operations
        for _ in range(size - 10):
            ops = [
                b'\x90',  # nop
                b'\x31\xC0',  # xor eax, eax
                b'\x40',  # inc eax
                b'\x48',  # dec eax
                b'\x50\x58',  # push eax, pop eax
            ]
            junk += random.choice(ops)
        
        # Function epilogue
        junk += b'\x5D\xC3'  # pop ebp; ret
        
        return junk
    
    def apply_instruction_substitution(self, code: bytearray) -> bytearray:
        """Replace instructions with equivalent but different opcodes"""
        # This is a simplified example
        # Real implementation would need full x86 disassembly
        
        substitutions = {
            b'\x90': [  # NOP
                b'\x90',
                b'\x66\x90',  # 2-byte NOP
                b'\x87\xC0',  # xchg eax, eax
            ],
            b'\x31\xC0': [  # XOR EAX, EAX
                b'\x31\xC0',
                b'\x33\xC0',  # XOR EAX, EAX (alternative encoding)
            ],
        }
        
        result = bytearray()
        i = 0
        while i < len(code):
            found = False
            for pattern, replacements in substitutions.items():
                if code[i:i+len(pattern)] == pattern:
                    result.extend(random.choice(replacements))
                    i += len(pattern)
                    found = True
                    break
            
            if not found:
                result.append(code[i])
                i += 1
        
        return result
    
    def add_opaque_predicates(self) -> bytes:
        """Generate opaque predicates (always true/false conditions)"""
        predicates = [
            # (x^2 >= 0) - always true
            # Represented as conditional jump that always/never taken
            b'\x31\xC0'  # xor eax, eax
            b'\x40'      # inc eax  
            b'\x85\xC0'  # test eax, eax
            b'\x75\x02'  # jnz +2 (always taken if eax != 0)
            b'\xEB\x00', # jmp +0 (does nothing)
            
            # Always false: check if (x & 1) == (x + 1) & 1 for even x
            b'\x31\xC0'  # xor eax, eax
            b'\xA8\x01'  # test al, 1
            b'\x74\x02'  # jz +2 (taken if even)
            b'\xEB\x00', # jmp +0
        ]
        
        return random.choice(predicates)
    
    def polymorphic_encrypt_section(self, data: bytes, key: int = None) -> Tuple[bytes, bytes]:
        """
        Create polymorphic encryption with unique decryption stub each time
        Returns: (encrypted_data, decryption_stub)
        """
        if key is None:
            key = random.randint(1, 255)
        
        # Encrypt data with XOR
        encrypted = bytearray()
        for byte in data:
            encrypted.append(byte ^ key)
        
        # Generate unique decryption stub
        # This is a simplified x86 decryption stub
        # Real implementation would be much more complex
        
        stub_variants = [
            # Variant 1: Simple XOR loop
            f'''
            mov ecx, {len(data)}      ; Loop counter
            mov esi, [data_address]   ; Data pointer
            mov bl, {key}             ; XOR key
        decrypt_loop:
            xor byte ptr [esi], bl
            inc esi
            loop decrypt_loop
            ''',
            
            # Variant 2: XOR with different registers
            f'''
            mov edi, [data_address]
            mov edx, {len(data)}
            mov al, {key}
        decrypt_loop2:
            xor byte ptr [edi], al
            inc edi
            dec edx
            jnz decrypt_loop2
            ''',
        ]
        
        # For demonstration, return a comment about the stub
        stub_description = random.choice(stub_variants).encode()
        
        return bytes(encrypted), stub_description
    
    def create_metamorphic_code(self, original: bytes) -> bytes:
        """
        Create metamorphic version of code (reordered but functionally equivalent)
        This is a simplified demonstration
        """
        # In real metamorphism, we would:
        # 1. Disassemble the code
        # 2. Build control flow graph
        # 3. Reorder basic blocks
        # 4. Change instruction encoding
        # 5. Insert junk instructions
        # 6. Reassemble
        
        # Simplified: just add junk around the original code
        result = bytearray()
        
        # Add random junk before
        result.extend(self.create_junk_function(16))
        
        # Add original code
        result.extend(original)
        
        # Add random junk after
        result.extend(self.create_junk_function(16))
        
        return bytes(result)
    
    def calculate_code_hash(self, data: bytes) -> str:
        """Calculate hash of code section for verification"""
        return hashlib.sha256(data).hexdigest()
    
    def add_control_flow_flattening(self) -> bytes:
        """
        Generate control flow flattening pattern
        Converts linear code into switch-case dispatcher
        """
        # This is a template - real implementation needs full disassembly
        template = b'''
        ; Control flow dispatcher
        mov eax, 0              ; State = 0
        dispatcher:
        cmp eax, 0
        je state_0
        cmp eax, 1
        je state_1
        jmp exit
        state_0:
            ; ... code block 0 ...
            mov eax, 1
            jmp dispatcher
        state_1:
            ; ... code block 1 ...
            jmp exit
        exit:
            ret
        '''
        return template
    
    def add_string_encryption(self, strings: List[bytes]) -> List[Tuple[bytes, int]]:
        """Encrypt strings with unique keys"""
        encrypted_strings = []
        
        for s in strings:
            key = random.randint(1, 255)
            encrypted = bytearray()
            for byte in s:
                encrypted.append(byte ^ key)
            encrypted_strings.append((bytes(encrypted), key))
        
        return encrypted_strings
    
    def generate_api_obfuscation_stub(self, api_name: str) -> bytes:
        """Generate code to resolve API dynamically instead of using IAT"""
        # Template for dynamic API resolution
        # In practice, this would call GetProcAddress
        stub = f'''
        ; Dynamic resolution of {api_name}
        push {hash(api_name) & 0xFFFFFFFF}  ; Hash of API name
        call resolve_api                     ; Custom resolver function
        call eax                             ; Call the API
        '''.encode()
        
        return stub
    
    def apply_register_renaming(self, code: bytes) -> bytes:
        """
        Rename registers in code (requires disassembly)
        This is a placeholder for the concept
        """
        # Would require full disassembly and reassembly
        # Changing register allocations while maintaining semantics
        return code  # Placeholder
    
    def insert_anti_disassembly_tricks(self) -> List[bytes]:
        """Generate anti-disassembly patterns"""
        tricks = [
            # Overlapping instructions
            b'\xE8\x00\x00\x00\x00'  # call $+5
            b'\xC3',                  # ret (looks like end of function)
            # But execution continues here
            
            # Fake conditional jumps
            b'\x74\x01'  # jz +1
            b'\xE9',     # Start of jmp instruction
            # Disassembler thinks jmp is here, but jz skips it
            
            # Invalid instruction that's never executed
            b'\xEB\x02'  # jmp +2
            b'\xFF\xFF'  # Invalid (never executed)
            
            # Return-oriented tricks
            b'\xE8\x00\x00\x00\x00'  # call $+5
            b'\x83\x04\x24\x05'      # add dword [esp], 5
            b'\xC3',                  # ret (jumps 5 bytes ahead)
        ]
        
        return tricks


def demonstrate_advanced_techniques():
    """Demonstrate advanced obfuscation techniques"""
    print("\n" + "="*60)
    print("ADVANCED OBFUSCATION TECHNIQUES DEMO".center(60))
    print("="*60 + "\n")
    
    # Create dummy data
    dummy_data = bytearray(b'\x90' * 1000)
    obf = AdvancedPEObfuscator(dummy_data)
    
    print("[*] 1. Dead Code Insertion")
    dead_code = obf.insert_dead_code(bytearray(b'\x90\x90\x90'), 1)
    print(f"    Original: 90 90 90")
    print(f"    Modified: {dead_code.hex()}")
    
    print("\n[*] 2. Junk Function Generation")
    junk_func = obf.create_junk_function(20)
    print(f"    Generated: {junk_func.hex()}")
    
    print("\n[*] 3. Polymorphic Encryption")
    test_data = b"SECRET_DATA_HERE"
    encrypted, stub = obf.polymorphic_encrypt_section(test_data)
    print(f"    Original: {test_data.hex()}")
    print(f"    Encrypted: {encrypted.hex()}")
    print(f"    Hash: {obf.calculate_code_hash(encrypted)}")
    
    print("\n[*] 4. String Encryption")
    strings = [b"kernel32.dll", b"GetProcAddress", b"LoadLibraryA"]
    encrypted_strings = obf.add_string_encryption(strings)
    for i, (enc, key) in enumerate(encrypted_strings):
        print(f"    String {i}: {strings[i]} -> {enc.hex()} (key: 0x{key:02X})")
    
    print("\n[*] 5. Anti-Disassembly Tricks")
    tricks = obf.insert_anti_disassembly_tricks()
    for i, trick in enumerate(tricks):
        print(f"    Trick {i+1}: {trick.hex()}")
    
    print("\n[*] 6. Opaque Predicates")
    predicate = obf.add_opaque_predicates()
    print(f"    Generated: {predicate.hex()}")
    
    print("\n" + "="*60)
    print("[+] Demo completed!")
    print("="*60 + "\n")


if __name__ == '__main__':
    demonstrate_advanced_techniques()

