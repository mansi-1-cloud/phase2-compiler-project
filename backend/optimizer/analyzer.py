"""
Simple Code Analyzer
"""
import re

def analyze_code(code):
    """Find issues in code"""
    issues = []
    lines = code.split('\n')
    
    # ===== FIND UNUSED VARIABLES =====
    declared_vars = {}
    
    for i, line in enumerate(lines):
        match = re.search(r'\b(int|float|double|char|long|unsigned|bool)\s+(\w+)\s*=', line)
        if match:
            var_name = match.group(2)
            declared_vars[var_name] = i + 1
    
    used_vars = set()
    
    for i, line in enumerate(lines):
        for var_name in declared_vars.keys():
            if 'printf' in line and var_name in line:
                used_vars.add(var_name)
            elif 'return' in line and var_name in line:
                used_vars.add(var_name)
            elif var_name in line and 'return' not in line and 'printf' not in line:
                if not re.search(rf'^[^=]*{var_name}\s*=', line):
                    used_vars.add(var_name)
    
    for var_name, decl_line in declared_vars.items():
        if var_name not in used_vars:
            issues.append({
                'line': decl_line,
                'type': 'unused_variable',
                'issue': f'Variable "{var_name}" is declared but never used',
                'severity': 'warning'
            })
    
    # ===== CONSTANT FOLDING - Complex expressions =====
    for i, line in enumerate(lines, 1):
        # Match: 5 * 4 + 10 - 2, (2 * 3) + (4 * 5), (10 + 20) * 2
        if re.search(r'=\s*\(\d+\s*[+\-*/]\s*\d+\).*?[;]', line) or re.search(r'=\s*\d+\s*[+\-*/]\s*\d+\s*[+\-*/]', line):
            issues.append({
                'line': i,
                'type': 'constant_folding',
                'issue': 'Can fold constant expression',
                'severity': 'info'
            })
    
    # ===== REDUNDANT ASSIGNMENT - Detect consecutive assignments =====
    for i in range(len(lines) - 1):
        line1 = lines[i].strip()
        line2 = lines[i+1].strip()
        
        # Match: x = 5; followed by x = 5;
        match1 = re.match(r'^(\w+)\s*=\s*(.+?)\s*[;]', line1)
        match2 = re.match(r'^(\w+)\s*=\s*(.+?)\s*[;]', line2)
        
        if match1 and match2 and match1.group(1) == match2.group(1) and match1.group(2) == match2.group(2):
            issues.append({
                'line': i + 2,
                'type': 'redundant',
                'issue': f'Redundant assignment',
                'severity': 'warning'
            })
    
    # Also catch single line redundant: x = x;
    for i, line in enumerate(lines, 1):
        if re.search(r'^\s*(\w+)\s*=\s*\1\s*[;]', line.strip()):
            issues.append({
                'line': i,
                'type': 'redundant',
                'issue': f'Redundant assignment',
                'severity': 'warning'
            })
    
    # ===== DEAD CODE - if(false), if(0) =====
    for i, line in enumerate(lines, 1):
        if re.search(r'if\s*\(\s*(false|0)\s*\)', line):
            issues.append({
                'line': i,
                'type': 'dead_code',
                'issue': 'Dead code block (if(false) or if(0))',
                'severity': 'warning'
            })
    
    # ===== EXPRESSION SIMPLIFICATION =====
    for i, line in enumerate(lines, 1):
        # x * 1
        if re.search(r'(\w+)\s*\*\s*1\b', line) and '=' in line:
            issues.append({
                'line': i,
                'type': 'simplify',
                'issue': 'Can simplify: x * 1 → x',
                'severity': 'info'
            })
        # x + 0
        if re.search(r'(\w+)\s*\+\s*0\b', line) and '=' in line:
            issues.append({
                'line': i,
                'type': 'simplify',
                'issue': 'Can simplify: x + 0 → x',
                'severity': 'info'
            })
    
    return issues