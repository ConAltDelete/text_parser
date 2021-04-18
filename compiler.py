#Parser for turing

import sys

"""

A:
1 -> flip|card: B|move: right
0 -> 1   |card: A|move: right

out:
00000|00|00000|0|00|00000|0

"""

def pars_line(**arguments):
	s1_pars = pars_s1(arguments["line"][1][0],arguments["line"][0])
	bin_comp = s1_pars[1] + pars_s2(arguments["line"][1][1],arguments["alfabet"],arguments["line"][0]) + pars_s3(arguments["line"][1][2],arguments["line"][0])
	arguments["flags"]["card_args"].update({s1_pars[0]:bin_comp})

	if len(arguments["flags"]["card_args"]) > 2:
		raise SyntaxError("too many lines for card {}".format(arguments["flags"]["card"]))
	# den henter neste index før den gjør seg ferdig med denne.
	elif len(arguments["flags"]["card_args"]) == 2:
		arguments["cards"][arguments["flags"]["card"]] = "{:05b}".format( arguments["alfabet"][arguments["flags"]["card"]] )+arguments["flags"]["card_args"]["0"] + arguments["flags"]["card_args"]["1"]
		arguments["flags"]["card"] = None
		arguments["flags"]["card_args"] = dict()
	else:
		pass
	return arguments


def pars_s1(section,line):
	args = section.split("->")

	if len(args) > 2: raise ValueError("too many values in line {} section 1".format(line))

	bin_dic = {
		"0":"00",
		"1":"01",
		"T":"10",
		"X":"11"
	}

	args = [a.strip() for a in args]
	if args[0] not in bin_dic or args[1] not in bin_dic:
		raise ValueError("invalid value in line {} section 1, got {}".format(line,args[0] if args[0] not in bin_dic else args[1]))
	
	return args[0],bin_dic[args[1]]

def pars_s2(section,alfabet,line):
	args = section.split(":")
	if len(args) > 2: raise ValueError("too many arguments section 2 line {}".format(line))
	args = [a.strip() for a in args]

	if args[0] != "card": raise SyntaxError("Invalid syntax in section 2 line {}".format(line))

	if args[1] not in alfabet: raise SyntaxError("Invalid argument in section 2 line {}".format(line))



	return "{:05b}".format(alfabet[args[1]])

def pars_s3(section,line):
	args = section.split(":")
	if len(args) > 2: raise ValueError("too many arguments section 2 line {}".format(line))
	args = [a.strip() for a in args]

	if args[0] != "move": raise SyntaxError("Invalid syntax in section 2 line {}".format(line))

	if args[1] not in ["left","right"]: raise SyntaxError("Invalid argument in section 2 line {}, got {}".format(line,args[1]))

	return "1" if args[1] == "right" else "0"


if __name__ == "__main__":
	file_str:str = sys.argv[1]

	if not(file_str.endswith(".tur")):
		raise FileNotFoundError("Forventet '.tur' fil, fikk: {}".format(file_str.split(".")[-1]))
	else:
		file = open(file_str,"r")

	alfabet = dict(map( lambda x: (x[1],x[0]),enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ_",start=1)))

	cards = dict()

	flags = {
		"card":None,
		"card_args":dict(),
		"card_compile":False
	}

	for line in enumerate(file,start=1):
		line = list(line)
		line[1] = line[1].strip()
		if line[1] in ["","\n","#"]:
			continue
		if len(line) == 2 and line[1].endswith(":"):
			flags["card"] = line[1][:-1]
		else:
			line[1] = line[1].split("|")
			if len(line[1]) > 3:
				raise SyntaxError("For mange inndelinger på linje {}.".format(line[0]))
			elif len(line[1]) < 3:
				raise SyntaxError("For få inndelinger på linje {}.".format(line[0]))
			else:
				ret = pars_line(line=line,cards=cards,flags=flags,alfabet = alfabet)
	
	combined_bin = ""

	for card in ret["cards"]:
		combined_bin += ret["cards"][card]
	
	combined_bin += "0"*(len(combined_bin) % 8)

	fliped_bin = "".join(str(int(bool(int(a))^1)) for a in combined_bin)
	
	print(fliped_bin)


	print(combined_bin)

	byt:bytearray = bytearray([int(fliped_bin[i:i+8],base=2) for i in range(len(fliped_bin)//8+1)])

	exit_file = open(file_str[:-4] + ".bin","wb")

	exit_file.write(byt)

	exit_file.close()

