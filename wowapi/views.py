from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Question
from .serializer import QuestionSerializer
from bs4 import BeautifulSoup

import requests
import json

# Create your views here.


def index(request):
    return HttpResponse("Success")


class QuestionAPI(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


def latest(request):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        res = requests.get("https://stackoverflow.com/questions",headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        q = soup.find_all('a',class_="s-link")
        votes = soup.find_all('span',class_="s-post-summary--stats-item-number")

        # final storage variables
        vote_count = []
        views_count = []
        tagger = []
        questions = []
        for i,value in enumerate(votes):
            if(i%3==0):
                vote_count.append(value.text) 
            elif(i%3==2):
                views_count.append(value.text)

        tags = soup.find_all('ul',class_="ml0 list-ls-none js-post-tag-list-wrapper d-inline")
        tao = []
        for i in tags:
            i.find_all('a') 
            for j in i:
                tao.append(j.text)
            tagger.append(tao)  


        for i in q:
            if ((i.text).strip()!="") and ((i.text).strip() != "Hot Network Questions") and ((i.text).  strip() != "Get early access"):
                questions.append(i.text.strip())
        
        # print(len(questions),len(tagger),len(views_count),len(vote_count))

            # questions_data['questions'].append({
            #     "question":i,
            #     "tags":j,
            #     "views":k,
            #     "vote_count":l,
            # })
        for i, j, k, l in zip(questions,tagger,views_count,vote_count):
            question = Question()
            question.question = i
            question.vote_count = l
            question.views = k
            question.tags = j

            question.save()

        return HttpResponse("Latest Data Fetched from Stack Overflow")
    except:
        return HttpResponse(f"Failed idc idk")