import pyswip as ps


class Agent:
    def __init__(self, map, start_pos, n):
        self.map = map
        self.start_pos = start_pos
        self.N = n

        # Values to be displayed in the map

        self.map.unexplored_safe = set()
        self.map.explored_safe = set()
        self.map.unknown = set()
        self.map.pit = set()
        
        self.prolog = ps.Prolog()

        try:
            
            R, C = self.start_pos
            self.prolog.consult("knowledgebase.pl")
            list(self.prolog.query(f"initialize_start({R},{C},{self.N})."))

            print("Initialized.")
        except Exception as e:
            print(f"Error consulting knowledge base: {e}")

    def query_move(self, player_pos):
        try:
            R, C = player_pos
            tile_type = self.map.get_tile_type(R,C)
            
            if tile_type == "safe":
                if player_pos in self.map.breeze_pos:
                    list(self.prolog.query(f"move({R}, {C}, [breeze], {self.N})."))
                else:
                    list(self.prolog.query(f"move({R}, {C}, [{tile_type}], {self.N})."))
            else:
                if tile_type != "pit":
                    if player_pos in self.map.breeze_pos:
                        list(self.prolog.query(f"move({R}, {C}, [breeze, {tile_type}], {self.N})."))
                    else:
                        list(self.prolog.query(f"move({R}, {C}, [{tile_type}], {self.N})."))
                
            self.__get_updated_values()

        except Exception as e:
            print(f"Error consulting knowledge base: {e}")

    def __get_updated_values(self): # helper method
        # Ask
        # self.unexplored_safe = set()
        # self.explored_safe = set()
        # self.unknown = set()
        self.map.unexplored_safe = set()
        self.map.explored_safe = set()
        self.map.unknown = set()
        self.map.pit = set()


        try:
            us_buffer = list(self.prolog.query(f"unexplored_safe(R,C)."))

            for fact in us_buffer:
                self.map.unexplored_safe.add((dict(fact)["R"], dict(fact)["C"]))
            
            s_buffer = list(self.prolog.query(f"explored_safe(R,C)."))

            for fact in s_buffer:
                self.map.explored_safe.add((dict(fact)["R"], dict(fact)["C"]))

            u_buffer = list(self.prolog.query(f"unknown(R,C)."))

            for fact in u_buffer:
                self.map.unknown.add((dict(fact)["R"], dict(fact)["C"]))

            p_buffer = list(self.prolog.query(f"pit(R,C)."))
            for fact in p_buffer:
                self.map.pit.add((dict(fact)["R"], dict(fact)["C"]))
        
        
        except Exception as e:
            print(f"Error consulting knowledge base: {e}")


    def get_gold_count(self):
        try:
            coins = list(self.prolog.query("coins(N)."))
            if not coins:
                return 0
            return coins[0]["N"]
            
        except Exception as e:
            print(f"Error consulting knowledge base: {e}")

    def is_home(self, pos):
        return pos == self.start_pos
    
    def check_win(self, player_pos, escape):
        tile_type = self.map.get_tile_type(*player_pos)

        if tile_type == "pit":
            return "lose"
        elif self.is_home(player_pos) and self.get_gold_count() < 2 and escape:
            return "lose"
        elif self.is_home(player_pos) and self.get_gold_count() >= 2 and escape:
            return "win"




        
        



   



    
