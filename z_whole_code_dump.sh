{
  echo "===== PROJECT TREE ====="
  tree -a -I "__pycache__|.git|output|node_modules|.next"
  echo -e "\n===== FILE DUMP ====="
  find . \( -name "*.py" -o -name "*.csv" -o -name "Pipfile" -o -name "*.md" \) -type f \
    ! -name "Pipfile.lock" \
    ! -path "*/node_modules/*" \
    ! -path "*/.next/*" \
    | sort \
    | while read -r file; do
        echo "===== FILE: $file ====="
        cat "$file"
        echo -e "\n"
      done
} > zz_whole_code_dump.txt