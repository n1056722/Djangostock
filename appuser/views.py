from datetime import timedelta
from django.db import connection

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import ExtractHour, ExtractMinute
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
# Create your views here.
from django.urls import reverse
import secrets

from django.utils.datetime_safe import datetime

from appuser.models import AppUser, AppUserLog


@login_required
def list(request):
    appusers = AppUser.objects.all()
    appuser_list = []
    for appuser in appusers:
        appuser_list.append(
            {
                'id': appuser.id,
                'name': appuser.name,
                'token': appuser.token,
                'secretkey': appuser.secret_key,
                'is_enable': appuser.is_enable,
            }
        )
    data = {
        'title': '股票管理後台',
        'appuser_list': appuser_list,
    }
    return render(request, 'appuser/list.html', context=data)


@login_required
def add(request):
    if request.method == 'GET':
        data = {
            'title': '新增appuser'
        }
        return render(request, 'appuser/add.html', context=data)
    elif request.method == 'POST':
        name = request.POST.get('name')
        token = secrets.token_hex(10)
        secretkey = secrets.token_urlsafe(20)
        appuser = AppUser()
        appuser.name = name
        appuser.token = token
        appuser.secret_key = secretkey
        appuser.save()
        return redirect(reverse('appuser:list'))


@login_required
def edit(request, pk):
    appuser = get_object_or_404(AppUser, id=pk)
    if request.method == 'GET':
        data = {
            'title': '修改權限',
            'pk': appuser.id,
            'name': appuser.name,
            'is_enable': appuser.is_enable,
        }
        return render(request, 'appuser/edit.html', context=data)
    elif request.method == 'POST':
        is_enable = request.POST.get('is_enable')
        appuser.is_enable = is_enable
        appuser.save(update_fields=['is_enable'])
        return redirect(reverse('appuser:list'))


def pie_chart(request):  # 用圓餅圖顯示24小時內 誰打了Api打了幾次
    labels = []
    data = []
    now = timezone.now()
    start = now - timedelta(hours=23, minutes=59, seconds=59)
    qs = AppUserLog.objects.values('app_user_id').filter(create_at__gt=start).annotate(total=Count('path')).order_by(
        'total')
    for app_user in qs:
        labels.append(app_user['app_user_id'])
        data.append(app_user['total'])
    log_data = {
        'labels': labels,
        'data': data,
    }
    return render(request, 'appuser/pie_chart.html', context=log_data)


def line_chart(request):  # 用線圖顯示24小時內每小時api打的次數
    labels = []
    data = []
    now = timezone.now()
    start = now - timedelta(hours=23, minutes=59, seconds=59)
    hour_data = AppUserLog.objects.filter(create_at__gt=start)
    count_res = hour_data.annotate(hour=ExtractHour('create_at')).values('hour').order_by('hour').annotate(
        count=Count('path'))
    for i in count_res:
        labels.append(i['hour'])
        data.append(i['count'])
        """
            做出小時對應次數的mapping
            {
                11: 1,
                12: 6,
                14: 4,
            }
        """
    label_mapping_data = {}
    for i in range(len(labels)):
        label_mapping_data[labels[i]] = data[i]
        # 開始補資料`

    new_labels = []
    new_data = []
    for i in range(24):
        if i in label_mapping_data:  # 如果該小時有資料則用資料
            new_labels.append(i)
            new_data.append(label_mapping_data[i])
        else:  # 沒的話就補0
            new_labels.append(i)
            new_data.append(0)

        # 旋轉, 不然都是從0時開始, 可以根據現在幾點去做旋轉

    def rotate(l, n):
        return l[n:] + l[:n]

    now_hour = datetime.now().hour + 1
    new_labels = rotate(new_labels, now_hour)
    new_data = rotate(new_data, now_hour)

    labels_min = []
    data_min = []
    now_min = timezone.now()
    start_min = now_min - timedelta(minutes=59, seconds=59)
    min_data = AppUserLog.objects.filter(create_at__gt=start_min)
    count_min = min_data.annotate(minute=ExtractMinute('create_at')).values('minute').order_by('minute').annotate(
        count=Count('path'))
    for i in count_min:
        labels_min.append(i['minute'])
        data_min.append(i['count'])

    label_min_mapping_data = {}
    for i in range(len(labels_min)):
        label_min_mapping_data[labels_min[i]] = data_min[i]
    new_labels_min = []
    new_data_min = []
    for i in range(60):
        if i in label_min_mapping_data:  # 如果該分鐘有資料則用資料
            new_labels_min.append(i)
            new_data_min.append(label_min_mapping_data[i])
        else:  # 沒的話就補0
            new_labels_min.append(i)
            new_data_min.append(0)

    now_minute = datetime.now().minute + 1
    new_labels_min = rotate(new_labels_min, now_minute)
    new_data_min = rotate(new_data_min, now_minute)
    log_data = {
        'labels': new_labels,
        'data': new_data,
        'labels_min': new_labels_min,
        'data_min': new_data_min,
    }

    print(log_data)
    return render(request, 'appuser/line_chart.html', context=log_data, )
