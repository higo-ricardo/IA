import re

for filename in ['VerbetesSTJ.md', 'VerbetesSTF.md']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    all_nums = re.findall(r'Súmula (\d+)', content)
    sections = re.split(r'(?=^## )', content, flags=re.MULTILINE)
    section_nums = []
    for sec in sections[1:]:
        section_nums.extend(re.findall(r'Súmula (\d+)', sec))
    
    status = "OK" if len(all_nums) == len(section_nums) else "ERRO"
    print(f"{filename}: total={len(all_nums)} em_secoes={len(section_nums)} -> {status}")
