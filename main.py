# main.py 
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import json
import subprocess

def main():
    # --- 1. Validate Command-Line Input ---
    if len(sys.argv) != 2:
        print("Usage: python main.py <path/to/your/config.json>")
        sys.exit(1)
    
    config_path = sys.argv[1]
    
    # Normalize the path
    config_path = os.path.normpath(config_path)
    
    if not os.path.exists(config_path):
        print(f"Error: Configuration file not found at '{config_path}'")
        sys.exit(1)

    # --- 2. Load Credentials ---
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        creds_path = os.path.join(script_dir, 'credentials.json')
        with open(creds_path, 'r', encoding='utf-8') as f:
            creds = json.load(f)
    except FileNotFoundError:
        print(f"Error: credentials.json not found in '{script_dir}'. Please create it.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in credentials.json: {e}")
        sys.exit(1)

    # --- 3. Set Environment Variables for the Sub-script ---
    os.environ['ALIYUN_ACCESS_KEY_ID'] = creds['accessKeyId']
    os.environ['ALIYUN_ACCESS_KEY_SECRET'] = creds['accessKeySecret']
    os.environ['ALIYUN_SECURITY_TOKEN'] = creds.get('securityToken', '')
    os.environ['DATAWORKS_PROJECT_ID'] = str(creds['projectId'])

    print("Credentials loaded. Starting node update process...")
    print("-" * 40)

    # --- 4. Execute the Update Script ---
    update_script_path = os.path.join(script_dir, 'update_nodes.py')
    result = subprocess.run(
        [sys.executable, update_script_path, config_path],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    print(result.stdout)
    if result.returncode != 0:
        print("\n--- ERROR ---")
        print(result.stderr)
        print("Node update failed.")
        sys.exit(1)

    print("-" * 40)
    print("Script execution finished successfully.")

if __name__ == "__main__":
    main()

