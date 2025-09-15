# %%
import os

# List of desired filenames
filenames = ["op2.json", "op2.html", "op2.js",
             "op3.json", "op3.html", "op3.js",
             "op4.json", "op4.html", "op4.js",
             "op5.json", "op5.html", "op5.js",
            ]

# Get the current directory to show where files will be created
current_directory = os.getcwd()
print(f"Files will be created in: {current_directory}\n")

# Loop through the list and create each file
for filename in filenames:
    try:
        # 'w' mode creates a file if it doesn't exist
        with open(filename, 'w') as f:
            # The 'with' statement automatically handles closing the file.
            # We don't need to write anything, so we can just pass.
            pass
        print(f"✅ Created file: {filename}")
    except IOError as e:
        print(f"❌ Error creating file {filename}: {e}")

print("\nScript finished.")