"""
Simple Code Analyzer
"""
import re

def analyze_code(code):
    """Find issues in code"""
    issues = []
    lines = code.split('\n')
    
    print("\n" + "="*60)
    print("ANALYZING CODE")
    print("="*60)
    
    # ===== FIND UNUSED VARIABLES =====
    declared_vars = {}
    
    for i, line in enumerate(lines):
        # Match: int x = 10;  or  float y = 3.14;
        match = re.search(r'\b(int|float|double|char|long|unsigned|bool)\s+(\w+)\s*=', line)
        if match:
            var_name = match.group(2)
            declared_vars[var_name] = i + 1
            print(f"Found variable: {var_name} at line {i+1}")
    
    print(f"Total variables declared: {len(declared_vars)}")
    
    # Check which variables are USED (appear in printf, return, etc)
    used_vars = set()
    
    for i, line in enumerate(lines):
        for var_name in declared_vars.keys():
            # Check if variable is used in printf
            if 'printf' in line and var_name in line:
                used_vars.add(var_name)
                print(f"Variable '{var_name}' USED in printf at line {i+1}")
            # Check if variable is used in return
            elif 'return' in line and var_name in line:
                used_vars.add(var_name)
                print(f"Variable '{var_name}' USED in return at line {i+1}")
            # Check if variable is used in any other way
            elif var_name in line and 'return' not in line and 'printf' not in line:
                # Make sure it's not just being assigned
                if not re.search(rf'^[^=]*{var_name}\s*=', line):
                    used_vars.add(var_name)
                    print(f"Variable '{var_name}' USED in calculation at line {i+1}")
    
    print(f"Used variables: {used_vars}")
    
    # Report unused variables
    for var_name, decl_line in declared_vars.items():
        if var_name not in used_vars:
            print(f"REPORTING: {var_name} as UNUSED")
            issues.append({
                'line': decl_line,
                'type': 'unused_variable',
                'issue': f'Variable "{var_name}" is declared but never used',
                'severity': 'warning'
            })
    
    # ===== CONSTANT FOLDING =====
    for i, line in enumerate(lines, 1):
        if re.search(r'=\s*\d+\s*[+\-*/]\s*\d+\s*;', line):
            print(f"Constant folding found at line {i}")
            issues.append({
                'line': i,
                'type': 'constant_folding',
                'issue': 'Can fold constant expression (e.g., 2 + 3 → 5)',
                'severity': 'info'
            })
    
    # ===== REDUNDANT ASSIGNMENT =====
    for i, line in enumerate(lines, 1):
        if re.search(r'^\s*(\w+)\s*=\s*\1\s*;\s*$', line.strip()):
            print(f"Redundant assignment found at line {i}")
            issues.append({
                'line': i,
                'type': 'redundant',
                'issue': f'Redundant assignment',
                'severity': 'warning'
            })
    
    # ===== SIMPLE EXPRESSIONS =====
    for i, line in enumerate(lines, 1):
        if re.search(r'(\w+)\s*=\s*\1\s*\+\s*0\s*;', line):
            print(f"Simple expression found at line {i}")
            issues.append({
                'line': i,
                'type': 'simplify',
                'issue': 'Can simplify: x = x + 0 → x',
                'severity': 'info'
            })
        if re.search(r'(\w+)\s*=\s*\1\s*\*\s*1\s*;', line):
            print(f"Simple expression found at line {i}")
            issues.append({
                'line': i,
                'type': 'simplify',
                'issue': 'Can simplify: x = x * 1 → x',
                'severity': 'info'
            })
    
    # ===== DEAD CODE =====
    for i, line in enumerate(lines, 1):
        if 'return' in line and not line.strip().startswith('//'):
            for j in range(i, len(lines)):
                next_line = lines[j].strip()
                if next_line and next_line != '}' and not next_line.startswith('//'):
                    print(f"Dead code found at line {j+1}")
                    issues.append({
                        'line': j + 1,
                        'type': 'dead_code',
                        'issue': 'Unreachable code after return',
                        'severity': 'error'
                    })
                    break
                if next_line == '}':
                    break
    
    print(f"Total issues found: {len(issues)}")
    print("="*60 + "\n")
    
    return issues