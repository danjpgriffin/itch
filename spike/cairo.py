import cairosvg

print(dir(cairosvg))

cairosvg.svg2png(url="/home/daneva/sandbox/pyscratch/fish.svg", write_to="/tmp/fish.png")