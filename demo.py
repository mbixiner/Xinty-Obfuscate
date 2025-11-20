#!/usr/bin/env python3
"""
Quick Demo Script for PE Obfuscator
Demonstrates the obfuscator's capabilities with a generated test file
"""

import sys
from pathlib import Path


def print_banner():
    """Print demo banner"""
    banner = """
    ============================================================
                                                                
              PE EXECUTABLE OBFUSCATOR DEMO                 
                                                                
      A comprehensive obfuscator for Windows PE (.exe) files    
                                                                
    ============================================================
    """
    print(banner)


def check_requirements():
    """Check if required files exist"""
    required_files = ['obfuscator.py', 'test_obfuscator.py']
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
    
    if missing:
        print(f"[-] Missing required files: {', '.join(missing)}")
        return False
    
    print("[+] All required files found")
    return True


def run_demo():
    """Run the complete demonstration"""
    print_banner()
    
    print("[*] Checking requirements...")
    if not check_requirements():
        sys.exit(1)
    
    print("\n" + "="*60)
    print("STEP 1: Creating Test PE Executable")
    print("="*60 + "\n")
    
    try:
        from test_obfuscator import create_minimal_pe_exe, analyze_pe_structure
        
        # Create test directory
        test_dir = Path("demo_output")
        test_dir.mkdir(exist_ok=True)
        
        # Create test executable
        test_exe = test_dir / "demo_sample.exe"
        create_minimal_pe_exe(str(test_exe))
        
        print("\n[+] Test executable created successfully!")
        
    except Exception as e:
        print(f"[-] Error creating test file: {e}")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("STEP 2: Analyzing Original PE Structure")
    print("="*60)
    
    analyze_pe_structure(str(test_exe))
    
    print("\n" + "="*60)
    print("STEP 3: Applying Obfuscation")
    print("="*60 + "\n")
    
    try:
        from obfuscator import PEObfuscator
        
        # Demonstrate different obfuscation levels
        demos = [
            {
                'name': 'Light Obfuscation',
                'output': test_dir / 'demo_light.exe',
                'techniques': ['sections', 'timestamp']
            },
            {
                'name': 'Medium Obfuscation',
                'output': test_dir / 'demo_medium.exe',
                'techniques': ['sections', 'timestamp', 'dos-stub', 'checksum']
            },
            {
                'name': 'Heavy Obfuscation',
                'output': test_dir / 'demo_heavy.exe',
                'techniques': ['all']
            }
        ]
        
        for demo in demos:
            print(f"\n[*] {demo['name']}")
            print(f"    Techniques: {', '.join(demo['techniques'])}")
            print()
            
            obf = PEObfuscator(str(test_exe), str(demo['output']))
            obf.obfuscate(demo['techniques'])
            
            print()
        
    except Exception as e:
        print(f"[-] Error during obfuscation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    print("\n" + "="*60)
    print("STEP 4: Comparing Results")
    print("="*60 + "\n")
    
    import os
    
    print("File Size Comparison:")
    print(f"{'File':<30} {'Size':>12} {'Change':>12}")
    print("-" * 60)
    
    original_size = os.path.getsize(str(test_exe))
    print(f"{'Original':<30} {original_size:>10} B {'-':>12}")
    
    for demo in demos:
        if demo['output'].exists():
            size = os.path.getsize(str(demo['output']))
            change = size - original_size
            change_pct = (change / original_size) * 100
            print(f"{demo['name']:<30} {size:>10} B {f'+{change} B ({change_pct:.1f}%)':>12}")
    
    print("\n" + "="*60)
    print("STEP 5: Analyzing Obfuscated Files")
    print("="*60)
    
    for demo in demos:
        if demo['output'].exists():
            print(f"\n[*] {demo['name']}:")
            analyze_pe_structure(str(demo['output']))
    
    print("\n" + "="*60)
    print("DEMO COMPLETED!")
    print("="*60 + "\n")
    
    print("[+] Demo files created in: " + str(test_dir.absolute()))
    print("\n[*] Files created:")
    for file in test_dir.glob("*.exe"):
        print(f"    - {file.name}")
    
    print("\n[*] Next steps:")
    print("    1. Inspect the obfuscated files with PE analysis tools")
    print("    2. Try obfuscating your own executables:")
    print("       python obfuscator.py your_program.exe")
    print("    3. Read QUICKSTART.md for more usage examples")
    print("    4. Check examples.py for code examples")
    
    print("\n[!] Remember:")
    print("    - Always test obfuscated executables before deployment")
    print("    - Only obfuscate files you have rights to modify")
    print("    - Use for legitimate software protection only")
    
    print("\n[+] Demo completed successfully!\n")


def show_help():
    """Show help information"""
    print("""
PE Obfuscator Demo Script

This script demonstrates the PE obfuscator by:
1. Creating a test PE executable
2. Analyzing its structure
3. Applying different levels of obfuscation
4. Comparing the results

Usage:
    python demo.py              Run the complete demo
    python demo.py --help       Show this help message

For more information:
    python obfuscator.py --help
    cat QUICKSTART.md
    cat README.md
    """)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        show_help()
    else:
        try:
            run_demo()
        except KeyboardInterrupt:
            print("\n\n[-] Demo interrupted by user")
            sys.exit(1)
        except Exception as e:
            print(f"\n[-] Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

