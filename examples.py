"""
Example usage scripts for PE Obfuscator
"""

from obfuscator import PEObfuscator
from pathlib import Path


def example_basic_obfuscation():
    """Example 1: Basic obfuscation with all techniques"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Obfuscation")
    print("="*60 + "\n")
    
    input_file = "myapp.exe"
    output_file = "myapp_protected.exe"
    
    obf = PEObfuscator(input_file, output_file)
    obf.obfuscate(['all'])
    
    print(f"\n[+] Obfuscated {input_file} -> {output_file}")


def example_custom_techniques():
    """Example 2: Custom technique selection"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Custom Techniques")
    print("="*60 + "\n")
    
    input_file = "myapp.exe"
    output_file = "myapp_custom.exe"
    
    # Only use safe techniques that won't break functionality
    techniques = ['sections', 'timestamp', 'junk']
    
    obf = PEObfuscator(input_file, output_file)
    obf.obfuscate(techniques)
    
    print(f"\n[+] Applied techniques: {', '.join(techniques)}")


def example_manual_control():
    """Example 3: Manual control over each step"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Manual Control")
    print("="*60 + "\n")
    
    input_file = "myapp.exe"
    output_file = "myapp_manual.exe"
    
    obf = PEObfuscator(input_file, output_file)
    
    # Load and parse
    if not obf.load_file():
        print("[-] Failed to load file")
        return
    
    if not obf.parse_headers():
        print("[-] Failed to parse headers")
        return
    
    # Selectively apply techniques
    print("[*] Applying custom obfuscation pipeline...\n")
    
    obf.obfuscate_section_names()
    obf.modify_timestamps()
    obf.randomize_dos_stub()
    
    # Add extra junk multiple times
    for i in range(3):
        print(f"[*] Adding junk layer {i+1}...")
        obf.add_junk_sections()
    
    obf.modify_checksum()
    
    # Save
    obf.save_file()
    
    print(f"\n[+] Custom pipeline completed")


def example_batch_obfuscation():
    """Example 4: Batch obfuscate multiple files"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Batch Obfuscation")
    print("="*60 + "\n")
    
    # Find all .exe files in a directory
    input_dir = Path("./input_executables")
    output_dir = Path("./obfuscated_output")
    
    output_dir.mkdir(exist_ok=True)
    
    exe_files = list(input_dir.glob("*.exe"))
    
    if not exe_files:
        print("[!] No .exe files found in input directory")
        print(f"[!] Create directory: {input_dir}")
        return
    
    print(f"[*] Found {len(exe_files)} executable(s) to obfuscate\n")
    
    for exe_file in exe_files:
        print(f"[*] Processing: {exe_file.name}")
        
        output_file = output_dir / f"{exe_file.stem}_obfuscated{exe_file.suffix}"
        
        obf = PEObfuscator(str(exe_file), str(output_file))
        obf.obfuscate(['all'])
        
        print(f"[+] Saved to: {output_file}\n")
    
    print(f"[+] Batch obfuscation completed!")
    print(f"[+] Output directory: {output_dir.absolute()}")


def example_progressive_obfuscation():
    """Example 5: Progressive obfuscation layers"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Progressive Obfuscation")
    print("="*60 + "\n")
    
    input_file = "myapp.exe"
    
    # Apply obfuscation in layers
    layers = [
        (['sections', 'timestamp'], 'layer1'),
        (['dos-stub', 'checksum'], 'layer2'),
        (['junk', 'anti-debug'], 'layer3'),
        (['caves'], 'layer4'),
    ]
    
    current_input = input_file
    
    for techniques, layer_name in layers:
        output_file = f"myapp_{layer_name}.exe"
        
        print(f"[*] Applying {layer_name}: {', '.join(techniques)}")
        
        obf = PEObfuscator(current_input, output_file)
        obf.obfuscate(techniques)
        
        current_input = output_file
        print(f"[+] {layer_name} completed -> {output_file}\n")
    
    print(f"[+] Progressive obfuscation completed!")
    print(f"[+] Final output: {current_input}")


def example_analysis_comparison():
    """Example 6: Compare original vs obfuscated"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Analysis Comparison")
    print("="*60 + "\n")
    
    input_file = "myapp.exe"
    output_file = "myapp_obfuscated.exe"
    
    # Obfuscate
    obf = PEObfuscator(input_file, output_file)
    success = obf.obfuscate(['all'])
    
    if not success:
        print("[-] Obfuscation failed")
        return
    
    # Compare file sizes
    import os
    
    if os.path.exists(input_file) and os.path.exists(output_file):
        original_size = os.path.getsize(input_file)
        obfuscated_size = os.path.getsize(output_file)
        size_increase = obfuscated_size - original_size
        percentage = (size_increase / original_size) * 100
        
        print("\n[*] Size Comparison:")
        print(f"    Original:    {original_size:,} bytes")
        print(f"    Obfuscated:  {obfuscated_size:,} bytes")
        print(f"    Increase:    {size_increase:,} bytes ({percentage:.2f}%)")
        
        print("\n[*] Structure Comparison:")
        print(f"    Original sections:    {obf.number_of_sections}")
        print(f"    Modified sections:    {obf.number_of_sections}")
        print(f"    Architecture:         {'64-bit' if obf.is_64bit else '32-bit'}")


def print_menu():
    """Print example menu"""
    print("\n" + "="*60)
    print("PE OBFUSCATOR - USAGE EXAMPLES")
    print("="*60)
    print("\nAvailable examples:")
    print("  1. Basic obfuscation with all techniques")
    print("  2. Custom technique selection")
    print("  3. Manual control over obfuscation steps")
    print("  4. Batch obfuscate multiple files")
    print("  5. Progressive obfuscation layers")
    print("  6. Compare original vs obfuscated")
    print("\nNote: These are demonstration examples.")
    print("Replace 'myapp.exe' with your actual file path.")
    print("="*60 + "\n")


if __name__ == '__main__':
    print_menu()
    
    print("[*] To run a specific example, uncomment the function call below:\n")
    print("# example_basic_obfuscation()")
    print("# example_custom_techniques()")
    print("# example_manual_control()")
    print("# example_batch_obfuscation()")
    print("# example_progressive_obfuscation()")
    print("# example_analysis_comparison()")
    
    print("\n[*] Or run the test suite to see it in action:")
    print("    python test_obfuscator.py")

