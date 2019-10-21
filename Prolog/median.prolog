partition([],_,[],[]).
partition([X],V,[X],[]):- X < V.
partition([X],V,[],[X]):- X > V.

partition([H | T],V,[H | A],B):- H < V, partition(T,V,A,B).
partition([H | T],V,A,[H | B]):- H > V, partition(T,V,A,B).
partition([H | T],V,A,B):- H is V, partition(T,V,A,B).

len([],[]).
len([_ | T1], [_ | T2]):- len(T1, T2).

median([],[]).
median([X],X).
median(L,M):- member(M,L), partition(L,M,A,B), len(A,B).
