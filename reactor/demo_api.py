#!/usr/bin/env python3
"""
Demo script showing how to access the Reactor 3D Visualization API
"""

import requests
import json
import sys

def get_model_info(base_url="http://localhost:5001"):
    """Get model information from the API"""
    try:
        response = requests.get(f"{base_url}/api/model-info")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to server: {e}")
        return None

def print_model_info(info):
    """Pretty print model information"""
    print("=== Reactor Model Information ===")
    
    # GLTF Info
    gltf_info = info.get('gltf_info', {})
    print(f"\nGLTF Model Stats:")
    print(f"  Total Nodes: {gltf_info.get('total_nodes', 'N/A')}")
    print(f"  Total Meshes: {gltf_info.get('total_meshes', 'N/A')}")
    print(f"  Total Materials: {gltf_info.get('total_materials', 'N/A')}")
    print(f"  Total Buffers: {gltf_info.get('total_buffers', 'N/A')}")
    
    # Node Information
    nodes = gltf_info.get('nodes', [])
    print(f"\nModel Components ({len(nodes)} nodes):")
    for node in nodes:
        mesh_indicator = "📦" if node.get('has_mesh') else "📁"
        children_indicator = f" (+{len(node.get('children', []))} children)" if node.get('has_children') else ""
        print(f"  {mesh_indicator} {node['name']}{children_indicator}")
    
    # File Mapping
    mapping = info.get('mapping', [])
    print(f"\nFile Mapping ({len(mapping)} entries):")
    for item in mapping:
        stl_name = item['stl'].split('/')[-1]  # Just filename
        bin_name = item['bin'].split('/')[-1]  # Just filename
        print(f"  {stl_name} → {bin_name}")
    
    print(f"\nModel File: {info.get('model_file', 'N/A')}")
    print("================================")

def main():
    """Main demo function"""
    base_url = "http://localhost:5001"
    
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    
    print(f"Connecting to Reactor 3D Visualization API at: {base_url}")
    print("Make sure the Flask server is running first!")
    print()
    
    info = get_model_info(base_url)
    
    if info:
        if 'error' in info:
            print(f"API Error: {info['error']}")
        else:
            print_model_info(info)
    else:
        print("Failed to retrieve model information.")
        print("Make sure the server is running with: python app.py")

if __name__ == "__main__":
    main()