from django.db import models

""" 
    基于角色的权限管理  无法依靠简单的会员级别，
    基于RBAC
    分析表关系：
        1.用户表 
        2.角色表
        3.用户角色中间表   用户和角色
    
"""


# ---------------------用户角色表---------------------------------
class User(models.Model):
    """
        用户表
    """
    username = models.CharField('用户名', max_length=50)
    password = models.CharField('密码', max_length=32)

    class Meta:
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Role(models.Model):
    """
        角色表
    """
    name = models.CharField('角色名称', max_length=50)

    class Meta:
        verbose_name = '角色表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserRole(models.Model):
    """
        用户和角色之间的中间表， 用户角色之前产生多对多关系
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '用户和角色之间的中间表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户: %s ----> 角色：%s' % (self.user.username, self.role.name)


# ----------------------菜单数据和权限关联------------------------------
class Menu(models.Model):
    """
        菜单表，没有菜单显就不显示权限
    """
    name = models.CharField('菜单名', max_length=20)
    # 菜单有一个父级菜单
    parent = models.ForeignKey('self', models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = '菜单表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Permission(models.Model):
    """
        权限表
    """
    name = models.CharField('权限名称', max_length=50)
    url = models.CharField('权限URL', max_length=200)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Action(models.Model):
    """
        动作表
    """
    name = models.CharField('动作名', max_length=50)
    action = models.CharField('具体动作', max_length=50)

    class Meta:
        verbose_name = '动作表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PermissionAction(models.Model):
    """
        权限动作之间的中间表
    """
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name='权限')
    action = models.ForeignKey(Action, on_delete=models.CASCADE, verbose_name='动作')

    class Meta:
        verbose_name = '权限动作中间表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '权限：%s ------> 动作：%s' % (self.permission.name, self.action.name)


# -----------------------角色和权限相关联----------------------------------

class RolePermissionAction(models.Model):
    """
        角色和权限动作中间表
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission_action = models.ForeignKey(PermissionAction, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '角色和权限动作中间表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '角色：%s -->权限：%s ------> 动作：%s' % (
        self.role.name, self.permission_action.permission.name, self.permission_action.action.name)
