#!/bin/bash

# CampusEats Rebranding Script
# This script performs comprehensive find-and-replace across the codebase

echo "===== CampusEats Rebranding Script ====="
echo "Starting comprehensive rebranding from 'CampusEats' to 'CampusEats'..."
echo ""

# Counter for tracking changes
TOTAL_FILES=0

# Function to perform replacement in a file
replace_in_file() {
    local file="$1"
    local has_changes=0

    # Skip node_modules, .git, __pycache__, dist, build directories
    if [[ "$file" == *"/node_modules/"* ]] || [[ "$file" == *"/.git/"* ]] || \
       [[ "$file" == *"/__pycache__/"* ]] || [[ "$file" == *"/dist/"* ]] || \
       [[ "$file" == *"/build/"* ]]; then
        return
    fi

    # Check if file contains any NTU references
    if grep -q "CampusEats\|CampusEats\|campuseats\|campuseats\|CampusEats\|ntu\.edu\.sg\|campus eateries\|university students\|Nanyang Technological University" "$file" 2>/dev/null; then
        echo "Processing: $file"

        # Create backup
        cp "$file" "$file.bak"

        # Perform all replacements
        sed -i '' 's/CampusEats/CampusEats/g' "$file"
        sed -i '' 's/CampusEats/CampusEats/g' "$file"
        sed -i '' 's/campuseats/campuseats/g' "$file"
        sed -i '' 's/campuseats/campuseats/g' "$file"
        sed -i '' 's/CampusEats/CampusEats/g' "$file"
        sed -i '' 's/campus eateries/campus eateries/g' "$file"
        sed -i '' 's/university students/university students/g' "$file"
        sed -i '' 's/university students/university students/g' "$file"
        sed -i '' 's/university students/university students/g' "$file"
        sed -i '' 's/@ntu\.edu\.sg/@campuseats.com/g' "$file"
        sed -i '' 's/@e\.ntu\.edu\.sg/@campuseats.com/g' "$file"

        # Remove backup if successful
        rm "$file.bak"

        ((TOTAL_FILES++))
    fi
}

# Export function so it can be used by find
export -f replace_in_file
export TOTAL_FILES

# Find and process all relevant files
echo "Searching for files to rebrand..."
echo ""

# Process Python files
find . -type f -name "*.py" ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/__pycache__/*" | while read -r file; do
    replace_in_file "$file"
done

# Process TypeScript/JavaScript files
find . -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \) ! -path "*/node_modules/*" ! -path "*/.git/*" | while read -r file; do
    replace_in_file "$file"
done

# Process Markdown files
find . -type f -name "*.md" ! -path "*/node_modules/*" ! -path "*/.git/*" | while read -r file; do
    replace_in_file "$file"
done

# Process HTML files
find . -type f -name "*.html" ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/dist/*" | while read -r file; do
    replace_in_file "$file"
done

# Process YAML files
find . -type f \( -name "*.yaml" -o -name "*.yml" \) ! -path "*/node_modules/*" ! -path "*/.git/*" | while read -r file; do
    replace_in_file "$file"
done

# Process shell scripts
find . -type f -name "*.sh" ! -path "*/node_modules/*" ! -path "*/.git/*" | while read -r file; do
    replace_in_file "$file"
done

# Process JSON files
find . -type f -name "*.json" ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/package-lock.json" | while read -r file; do
    replace_in_file "$file"
done

# Process .env.example files
find . -type f -name ".env.example" ! -path "*/node_modules/*" ! -path "*/.git/*" | while read -r file; do
    replace_in_file "$file"
done

# Process CSS files
find . -type f -name "*.css" ! -path "*/node_modules/*" ! -path "*/.git/*" | while read -r file; do
    replace_in_file "$file"
done

echo ""
echo "===== Rebranding Summary ====="
echo "Rebranding complete!"
echo ""
echo "Manual steps required:"
echo "1. Rename GitHub repository to 'campuseats'"
echo "2. Update deployment URLs (Vercel/Render) if needed"
echo "3. Update database connection strings if they contain 'ntu'"
echo "4. Test the application thoroughly"
echo ""
echo "Files to potentially rename:"
echo "  - backend/import_ntu_eateries.py → backend/import_campus_eateries.py"
echo "  - ntu_eateries_partial_list.csv → campus_eateries_list.csv"
echo ""
echo "===== DONE ====="
