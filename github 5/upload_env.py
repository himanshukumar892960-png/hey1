import os
import subprocess

def upload_env():
    if not os.path.exists('.env'):
        print("Error: .env file not found!")
        return

    print("Reading .env file and uploading variables to Vercel...")
    
    with open('.env', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    count = 0
    for line in lines:
        line = line.strip()
        # Skip comments and empty lines
        if not line or line.startswith('#'):
            continue
        
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            
            if not key or not value:
                continue
                
            print(f"Uploading {key}...")
            # Using --force to overwrite if already exists
            # venv env add [key] [environment]
            try:
                # Add to production, preview, and development
                process = subprocess.Popen(
                    ['vercel', 'env', 'add', key, 'production'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate(input=value)
                
                # Also add to development/preview if you want
                subprocess.run(['vercel', 'env', 'add', key, 'preview'], input=value, text=True, capture_output=True)
                subprocess.run(['vercel', 'env', 'add', key, 'development'], input=value, text=True, capture_output=True)
                
                count += 1
            except Exception as e:
                print(f"Failed to upload {key}: {e}")

    print(f"\nFinished! Uploaded {count} environment variables.")
    print("Now you can run 'vercel --prod' to deploy.")

if __name__ == "__main__":
    upload_env()
