import compiler

test = "card: K"

alfabet = dict(map( lambda x: (x[1],x[0]),enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ_",start=1)))

print(compiler.pars_s2(test,line=6,alfabet=alfabet))
