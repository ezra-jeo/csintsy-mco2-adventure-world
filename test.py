import pyswip as ps

try:
    prolog = ps.Prolog()

    prolog.consult("knowledgebase.pl")
    list(prolog.query("initialize_start(5,1,5)."))
    list(prolog.query("assert_fact(coins(2))."))

    print(list(prolog.query("coins(A).")))

    # for fact in list(prolog.query("unexplored_safe(R,C).")):
    #     print(dict(fact)["R"], dict(fact)["C"])  
except Exception as e:
    print(f"Error consulting knowledge base: {e}")
