from django.shortcuts import render

from tekis.board.models import Board

def board(request, year=None):
    if year is None:
        board = Board.objects.latest()
    else:
        board = get_object_or_404(Board, year=year)

    return render(request, "board/board.html", {
        "year": board.year,
        "members": board.boardmember_set.all(),
        "officers": board.officers,
        "other_years": Board.objects.values_list("year", flat=True).distinct()
    })
