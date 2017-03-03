import cairosvg

print(dir(cairosvg))

cairosvg.svg2png(url="../resources/party.svg", write_to="../resources/party.png")