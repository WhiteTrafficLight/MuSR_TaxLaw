"""
HTML rendering utilities for German tax case visualization.
"""

from typing import List

from src.logic_tree.tree import LogicTree


def render_node_html(node: dict, level: int = 0) -> str:
    """
    Recursively render a tree node as HTML.
    
    Args:
        node: Node dictionary from tree JSON
        level: Current depth level
        
    Returns:
        HTML string for this node and its children
    """
    value = node.get('value', '')
    
    # Skip nodes with empty values
    if not value or not value.strip():
        return ''
    
    # Determine CSS class based on level
    if level == 0:
        css_class = 'root-node'
    elif level == 1:
        css_class = 'child-node'
    elif level == 2:
        css_class = 'grandchild-node'
    else:
        css_class = 'great-grandchild-node'
    
    fact_type = node.get('fact_type', 'unknown')
    operator = node.get('operator', '')
    
    # Build badges
    fact_badge = f'<span class="fact-type {fact_type}">{fact_type}</span>' if fact_type != 'unknown' else ''
    operator_badge = f'<span class="operator-info">{operator}</span>' if operator else ''
    
    # Build HTML
    html = f'<div class="tree-node {css_class}">{fact_badge}{value}{operator_badge}</div>'
    
    # Recursively render children
    for child in node.get('children', []):
        child_html = render_node_html(child, level + 1)
        if child_html:  # Only add non-empty children
            html += child_html
    
    return html


def generate_html_page(tree: LogicTree, story_text: str, choices: List[str]) -> str:
    """
    Generate a complete HTML page with tree, story, and question.
    
    Args:
        tree: The logic tree to render
        story_text: Generated story text
        choices: List of choice strings (e.g., ["A) ...", "B) ...", "C) ..."])
        
    Returns:
        Complete HTML string
    """
    tree_id = 'tree_single'
    tree_json = tree.to_json()
    
    html_parts: List[str] = []
    
    # HTML header
    html_parts.append('''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Single German Tax Case (Tree + Story)</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
    .section { border: 2px solid #333; margin: 20px 0; padding: 20px; border-radius: 8px; }
    .tree { background: #ffffff; padding: 15px; margin: 10px 0; border-radius: 5px; border: 1px solid #dee2e6; }
    .tree-node { margin: 8px 0; padding: 8px; border-radius: 4px; position: relative; }
    .root-node { border-left: 6px solid #dc3545; font-weight: bold; background: #f8d7da; font-size: 1.2em; margin-bottom: 15px; }
    .child-node { margin-left: 25px; border-left: 4px solid #28a745; background: #d4edda; padding-left: 15px; margin-bottom: 10px; }
    .grandchild-node { margin-left: 50px; border-left: 3px solid #007acc; background: #cce7ff; padding-left: 12px; margin-bottom: 8px; }
    .great-grandchild-node { margin-left: 75px; border-left: 2px solid #6c757d; background: #f8f9fa; padding-left: 10px; margin-bottom: 5px; }
    .fact-type { display: inline-block; color: white; padding: 3px 8px; border-radius: 4px; font-size: 0.8em; margin-right: 10px; font-weight: bold; }
    .explicit { background: #28a745; }
    .commonsense { background: #ffc107; color: #212529; }
    .toggle-btn { background: #007acc; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer; margin: 5px 0 15px 0; font-size: 14px; font-weight: bold; }
    .hidden { display: none; }
    .operator-info { display: inline-block; background: #6c757d; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.7em; margin-left: 10px; }
    .question { background: #fff3cd; padding: 15px; border-radius: 5px; }
    .choice { margin: 4px 0; }
    .correct { font-weight: bold; color: #0a7e07; }
  </style>
  <script>
    function toggleTree(id) {
      var el = document.getElementById(id);
      var btn = document.querySelector('[onclick="toggleTree(\\'' + id + '\\')"]');
      if (el.classList.contains('hidden')) {
        el.classList.remove('hidden');
        if (btn) btn.textContent = '🔼 Hide Tree';
      } else {
        el.classList.add('hidden');
        if (btn) btn.textContent = '🔽 Show Tree';
      }
    }
  </script>
</head>
<body>
  <h1>🏛️ Single German Tax Case (Reasoning Tree + Story)</h1>
''')

    # Tree section
    html_parts.append('<div class="section">')
    html_parts.append('<h2>🌳 Reasoning Tree</h2>')
    html_parts.append(f'<button class="toggle-btn" onclick="toggleTree(\'{tree_id}\')">🔽 Show Tree</button>')
    html_parts.append(f'<div class="tree hidden" id="{tree_id}">')
    
    roots = tree_json.get('root_structure', [])
    if roots:
        for root in roots:
            html_parts.append(render_node_html(root))
    else:
        html_parts.append('<p>❌ No tree structure found</p>')
    
    html_parts.append('</div>')
    html_parts.append('</div>')

    # Story section
    html_parts.append('<div class="section">')
    html_parts.append('<h2>📖 Story</h2>')
    html_parts.append(f'<div class="story"><p>{story_text}</p></div>')
    html_parts.append('</div>')

    # Question section
    html_parts.append('<div class="section">')
    html_parts.append('<h2>❓ Question</h2>')
    html_parts.append('<div class="question">')
    
    for i, choice in enumerate(choices):
        css_class = 'choice correct' if i == 0 else 'choice'
        mark = '✅' if i == 0 else '❌'
        html_parts.append(f'<div class="{css_class}">{choice} {mark}</div>')
    
    html_parts.append('</div>')
    html_parts.append('</div>')

    html_parts.append('</body></html>')

    return ''.join(html_parts)


def generate_html_page_comparison(case_data: list, stories: list, labeled: list, business_sector: str, tx_type: str) -> str:
    """
    Generate HTML page for two-case comparison.
    
    Args:
        case_data: List of 2 case dictionaries with trees
        stories: List of 2 story texts
        labeled: Choices list
        business_sector: Business sector
        tx_type: Transaction type
        
    Returns:
        HTML string
    """
    html_parts = ['''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>German Tax Case Comparison</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; line-height: 1.6; }
    .section { border: 2px solid #333; margin: 20px 0; padding: 20px; border-radius: 8px; }
    .case-container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    .case { border: 1px solid #666; padding: 15px; border-radius: 5px; }
    .tree { background: #ffffff; padding: 15px; margin: 10px 0; border-radius: 5px; border: 1px solid #dee2e6; }
    .tree-node { margin: 8px 0; padding: 8px; border-radius: 4px; position: relative; }
    .root-node { border-left: 6px solid #dc3545; font-weight: bold; background: #f8d7da; font-size: 1.1em; margin-bottom: 15px; }
    .child-node { margin-left: 25px; border-left: 4px solid #28a745; background: #d4edda; padding-left: 15px; margin-bottom: 10px; }
    .grandchild-node { margin-left: 50px; border-left: 3px solid #007acc; background: #cce7ff; padding-left: 12px; margin-bottom: 8px; }
    .great-grandchild-node { margin-left: 75px; border-left: 2px solid #6c757d; background: #f8f9fa; padding-left: 10px; margin-bottom: 5px; }
    .fact-type { display: inline-block; color: white; padding: 3px 8px; border-radius: 4px; font-size: 0.8em; margin-right: 10px; font-weight: bold; }
    .explicit { background: #28a745; }
    .commonsense { background: #ffc107; color: #212529; }
    .toggle-btn { background: #007acc; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer; margin: 5px 0 15px 0; font-size: 14px; font-weight: bold; }
    .hidden { display: none; }
    .operator-info { display: inline-block; background: #6c757d; color: white; padding: 2px 6px; border-radius: 3px; font-size: 0.7em; margin-left: 10px; }
    .question { background: #fff3cd; padding: 15px; border-radius: 5px; }
    .choice { margin: 4px 0; }
    .correct { font-weight: bold; color: #0a7e07; }
    .metadata { background: #e7f3ff; padding: 10px; border-radius: 5px; margin-bottom: 10px; font-size: 0.9em; }
  </style>
  <script>
    function toggleTree(id) {
      var el = document.getElementById(id);
      var btn = document.querySelector('[onclick="toggleTree(\\'' + id + '\\')"]');
      if (el.classList.contains('hidden')) {
        el.classList.remove('hidden');
        if (btn) btn.textContent = '🔼 Hide Tree';
      } else {
        el.classList.add('hidden');
        if (btn) btn.textContent = '🔽 Show Tree';
      }
    }
  </script>
</head>
<body>
  <h1>🏛️ German Tax Case Comparison</h1>
  <div class="metadata">
    <strong>Business Sector:</strong> {business_sector}<br>
    <strong>Transaction Type:</strong> {tx_type}
  </div>
''']
    
    # Add both cases side by side
    html_parts.append('<div class="case-container">')
    
    for idx, (data, story) in enumerate(zip(case_data, stories)):
        case_num = idx + 1
        tree = data['correct_tree']
        case_info = data['case_info']
        
        html_parts.append(f'<div class="case">')
        html_parts.append(f'<h2>Case {case_num}</h2>')
        html_parts.append(f'<div class="metadata">')
        html_parts.append(f'<strong>Taxpayer:</strong> {case_info["taxpayer"]}<br>')
        html_parts.append(f'<strong>Tax Authority:</strong> {case_info["tax_authority"]}<br>')
        html_parts.append(f'<strong>Decision:</strong> {case_info["final_decision"]}')
        html_parts.append(f'</div>')
        
        # Tree
        html_parts.append(f'<h3>🌳 Reasoning Tree</h3>')
        html_parts.append(f'<button class="toggle-btn" onclick="toggleTree(\'tree_{case_num}\')">🔽 Show Tree</button>')
        html_parts.append(f'<div class="tree hidden" id="tree_{case_num}">')
        
        tree_json = tree.to_json()
        for root in tree_json['nodes']:
            html_parts.append(render_node_html(root))
        
        html_parts.append('</div>')
        
        # Story
        html_parts.append(f'<h3>📖 Story</h3>')
        html_parts.append(f'<div class="story"><p>{story}</p></div>')
        html_parts.append('</div>')
    
    html_parts.append('</div>')  # End case-container
    
    # Question
    html_parts.append('<div class="section">')
    html_parts.append('<h2>❓ Question</h2>')
    html_parts.append('<div class="question">')
    
    for i, choice in enumerate(labeled):
        css_class = 'choice correct' if i == 0 else 'choice'
        mark = '✅' if i == 0 else '❌'
        html_parts.append(f'<div class="{css_class}">{choice} {mark}</div>')
    
    html_parts.append('</div>')
    html_parts.append('</div>')
    
    html_parts.append('</body></html>')
    
    return ''.join(html_parts)

