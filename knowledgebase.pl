:- dynamic breeze/2.
:- dynamic glitter/2.
:- dynamic pit/2.
:- dynamic gold/2.
:- dynamic safe/2.
:- dynamic home/2.
:- dynamic unknown/2.

tae(maasim).

assert_fact(N) :-
    not(N), writeln(N),
    assertz(N).

in_bounds(R,C,N) :-
    R >= 1, R =< N,
    C >= 1, C =< N.

initialize_start(R,C,N) :-
    assert_fact(home(R,C)),
    assert_fact(safe(R,C)),
    forall(
    (
        member((DR, DC), [(-1, 0), (1, 0), (0, -1), (0, 1)]),  % Offsets for neighbors
        NR is R + DR,
        NC is C + DC,
        in_bounds(NR,NC,N)
    ),  assert_fact(safe(NR,NC))).

assert_unknown_adjacent(R,C,N) :-
    (breeze(R,C); glitter(R,C)), 
    forall(
    (
        member((DR, DC), [(-1, 0), (1, 0), (0, -1), (0, 1)]),  % Offsets for neighbors
        NR is R + DR,
        NC is C + DC,
        in_bounds(NR,NC,N),
        not(safe(NR,NC))
    ),  assert_fact(unknown(NR,NC))).

assert_safe_adjacent(R,C,N) :-
    safe(R,C), not(breeze(R,C)), not(glitter(R,C)),
    forall(
    (
        member((DR, DC), [(-1, 0), (1, 0), (0, -1), (0, 1)]),  % Offsets for neighbors
        NR is R + DR,
        NC is C + DC,
        in_bounds(NR,NC,N),
        not(home(NR,NC)),
        not(unknown(NR,NC))
    ),  assert_fact(safe(NR,NC))).


% get_pit(R,C,N) :- % Assuming the position entered is a breeze.

replace_unknown(R,C) :-
    unknown(R,C),
    retract(unknown(R,C)),
    assert_fact(safe(R,C)).

% replace_unknown_safe

end(R,C) :-
    pit(R,C).

grab(R,C) :-
    gold(R,C).


/* 
Possible Revision:

get_pit: given user explored all surrounding breeze cells, deduce pit
unexplored_safe
only one predicate for asserting a fact and assuming adjacents cells for breeze, safe, glitter.

count gold bars to decide whether win or lose
check if at home with enough goldbars


*/