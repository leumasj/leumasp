#!/usr/bin/env python3

with open('leumas/templates/leumas/index.html', 'r') as f:
    lines = f.readlines()

# Find lines with preview_blogs references and fix them
count = 0
for i, line in enumerate(lines):
    if 'preview_blogs.1.date' in line:
        count += 1
        if count == 2:  # Second occurrence should be .2
            lines[i] = line.replace('preview_blogs.1.date', 'preview_blogs.2.date')
        elif count == 3:  # Third occurrence should be .3
            lines[i] = line.replace('preview_blogs.1.date', 'preview_blogs.3.date')

with open('leumas/templates/leumas/index.html', 'w') as f:
    f.writelines(lines)

print("Fixed blog dates in template")
