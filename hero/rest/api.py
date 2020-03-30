# rest_framework
from django.db import transaction
from django.http import QueryDict
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from common import LOG
from hero.rest.serializers import HeroSerializer
from hero.models import HeroModel
from rest_framework.exceptions import ParseError as Bad
from rest_framework import permissions


class HeroView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    # 获取英雄
    def get(self, request, *args, **kwargs):
        """
        ## id:英雄id 可选参数
        """
        hero_id = request.GET.get('id', {})
        LOG.debug('this is id %s' % hero_id)
        if not hero_id:
            hero = HeroModel.objects.all()
            return Response(HeroSerializer(hero, many=True).data)
        hero = HeroModel.objects.get(id=hero_id)
        return Response(HeroSerializer(hero).data)

    # 添加英雄
    def post(self, request, *args, **kwargs):
        data = request.POST
        is_hero = HeroModel.objects.filter(hero=data.get('hero')).first()
        if is_hero:
            raise Bad('英雄已经存在')
        with transaction.atomic():
            hero = HeroModel.objects.create(hero=data.get('hero', ''), gender=data.get('gender', ''),
                                            address=data.get('address', ''), weizhi=data.get('weizhi', ''),
                                            taici=data.get('taici', ''))
            if hero:
                return Response({'msg': '英雄添加成功', 'data': HeroSerializer(hero).data})
            raise Bad('添加英雄失败')

    # 更新英雄
    def put(self, request, *args, **kwargs):
        put = QueryDict(request.body)
        id = put.get('id')
        if not id:
            raise Bad('请传正确的参数')
        change_hero = get_object_or_404(HeroModel, id=id)
        # change_hero = HeroModel.objects.filter(id=id)
        # if not change_hero:
        #     raise Bad('更新失败')
        # change_hero.update(**list(put.items())[0][0])
        # change_hero.update(**put)
        change_hero.hero = put.get('hero')
        change_hero.gender = put.get('gender')
        change_hero.address = put.get('address')
        change_hero.weizhi = put.get('weizhi')
        change_hero.taici = put.get('taici')
        change_hero.save()
        return Response('更新成功')

    # 删除英雄
    def delete(self, request, *args, **kwargs):
        delete = QueryDict(request.body)
        id = delete.get('id')
        if not id:
            return Bad('请传正确的参数')
        del_hero = HeroModel.objects.filter(id=id).delete()
        if not del_hero:
            raise Bad('删除英雄失败')
        return Response('操作成功')
