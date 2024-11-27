:- dynamic breeze/2.
:- dynamic glitter/2.
:- dynamic pit/2.
:- dynamic gold/2.
:- dynamic unexplored_safe/2.
:- dynamic explored_safe/2.
:- dynamic home/2.
:- dynamic unknown/2.

tae(maasim).
assert_fact(N) :-
    not(N), %writeln(N),
    assertz(N).

in_bounds(R,C,N) :-
    R >= 1, R =< N,
    C >= 1, C =< N.

initialize_start(R,C,N) :-
    assert_fact(home(R,C)),
    assert_fact(explored_safe(R,C)),

    forall(
    (
        member((DR, DC), [(-1, 0), (1, 0), (0, -1), (0, 1)]),  % Offsets for neighbors
        NR is R + DR,
        NC is C + DC,
        in_bounds(NR,NC,N)
    ),  assert_fact(unexplored_safe(NR,NC))).

assert_explored_safe(R,C,N) :-
    (unexplored_safe(R, C); unknown(R, C)),
    (retract(unexplored_safe(R,C)); retract(unknown(R,C))),
    assert_fact(explored_safe(R,C)),
    assert_unexplored_safe_adjacent(R,C,N).

assert_breeze(R,C,N) :-
    unexplored_safe(R, C),
    retract(unexplored_safe(R,C)),
    assert_fact(breeze(R,C)),
    assert_unknown_adjacent(R,C,N).

assert_glitter(R,C,N) :-
    unexplored_safe(R, C),
    retract(unexplored_safe(R,C)),
    assert_fact(glitter(R,C)),
    assert_unknown_adjacent(R,C,N).

assert_unknown_adjacent(R,C,N) :-
    (breeze(R,C); glitter(R,C)), 
    forall(
    (
        member((DR, DC), [(-1, 0), (1, 0), (0, -1), (0, 1)]),  % Offsets for neighbors
        NR is R + DR,
        NC is C + DC,
        in_bounds(NR,NC,N),
        not(explored_safe(NR,NC)),
        not(unexplored_safe(NR,NC)),   
        not(home(NR,NC))
    ),  assert_fact(unknown(NR,NC))).

assert_unexplored_safe_adjacent(R,C,N) :-
    explored_safe(R,C), not(breeze(R,C)), not(glitter(R,C)),
    forall(
    (
        member((DR, DC), [(-1, 0), (1, 0), (0, -1), (0, 1)]),  % Offsets for neighbors
        NR is R + DR,
        NC is C + DC,
        in_bounds(NR,NC,N),
        not(home(NR,NC)),
        not(unknown(NR,NC)),
        not(explored_safe(NR, NC))
    ),  assert_fact(unexplored_safe(NR,NC))).


%get_pit(R,C,N) :- % Assuming the position entered is a breeze.

fall(R,C) :-
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