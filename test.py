import pyswip as ps

try:
    prolog = ps.Prolog()

    prolog.consult("knowledgebase.pl")
    list(prolog.query("initialize_start(5,1,5)."))
    print(list(prolog.query("home(R,C).")))
    print(True)
except Exception as e:
    print(f"Error consulting knowledge base: {e}")
