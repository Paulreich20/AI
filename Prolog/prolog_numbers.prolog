init(2,3,46).
init(2,4,45).
init(2,6,55).
init(2,7,74).
init(3,2,38).
init(3,5,43).
init(3,8,78).
init(4,2,35).
init(4,8,71).
init(5,3,33).
init(5,7,59).
init(6,2,17).
init(6,8,67).
init(7,2,18).
init(7,8,64).
init(8,3,24).
init(8,4,21).
init(8,6,1).
init(8,7,2).
%init(1,1,13).
%init(1,5,27).
%init(2,5,24).
%init(2,2,11).
%init(4,1,71).
%init(9,1,79).
%init(4,2,70).
%init(8,2,81).
%init(8,5,62).
%init(9,5,63).
%init(1,9,39).
%init(2,8,37).
%init(5,8,34).
%init(5,9,43).
%init(8,8,53).
%init(9,9,51).
%init(2,2,1).


show(Soln) :- reverse(Soln,Forwards), write('\n'),
        member(Row,[1,2,3,4,5,6,7,8,9]),
            write('\n'),
            member(Col,[1,2,3,4,5,6,7,8,9]),
                nth1(Value,Forwards,[Row,Col]),
                write(Value),write('\t'),
        fail.


adjacent(I,J,X,J):- X is I + 1, I < 9, I >= 0, J =< 9, J >= 1.
adjacent(I,J,X,J):- X is I - 1, I =< 9, I > 1, J =< 9, J >= 1.
adjacent(I,J,I,X):- X is J + 1, I =< 9, I >= 1, J < 9, J >= 1.
adjacent(I,J,I,X):- X is J - 1, I =< 9, I >= 1, J =< 9, J > 1.

%adjacent(I,J,X,J):- X is I + 1, I < 5, I >= 0, J =< 5, J >= 1.
%adjacent(I,J,X,J):- X is I - 1, I =< 5, I > 1, J =< 5, J >= 1.
%adjacent(I,J,I,X):- X is J + 1, I =< 5, I >= 1, J < 5, J >= 1.
%adjacent(I,J,I,X):- X is J - 1, I =< 5, I >= 1, J =< 5, J > 1.

isNext([[A, B] | _], [X,Y]):- adjacent(A,B,X,Y).


solve(Final):- member(X, [1,2,3,4,5,6,7,8,9]), member(Y, [1,2,3,4,5,6,7,8,9]), \+init(X,Y,_), complete([[X,Y]], Final).

complete([], Finished):- init(X,Y,1), complete([[X,Y]], Finished).

complete(Partial, X):- length(Partial, 81), X = Partial.

complete(Partial, Finished):- isNext(Partial, [X,Y]), \+member([X,Y],Partial), init(X,Y,Z), length(Partial, C), C is Z-1, complete([[X,Y] | Partial], Finished).
complete(Partial, Finished):- isNext(Partial, [X,Y]), \+member([X,Y],Partial), \+init(X,Y,_), length(Partial, Z), \+init(_,_,Z+1), complete([[X,Y] | Partial], Finished).