% Implements a dynamic knowledge base.
:- dynamic breeze/2.
% :- dynamic glitter/2.
:- dynamic pit/2.
:- dynamic gold/2.
:- dynamic unexplored_safe/2.
:- dynamic explored_safe/2.
:- dynamic home/2.
:- dynamic unknown/2.
:- dynamic coins/1. 

% Adds non-existing fact to the knowledge base.
assert_fact(N) :-
    not(N),
    assertz(N).

% Validates if the given tile location is within the grid.
in_bounds(R,C,N) :-
    (R >= 1, R =< N),
    (C >= 1, C =< N).

% Validates if the given tile locations are neighboring or adjacent.
neighbor(R,C,NR,NC,N) :-
    ((NR is R + 1, NC is C);
    (NR is R - 1, NC is C);
    (NR is R, NC is C + 1);
    (NR is R, NC is C - 1)),
    in_bounds(NR,NC,N).

% Initializes the starting tile of player and home and status of neighboring tiles.
initialize_start(R,C,N) :-
    assert_fact(home(R,C)),
    assert_fact(explored_safe(R,C)),
    forall(neighbor(R,C,NR,NC,N), assert_fact(unexplored_safe(NR,NC))).

% Infers the given tile is unexplored safe with the respect to the constraints.
is_unexplored_safe(R,C) :-
    (\+ breeze(R,C),
    \+ pit(R,C),
    \+ gold(R,C),
    \+ explored_safe(R,C),
    \+ home(R,C),
    assert_fact(unexplored_safe(R,C)),
    (unknown(R,C) -> retract(unknown(R,C)); true)); true.

% Infers the given tile is unknown with the respect to the constraints.
is_unknown(R,C) :-
    (\+ breeze(R,C),
    \+ pit(R,C),
    \+ gold(R,C),
    \+ unexplored_safe(R,C),
    \+ explored_safe(R,C),
    \+ home(R,C),
    \+ unknown(R,C),
    assert_fact(unknown(R,C))); true.

% Validates if the given tile can be inferred as a gold.
% is_gold(R,C,N) :-
%     (forall(
%         neighbor(R,C,NR,NC,N),
%         glitter(NR,NC)),
%         assert_fact(gold(R,C)),
%         retract(unknown(R,C));
%     true).
%            (
%             glitter(NR,NC),
%             forall(
%                 neighbor(NR,NC,NNR,NNC,N),
%                  (
%                     explored_safe(NNR, NNC); 
%                     unexplored_safe(NNR,NNC)
%                 )
%             )
%         )
%     ), 
%     assert_fact(gold(R,C)), 
%     retract(unknown(R,C)); 
% true).
    
% Validates if the given tile can be inferred as a pit.
is_pit(R,C,N) :-
    (forall(
        neighbor(R,C,NR,NC,N),
        breeze(NR,NC)),
        assert_fact(pit(R,C)),
        retract(unknown(R,C));
    true).

is_pit_2(R,C,N) :-
    findall((NR,NC),
            (neighbor(R,C,NR,NC,N), (unknown(NR,NC); \+pit(NR,NC))),
            PP),
    length(PP,1) -> ([Pit] = PP,
                     Pit = (NR,NC),
                     assert_fact(pit(NR,NC)),
                     retract(unknown(NR,NC))
                    ); true.

% Updates knowledge base from the move of the player and tile status.
move(R,C,S,N) :-
    (member(safe,S) -> ((unexplored_safe(R,C); unknown(R,C)) -> (retract(unexplored_safe(R,C)); retract(unknown(R,C))),
                                                                assert_fact(explored_safe(R,C)), 
                                                                forall(neighbor(R,C,NR,NC,N), 
                                                                        is_unexplored_safe(NR,NC)); 
                                                                true); 
                    true),                   
    (member(breeze,S) -> ((unexplored_safe(R,C); unknown(R,C)) -> ((member(gold,S) -> true); (retract(unexplored_safe(R,C)); retract(unknown(R,C))), assert_fact(explored_safe(R,C))),
                                                                   assert_fact(breeze(R,C)),
                                                                   forall(neighbor(R,C,NR,NC,N), 
                                                                          is_unknown(NR,NC)),
                                                                    is_pit_2(R,C,N);
                                                                   true); 
                         true),
    (member(gold,S) -> ((unexplored_safe(R,C); unknown(R,C)) -> (retract(unexplored_safe(R,C)); retract(unknown(R,C))), 
                                                                assert_fact(gold(R,C)),
                                                                assert_fact(explored_safe(R,C)),
                                                                (member(breeze,S) -> true; forall(neighbor(R,C,NR,NC,N), 
                                                                                                  is_unexplored_safe(NR,NC))),
                                                                (coins(X) -> NX is X + 1, 
                                                                             assert_fact(coins(NX)), 
                                                                             retract(coins(X)); 
                                                                             NX is 1, 
                                                                             assert_fact(coins(NX))); 
                                                true); 
                        true), 
    (member(pit,S) -> (unknown(R,C) -> retract(unknown(R,C)), 
                                       assert_fact(pit(R,C)); 
                                       true); 
                       true).