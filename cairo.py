import cairosvg

print(dir(cairosvg))

cairosvg.svg2png(url="/home/daneva/sandbox/pyscratch/cat.svg", write_to="/tmp/cat.png")