
def writeOutput(result, path="output.txt"):
	output = ""
	if result == "PASS":
		output = "PASS"
	else:
		output += str(result[0]) + ',' + str(result[1])

	with open(path, 'w') as file:
		file.write(output)

# def writePass(path="output.txt"):
# 	with open(path, 'w') as f:
# 		f.write("PASS")

def writeNextInput(piece_type, previous_board, board, path="input.txt"):
	output = ""
	output += str(piece_type) + "\n"
	for item in previous_board:
		output += "".join([str(x) for x in item])
		output += "\n"

	for item in board:
		output += "".join([str(x) for x in item])
		output += "\n"

	with open(path, 'w') as file:
		file.write(output[:-1]);
