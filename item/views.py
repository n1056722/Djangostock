from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from rest_framework import generics, authentication, exceptions
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from appuser.models import AppUser, AppUserLog
from item.models import Item
from item.serializers import ItemListSerializer, ItemRetrieveSerializer


# class ItemAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         token = request.META.get('HTTP_TOKEN')
#         if not token:
#             data = {
#                 'status': 403,
#                 'msg': '認證未通過',
#             }
#             return JsonResponse(data=data)
#         try:
#             token = AppUser.objects.get(token=token)
#         except token.DoesNotExist:
#             raise exceptions.AuthenticationFailed('No such user')


# api股票列表

class ItemListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)  #
        return Response(data={'items': serializer.data})
    # authentication_classes = [ItemAuthentication, ]
    # permission_classes = (permissions.IsAuthenticated,)  # 權限
    # filter_backends = (OrderingFilter, SearchFilter)  # 排序 搜尋欄功能
    # ordering_fields = ('id', 'name')  # 可依照id 名字做排序
    # search_fields = ('name',)  # 可依照名字欄位做關鍵字搜尋
    # ordering = ('id',)  # 排序
    # pagination_class = LimitOffsetPagination  # 前端一頁要顯示幾個項目+分頁


# api股票詳情

class ItemRetrieveView(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemRetrieveSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = [ItemAuthentication, ]


# 後台股票列表
# @login_required
def list(request):
    items = Item.objects.all()
    item_list = []
    for item in items:
        item_list.append(
            {
                'id': item.id,
                'name': item.name,
                'value': item.value,
            }
        )
    data = {
        'title': '股票管理後台',
        'item_list': item_list,
    }
    return render(request, 'item/list.html', context=data)


@login_required  # 新增股票
def add(request):
    if request.method == 'GET':
        data = {
            'title': '新增股票'
        }
        return render(request, 'item/add.html', context=data)
    elif request.method == 'POST':
        name = request.POST.get('name')
        value = request.POST.get('value')
        items = Item()
        items.name = name
        items.value = value
        items.save()
        return redirect(reverse('item:list'))


@login_required  # 股票編輯
def edit(request, pk):
    item = get_object_or_404(Item, id=pk)
    if request.method == 'GET':
        data = {
            'title': '修改',
            'pk': item.id,
            'name': item.name,
            'value': item.value,
        }
        return render(request, 'item/edit.html', context=data)
    elif request.method == 'POST':
        name = request.POST.get('name')
        value = request.POST.get('value')
        item.name = name
        item.value = value
        item.save(update_fields=['name'])
        item.save(update_fields=['value'])
        return redirect(reverse('item:list'))


@login_required  # 刪除
def delete(request, pk):
    Item.objects.get(pk=pk).delete()
    messages.add_message(request, messages.INFO, '已刪除股票')
    return redirect(reverse('item:list'))


@login_required  # 首頁
def home(request):
    return render(request, 'main/home.html')


