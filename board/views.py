from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from board.models import Board
from board.serializers import BoardSerializer

def index(request):
    query = request.GET.get('q', '')
    if query:
        board_list = Board.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at')
    else:
        board_list = Board.objects.order_by('-created_at')
    paginator = Paginator(board_list, 5)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    return render(request, 'board/board_list.html', {
        'board_list': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'query': query,
    })

def detail(request, board_id):
    board = get_object_or_404(Board, id=board_id) # 존재하지 않을 경우 404 에러 발생
    return render(request, 'board/board_detail.html', {'board': board})

@api_view(['POST'])
def board_create(request):
    serializer = BoardSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save() # 값이 타당하면 저장
        # return Response({
        #     'message': '게시글이 성공적으로 생성되었습니다.',
        #     'data': serializer.data
        # }, status=status.HTTP_201_CREATED)
        return redirect('board:index')
    return Response({
        'message': '유효하지 않은 입력값입니다.',
        'data': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'GET'])
def board_update(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if request.method == 'POST':
        serializer = BoardSerializer(data=request.POST, instance=board) # 수정된 데이터 받아와서 board하고 업데이트
        if serializer.is_valid(): # 타당하면 저장
            serializer.save()
    elif request.method == 'GET':
        return Response({
            'message': '게시글이 성공적으로 수정되었습니다.',
            'data': board,
        }, status=status.HTTP_201_CREATED)
    return redirect('board:detail', board_id=board_id) # 새로고침

# @api_view(['DELETE']) # 왜 이 코드를 붙이면 에러가 날까?
def board_delete(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    board.delete()
    return redirect('board:index')