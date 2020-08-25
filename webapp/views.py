# -*- coding: utf-8 -*-
import operator
import uuid

from datetime import datetime

from django.http import JsonResponse

from django.contrib.auth.models import User

from django.shortcuts import render, render_to_response
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, View, TemplateView
from django.views.generic.detail import DetailView
from django.db.models import Q

from hitcount.views import HitCountDetailView

from webapp.models import ReadPost, Category, Tag, Profile, Referal
from webapp.serializers import ProfileSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class Clock(TemplateView):
    template_name = 'clock.html'


class HomePage(ListView):
    template_name = 'main.html'
    model = ReadPost

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['last_posts'] = ReadPost.objects.filter(status='published') \
                                            .filter(date__lte=datetime.now())[:7]
        context['rand_posts'] = ReadPost.objects.filter(status='published') \
                                            .filter(date__lte=datetime.now()) \
                                            .order_by('?')[:5]
        return context


class NewPosts(ListView):
    model = ReadPost
    template_name = 'new_posts.html'
    paginate_by = 5
    context_object_name = 'new_posts'

    def get_queryset(self):
        return ReadPost.objects.filter(status='published') \
                           .filter(date__lte=datetime.now())


class PopularPosts(ListView):
    template_name = 'popular_posts.html'
    model = ReadPost

    def get_context_data(self, **kwargs):
        context = super(PopularPosts, self).get_context_data(**kwargs)
        context['pop_posts'] = ReadPost.objects.filter(status='published') \
                                           .filter(date__lte=datetime.now()) \
                                           .order_by('views')[:10]
        return context


class CategoryPosts(ListView):
    template_name = "category_posts.html"
    model = ReadPost
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CategoryPosts, self).get_context_data(**kwargs)
        context['cat_posts'] = ReadPost.objects.filter(status='published') \
                                           .filter(date__lte=datetime.now()) \
                                           .filter(category__slug=self.kwargs.get('slug'))
        context['category'] = Category.objects.get(slug=self.kwargs.get('slug'))
        return context


class ViewPost(HitCountDetailView):
    model = ReadPost
    template_name = "post.html"
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(ViewPost, self).get_context_data(**kwargs)
        r_post = ReadPost.objects.get(slug=self.kwargs['slug'])
        context['read_post'] = r_post
        context['similar'] = ReadPost.objects.filter(date__lte=datetime.now()) \
                                         .filter(category=r_post.category) \
                                         .order_by('?')[:3]
        return context


class TagPosts(ListView):
    model = Tag
    template_name = "tag.html"

    def get_context_data(self, **kwargs):
        context = super(TagPosts, self).get_context_data(**kwargs)
        context['tag_posts'] = ReadPost.objects.filter(date__lte=datetime.now()) \
                                               .filter(tag__slug=self.kwargs['slug'])
        context['tag'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context


def search(request):
    """
    messages = []
    result = ''
    result_event = ''
    result_fact = ''
    args = {}
    if 'search_phrase' in request.GET and request.GET['search_phrase']:
        try:
            search_phrase = request.GET.get('search_phrase')
            logger.error(search_phrase)
            if not len(search_phrase):
                messages.append(_('Ви не ввели ничего. Пожалуйста, введите данные для поиска.'))
            elif len(search_phrase) > 20:
                messages.append(_('Пожалуйста, введите меньше чем 20 символов.'))
            else:
                result = Post.objects.filter(Q(title__icontains=search_phrase)|Q(content__icontains=search_phrase))
                result_event = Event.objects.filter(Q(title__icontains=search_phrase)|Q(content__icontains=search_phrase))
                result_fact = Fact.objects.filter(Q(title__icontains=search_phrase)|Q(content__icontains=search_phrase))
                if not len(result) and not len(result_event) and not len(result_fact):
                    messages.append(_('Ничего не найдено.'))
        except Exception:
            messages.append(_('Извините. На данный момент поиск не доступен'))
    args['result'] = result
    args['result_event'] = result_event
    args['result_fact'] = result_fact
    args['messages'] = messages
    return render_to_response('search.html', args)
    """
    messages = []
    result = ''
    args = {}
    if 'search_phrase' in request.GET and request.GET['search_phrase']:
        try:
            search_phrase = request.GET.get('search_phrase')
            if not len(search_phrase):
                messages.append('You didn\'t enter data. Please, enter a search term.')
            elif len(search_phrase) > 20:
                messages.append('Please enter at most 20 charachters.')
            else:
                result = ReadPost.objects.filter(Q(title__icontains=search_phrase)|Q(content__icontains=search_phrase))
                if not len(result):
                    messages.append('Sorry, your search returned no matches.')
        except Exception:
            messages.append('Sorry. Search now is not available.')
    args['result'] = result
    args['messages'] = messages
    args['title_1'] = 'result'
    args['title_2'] = 'results'
    args['count'] = len(result)
    return render_to_response('search.html', args)


# def handler404(request, exception, template_name="404.html"):
#     response = render_to_response("404.html")
#     response.status_code = 404
#     return response
#
#
# def handler500(request, exception, template_name="500.html"):
#     response = render_to_response("500.html")
#     response.status_code = 500
#     return response


def about(request):
    return render(request, 'about.html')


###########################

class UserProfileRest(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_request(self, request):
        android_id = request.data.get('android_id')
        if not android_id:
            return {
                'message': f'"android_id" is required field'
            }, 400

        profile = Profile.objects.filter(android_id=android_id)

        if not profile:
            return {
                'message': f'User with android_id="{android_id}" does not exist'
            }, 404

        response_data = {
            'android_id': profile[0].android_id,
            'referal_id': profile[0].referal_id,
            'username': profile[0].username,
            'score': profile[0].score,
            'friend_score': profile[0].friend_score,
            'money_output': profile[0].money_output,
            'timestamp': profile[0].timestamp,
            'views': profile[0].views
        }
        return response_data, 200

    def get(self, request):
        response_data, status = self.get_request(request)
        return Response(response_data, status=status)

    def delete(self, request):
        android_id = request.data.get('android_id')
        profile = Profile.objects.filter(android_id=android_id)
        if not profile:
            return Response({
                'message': f'User with android_id="{android_id}" does not exist'
            }, status=404)

        profile[0].delete()

        return Response({
            'message': f'user android_id="{android_id}" succesfuly deleted'
        }, status=200)

    def post(self, request):
        if request.data.get('type') == 'GET':
            response_data, status = self.get_request(request)
            return Response(response_data, status=status)
        else:
            data = {
                'android_id': request.data.get('android_id'),
                'username': request.data.get('username', 'User'),
                'referal_id': uuid.uuid1().hex,
                'timestamp': datetime.now().isoformat()
            }

            if not data.get('android_id'):
                return Response({
                    'message': f'"android_id" is required field'
                }, status=400)

            profile = Profile.objects.filter(android_id=data.get('android_id'))
            if profile:
                return Response({
                    'message': f'User with android_id="{data.get("android_id")}" already exist'
                }, status=400)

            try:
                profile.create(**data)
            except Exception as e:
                return Response({'message': str(e)}, status=400)

            return Response({'message': 'success'}, status=200)

    def put(self, request):

        android_id = request.data.get('android_id')

        data = {
            'username': request.data.get('username'),
            'score': request.data.get('score'),
            'friend_score': request.data.get('friend_score'),
            'money_output': request.data.get('money_output'),
            'views': request.data.get('views'),
        }

        data = {k: v for k, v in data.items() if v is not None}

        if not android_id:
            return Response({
                'message': f'"android_id" is required field'
            }, status=400)

        profile = Profile.objects.filter(android_id=android_id)

        if not profile:
            return Response({
                'message': f'User with android_id="{android_id}" does not exist'
            }, status=404)

        try:
            profile.update(**data)
        except Exception as e:
            return Response({'message': str(e)}, status=400)

        return Response({'message': 'success'}, status=200)



class ReferalRest(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_request(self, request):
        android_id = request.data.get('android_id')
        referal_id = request.data.get('referal_id')
        if not android_id and not referal_id:
            return {
                'message': f'"android_id" or "referal_id" required field'
            }, 400

        referals = None

        if android_id:
            referals = Referal.objects.filter(android_id_from=android_id)
        elif referal_id:
            referals = Referal.objects.filter(referal_id=referal_id)

        if not referals:
            return {
               'items': []
            }, 200

        response_data = {
            'items': [],
            'profile_from': referals[0].android_id_from,
            'referal_id': referal_id
        }

        if not referals:
            return response_data, 200


        android_ids = referals.values_list('android_id_to', flat=True)

        profiles = Profile.objects.filter(android_id__in=android_ids)

        for el in profiles:
            response_data['items'].append({
                'android_id': el.android_id,
                'username': el.username,
                'score': el.score,
                'friend_score': el.friend_score,
                'money_output': el.money_output,
                'timestamp': el.timestamp,
                'views': el.views
            })
        return response_data, 200

    def get(self, request):
        response_data, status = self.get_request(request)
        return Response(response_data, status=status)

    def delete(self, request):
        android_id_from = request.data.get('android_id_from')
        android_id_to = request.data.get('android_id_to')
        referal_id = request.data.get('referal_id')
        if not android_id_from and not android_id_to and not referal_id:
            return Response({
                'message': f'"android_id_from" or "android_id_to" or "referal_id" required field'
            }, status=400)

        if android_id_from:
            referals = Referal.objects.filter(android_id_from=android_id_from)

            if not referals:
                return Response({
                    'message': f'Referals with android_id="{android_id_from}" does not exist'
                }, status=404)

            referals[0].delete()

            return Response({'message': 'success'}, status=200)

        if android_id_to:
            referals = Referal.objects.filter(android_id_to=android_id_to)

            if not referals:
                return Response({
                    'message': f'Referals with android_id="{android_id_to}" does not exist'
                }, status=404)

            referals[0].delete()

            return Response({'message': 'success'}, status=200)

        if referal_id:
            referals = Referal.objects.filter(referal_id=referal_id)

            if not referals:
                return Response({
                    'message': f'Referals with referal_id="{referal_id}" does not exist'
                }, status=404)

            for ref in referals:
                ref.delete()

            return Response({'message': 'success'}, status=200)

    def post(self, request):
        if request.data.get('type') == 'GET':
            response_data, status = self.get_request(request)
            return Response(response_data, status=status)
        else:
            data = {
                'referal_id': request.data.get('referal_id'),
                'android_id_to': request.data.get('android_id_to'),
            }

            if not data.get('referal_id') and not data.get('android_id_to'):
                return Response({
                    'message': f'"android_id_to" and "referal_id" are required fields'
                }, status=400)

            referal_id_profile = Profile.objects.filter(referal_id=data.get('referal_id'))
            if not referal_id_profile:
                return Response({
                    'message': f'profile with referal_id="{data.get("referal_id")}" does not exist'
                }, status=400)

            profile_to = Profile.objects.filter(android_id=data.get('android_id_to'))
            if not profile_to:
                return Response({
                    'message': f'profile android_id_to="{data.get("android_id_to")}" does not exist'
                }, status=400)

            try:
                ref = Referal(
                    android_id_from=referal_id_profile[0].android_id,
                    android_id_to=data.get('android_id_to'),
                    referal_id=data.get('referal_id')
                )
                ref.save()
            except Exception as e:
                return Response({'message': str(e)}, status=400)

            return Response({
                'referal_id': data.get('referal_id'),
                'android_id_from': referal_id_profile[0].android_id,
                'android_id_to': request.data.get('android_id_to'),
                'message': 'success'
            }, status=200)


class ReferalAction(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def post(self, request):
        android_id = request.data.get('android_id')

        referal = Referal.objects.filter(android_id_to=android_id)
        if not referal:
            return Response({
                'message': f'referal for android_id_to="{android_id}" does not exist'
            }, status=400)

        referal_id = referal[0].referal_id

        profile = Profile.objects.filter(referal_id=referal_id)
        if not profile:
            return Response({
                'message': f'profile for referal_id="{referal_id}" does not exist'
            }, status=400)

        try:
            profile.update(
                score=profile[0].score + 1000,
                friend_score=profile[0].friend_score + 10
            )
        except Exception as e:
            return Response({'message': str(e)}, status=400)

        return Response({'message': 'success'}, status=200)
