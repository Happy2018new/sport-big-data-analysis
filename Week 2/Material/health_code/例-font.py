import matplotlib.font_manager as fm

font_name = sorted(set([f.name for f in fm.fontManager.ttflist]))
for name in font_name:
    print(name)
