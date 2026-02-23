#!/usr/bin/env python3

with open('leumas/templates/leumas/index.html', 'r') as f:
    content = f.read()

# Count occurrences to verify
count = content.count('By, {{ blog.author }}')
print(f"Found {count} instances of 'By, {{ blog.author }}'")

# Simple approach: replace all instances of {{ blog.author }} with specific preview_blogs references
# We need to do this carefully since there are 3 instances that need to be fixed

# Find and replace pattern by looking for context
changes = 0

# Replace for blog 1
old = 'By, {{ blog.author }}\n                                                    </p>\n                                                </li>\n                                            </ul>\n                                            <a href="{% url \'leumas:blog-detail\' 1 %}">'
new = 'By, {{ preview_blogs.1.author }}\n                                                    </p>\n                                                </li>\n                                            </ul>\n                                            <a href="{% url \'leumas:blog-detail\' 1 %}">'
if old in content:
    content = content.replace(old, new, 1)
    changes += 1
    print("✓ Fixed blog 1 author")

# Replace for blog 2
old = 'By, {{ blog.author }}\n                                                    </p>\n                                                </li>\n                                            </ul>\n                                            <a href="{% url \'leumas:blog-detail\' 2 %}">'
new = 'By, {{ preview_blogs.2.author }}\n                                                    </p>\n                                                </li>\n                                            </ul>\n                                            <a href="{% url \'leumas:blog-detail\' 2 %}">'
if old in content:
    content = content.replace(old, new, 1)
    changes += 1
    print("✓ Fixed blog 2 author")

# Replace for blog 3
old = 'By, {{ blog.author }}\n                                                    </p>\n                                                </li>\n                                            </ul>\n                                            <a href="{% url \'leumas:blog-detail\' 3 %}">'
new = 'By, {{ preview_blogs.3.author }}\n                                                    </p>\n                                                </li>\n                                            </ul>\n                                            <a href="{% url \'leumas:blog-detail\' 3 %}">'
if old in content:
    content = content.replace(old, new, 1)
    changes += 1
    print("✓ Fixed blog 3 author")

if changes == 0:
    print("Trying alternative approach...")
    # Try replacing just the variable references with more context
    lines = content.split('\n')
    new_lines = []
    for i, line in enumerate(lines):
        if 'By, {{ blog.author }}' in line:
            # Look at previous lines to determine which blog number this is
            context_lines = '\n'.join(lines[max(0, i-10):i])
            if 'blog-detail\' 1 %' in context_lines:
                line = line.replace('{{ blog.author }}', '{{ preview_blogs.1.author }}')
                print("✓ Fixed blog 1 author (alternative)")
            elif 'blog-detail\' 2 %' in context_lines:
                line = line.replace('{{ blog.author }}', '{{ preview_blogs.2.author }}')
                print("✓ Fixed blog 2 author (alternative)")
            elif 'blog-detail\' 3 %' in context_lines:
                line = line.replace('{{ blog.author }}', '{{ preview_blogs.3.author }}')
                print("✓ Fixed blog 3 author (alternative)")
        new_lines.append(line)
    content = '\n'.join(new_lines)

with open('leumas/templates/leumas/index.html', 'w') as f:
    f.write(content)

print(f"✓ Fixed blog author references in index.html ({changes} direct replacements made)")
