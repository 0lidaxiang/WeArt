#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import JsonResponse
from django.shortcuts import render
# from django.shortcuts import redirect
# from book.models import book
# from chapter.models import chapter
from version.models import version

def chapterVersionVote(request):
    if "readerId" not in request.session:
        return render(request, 'reader/login.html')

    # print request.GET['idVersion']
    context = {}

    if 'idVersion' not in request.GET:
        context['status'] = "fail"
        context['message'] = "The idVersion variable is not in request.GET."
        return JsonResponse(context)
    idVersion = request.GET['idVersion']
    if idVersion == "":
        context['status'] = "fail"
        context['message'] = "投票评分为空"
        return JsonResponse(context)

    if 'rating' not in request.GET:
        context['status'] = "fail"
        context['message'] = "The rating variable is not in request.GET."
        return JsonResponse(context)
    ratingUser = request.GET['rating']
    if ratingUser == "":
        context['status'] = "fail"
        context['message'] = "投票评分为空"
        return JsonResponse(context)

    if 'chapterFileName' not in request.GET:
        context['status'] = "fail"
        context['message'] = "The idChapter variable is not in request.GET."
        return JsonResponse(context)
    chapterFileNameUser = request.GET['chapterFileName']
    if chapterFileNameUser == "":
        context['status'] = "fail"
        context['message'] = "章节编号为空"
        return JsonResponse(context)

    try:
        # get old rating
        res,statusNumber,mes =  version.getValueById(idVersion, "all")
        if not res:
            context['res'] = "fail"
            context['statusNumber'] = statusNumber
            context['message'] = '錯誤： ' + str(statusNumber) + " ， " + mes
            return JsonResponse(context)
        
        # check is or not this chapter
        # modify the voteCount and socre into database
        voteCountNew = int(mes.voteCount) + 1
        scoreNew = (float(mes.score) + float(ratingUser)) / voteCountNew
        res, statusNumber, mes = version.modifyObj(idVersion, "voteCount", voteCountNew)
        if not res:
            context['res'] = "fail"
            context['statusNumber'] = statusNumber
            context['message'] = '錯誤： ' + str(statusNumber) + " ， " + mes
            return JsonResponse(context)

        res, statusNumber, mes = version.modifyObj(idVersion, "score", scoreNew)
        if not res:
            context['res'] = "fail"
            context['statusNumber'] = statusNumber
            context['message'] = '錯誤： ' + str(statusNumber) + " ， " + mes
            return JsonResponse(context)

        context['res'] = "success"
        context['statusNumber'] = 180500
        context['message'] = str(statusNumber) + " : " + mes

    except Exception as e:
        context['res'] = "fail"
        context['message'] = "異常錯誤: " + str(180501) + " " + str(e)

    return JsonResponse(context)
