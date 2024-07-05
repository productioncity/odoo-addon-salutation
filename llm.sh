#!/usr/bin/env zsh

# Base directories and specific files to include
INCLUDE_DIRS=("salutation" ".devcontainer" ".github")
INCLUDE_FILES=("README.md" "get-enterprise.sh")

# Output markdown file
OUTPUT_FILE="llm.md"

# Create or clear the output file
echo "# Files" > "${OUTPUT_FILE}"

# Function to check if a file is binary
is_binary() {
  local file_path="$1"
  # Use file command if available, otherwise use fallback method
  if command -v file &> /dev/null; then
    file "$file_path" | grep -q 'charset=binary'
  else
    # Fallback method to detect binary files
    if grep -qIL . "$file_path"; then
      return 1
    else
      return 0
    fi
  fi
}

# Function to process each file
process_file() {
  local file_path="$1"
  local file_extension="${file_path##*.}"

  echo "\n## ${file_path}\n" >> "${OUTPUT_FILE}"
  
  if is_binary "$file_path"; then
    echo "*This file is binary and its content is not included.*" >> "${OUTPUT_FILE}"
    return
  fi

  echo "\`\`\`${file_extension}" >> "${OUTPUT_FILE}"

  # Add the content of the file and ensure there is a trailing newline
  awk '{print} END {if (NR > 0 && substr($0, length($0), 1) != "\n") print ""}' "$file_path" >> "${OUTPUT_FILE}"
  echo "\`\`\`\n" >> "${OUTPUT_FILE}"
}

# Process each directory
for dir in "${INCLUDE_DIRS[@]}"; do
  find "$dir" -type f ! -path "*/__pycache__/*" | while read -r file; do
    process_file "$file"
  done
done

# Process each specific file
for file in "${INCLUDE_FILES[@]}"; do
  if [[ -f "$file" ]]; then
    process_file "$file"
  fi
done

echo "LLM prompt file has been generated at ${OUTPUT_FILE}"
