"""Flask API"""
from pathlib import Path

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from analyzer import analyze_code
from optimizations import optimize
from language_detector import detect_language

BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / 'frontend'

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path='')
CORS(app)


@app.route('/', methods=['GET'])
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        print("\n" + "="*60)
        print("RECEIVED REQUEST")
        print("="*60)
        
        data = request.json
        print(f"Request data: {data}")
        
        code = data.get('code', '')
        language = data.get('language', 'java')
        
        print(f"Language from request: {language}")
        print(f"Code length: {len(code)}")
        print(f"Code preview: {code[:100]}")
        
        if not code:
            print("ERROR: No code provided")
            return jsonify({'success': False, 'error': 'No code provided'}), 400
        
        # Analyze
        print(f"\nCalling analyze_code()...")
        issues = analyze_code(code)
        print(f"Issues found: {len(issues)}")
        print(f"Issues: {issues}")
        
        # Optimize
        print(f"\nCalling optimize()...")
        optimized, stats = optimize(code)
        print(f"Optimization stats: {stats}")
        
        # Calculate stats
        orig_lines = len([l for l in code.split('\n') if l.strip()])
        opt_lines = len([l for l in optimized.split('\n') if l.strip()])
        
        # Use defensive stat access because optimization modules may expose
        # different metric keys over time.
        response = {
            'success': True,
            'issues': issues,
            'statistics': {
                'original_lines': orig_lines,
                'optimized_lines': opt_lines,
                'lines_saved': orig_lines - opt_lines,
                'constant_folding': stats.get('constant_folding', 0),
                'dead_code': stats.get('dead_code', 0),
                'redundant_assignment': stats.get('redundant_assignment', 0),
                'expression_simplify': stats.get('expression_simplify', 0),
                'unused_variables': stats.get('unused_variables', 0),
                'loop_invariant': stats.get('loop_invariant', 0),
                'unnecessary_variables': stats.get('unnecessary_variables', 0),
                'inefficient_loops': stats.get('inefficient_loops', 0),
                'total_optimizations': sum(v for v in stats.values() if isinstance(v, (int, float)))
            }
        }
        
        print(f"\nResponse: {response}")
        print("="*60 + "\n")
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)