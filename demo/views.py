from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from demo.models import *


#  ----------------展示登录人员的所有权限-------------------------
# def show_permission(request):
#     """
#         1. 根据输入的账号密码取出具体的用户，查询用胡
#         2. 用户对应的角色
#         3. 通过角色获取对应的权限
#     :param request:
#     :return:
#     """
#     username = request.GET['username']
#     # username = 'smart'
#     # user = User.objects.all().filter(username=username).first()
#     #  取出对应的role 第一种方式
#     # datas = user.userrole_set.all()
#     # for data in datas:
#     #     print(data.role)
#     # 第二种方式，通过中间表进行获取
#     roles = Role.objects.all().filter(userrole__user__username=username)
#     #  前端显示并不需要直接的管理动作
#     # role_permission = RolePermissionAction.objects.all().filter(role__in=roles)\
#     #     .values('permission_action__permission__name',
#     #             'permission_action__permission__url',
#     #             'permission_action__action__action',
#     #             'permission_action__action__name',
#     #             ).distinct()
#     #  根据权限去重复  不需要考虑具体东动作
#     role_permission = RolePermissionAction.objects.all().filter(role__in=roles) \
#         .exclude(permission_action__permission__menu__isnull=True) \
#         .values('permission_action__permission__name',
#                 'permission_action__permission__url',
#                 'permission_action__permission_id',
#                 'permission_action__permission__menu_id',
#                 ).distinct()
#     # {'menu_id: [permission]'} 不同permission对应同一个菜单
#     permission_menus = {}
#     for permission in role_permission:
#         new_permission = {
#             'id': permission['permission_action__permission_id'],
#             'name': permission['permission_action__permission__name'],
#             'url': permission['permission_action__permission__url'],
#             'parent_id': permission['permission_action__permission__menu_id'],
#             'child': []  #
#         }
#         if new_permission['parent_id'] in permission_menus:
#             permission_menus[new_permission['parent_id']].append(new_permission)
#         else:
#             permission_menus[new_permission['parent_id']] = [new_permission, ]
#
#     print(permission_menus)
#     # -------------------菜单对应的权限------------------------------
#     for k, v in permission_menus.items():
#         print(k, v)
#     # ----------------------拿到对应的菜单-------------------------------------
#     # 菜单id
#     menu_list = Menu.objects.all().values('id', 'name', 'parent_id')
#     menu_list_dict = {}
#     for item in menu_list:
#         item['child'] = []
#         menu_list_dict[item['id']] = item
#     print(menu_list_dict)
#     #  permission_menu  和 permission_list_dict 进行合并
#     for k, v in permission_menus.items():
#         menu_list_dict[k]['child'] = v
#     #  以上是将权限全部
#     for value in menu_list_dict.values():
#         if not value['parent_id']:
#             pass
#         else:
#             menu_list_dict[value['parent_id']]['child'].append(value)
#     return render(request, 'show.html', locals())
def show_permission(request):
    """
    1.根据前端获取到的用户信息查询此用户对应的角色
    2.根据角色查询对应的权限
    3.根据权限得到具体的动作
    :param request:
    :return:
    """
    username = request.GET.get('username', None)
    user = User.objects.all().filter(username=username).first()
    # datas = user.userrole_set.all()
    # print('*********************************')
    # print(datas)
    # 第一种方式获取用户所对应的权限信息
    # for data in datas:
    #     print(data.role)
    #
    # 第二种方式，通过角色用户中间表反向解析用户信息进行获取数据
    roles = Role.objects.all().filter(userrole__user__username=username)
    # print(roles)
    # 第三种  直接操作中间表
    # 前端不许显示具体的职位以及操作，只显示权限管理
    # 通过角色权限动作中间表处理数据
    # 第一步： 通过角色权限中间表获取对象
    role_permission = RolePermissionAction.objects.all().filter(role__in=roles)
    # 通过distinct()去重， 根据权限去重 不需要考虑具体操作
    result = role_permission.values('permission_action__permission__name').distinct()
    for i in result:
        print(i)
    return HttpResponse('响应成功')
