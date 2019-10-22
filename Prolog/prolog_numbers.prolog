init(1,1,1).

show(Soln) :- reverse(Soln,Forwards), write('\n'),
        member(Row,[1,2,3,4,5,6,7,8,9]),
            write('\n'),
            member(Col,[1,2,3,4,5,6,7,8,9]),
                nth1(Value,Forwards,[Row,Col]),
                write(Value),write('\t'),
        fail.

%adjacent(I,J,I+1,J):- I < 9, I >= 0, J =< 9, J >= 1.
%adjacent(I,J,I-1,J):- I =< 9, I > 1, J =< 9, J >= 1.
%adjacent(I,J,I,J+1):- I =< 9, I >= 1, J < 9, J >= 1.
%adjacent(I,J,I,J-1):- I =< 9, I >= 1, J =< 9, J > 1.



adjacent(I,J,I+1,J):- I < 2, I >= 0, J =< 2, J >= 1.
adjacent(I,J,I-1,J):- I =< 2, I > 1, J =< 2, J >= 1.
adjacent(I,J,I,J+1):- I =< 2, I >= 1, J < 2, J >= 1.
adjacent(I,J,I,J-1):- I =< 2, I >= 1, J =< 2, J > 1.

isNext([[A, B] | _], [X,Y]):- adjacent(A,B,X,Y).

complete([], F):- init(X,Y,1), complete([[X,Y]], F).
complete([], F):- \+init(_,_,1), complete([[_,_]], F).

complete(P, _):- length(P, 4).
complete(P, F):- isNext(P, [X,Y]), \+member([X,Y],P), init(X,Y,Z), length(P, C), C is Z-1, complete([[X,Y] | P], F).

complete(P, F):- isNext(P, [X,Y]), \+member([X,Y],P), \+init(X,Y,_), length(P, Z), \+init(_,_,Z+1), complete([[X,Y] | P], F).