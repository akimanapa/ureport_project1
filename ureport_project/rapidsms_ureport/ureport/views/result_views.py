#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from script.models import ScriptStep
from django.contrib.auth.decorators import login_required
from generic.views import generic
from django.views.decorators.cache import cache_control, never_cache
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from rapidsms_xforms.models import XFormField, XForm
from ureport.models.utils import recent_message_stats
from ussd.models import StubScreen
from poll.models import Poll, Category, Rule, Translation, Response
from poll.forms import CategoryForm, RuleForm2
from rapidsms.models import Contact
from ureport.forms import NewPollForm, GroupsFilter
from django.conf import settings
from ureport.forms import AssignToPollForm, SearchResponsesForm, AssignResponseGroupForm, ReplyTextForm, DeleteSelectedForm
from django.contrib.sites.models import Site, get_current_site
from ureport import tasks
from ureport.utils import get_polls, get_script_polls, get_access
from generic.sorters import SimpleSorter
from ureport.views.utils.paginator import ureport_paginate
from django.db import transaction
from django.contrib.auth.models import Group, User #, Message
from ureport.models import UPoll
import logging, datetime
from ureport.utils import retrieve_poll #, retrieve_gp
from ureport.views.utils.tags import _get_tags, _get_tags1
from django.http import HttpResponse, Http404


def view_data(request,group_name,poll_id):
    
    poll=Poll.objects.get(pk=poll_id)
    responses=Response.objects.filter(contact__groups__name=group_name,poll__pk=poll_id)
    group=group_name
    template='ureport/poll_results.html'
    return render_to_response(template,
                              {'responses':responses,
                               'poll':poll,
                               'group':group
                               },
                               context_instance=RequestContext(request))

def view_cloud(request,group_name,poll_id):
        
    module = False
    #response=Response.objects.filter(pk=poll_id)
    if 'module' in request.GET:
        module = True
    polls = retrieve_poll(request, poll_id)
    try:
        poll = polls[0]
    except IndexError:
        raise Http404
    
    try:
        rate = poll.responses.count() * 100 / poll.contacts.count()
    except ZeroDivisionError:
        rate = 0
    dict_to_render = {
        
        'poll': poll,
        'polls': [poll],
        'unlabeled': True,
        'module': module,
        'rate': int(rate),
        }
        
    gp=Group.objects.all()
    for g in gp:
       	if g.name==group_name:
           responses = Response.objects.filter(contact__groups__name=group_name,poll__pk=poll_id)   
	   dict_to_render.update({'tagged': True,
                               'tags': _get_tags1(group_name,polls),
                   'responses':  responses,
                    'poll_id': poll.pk,
                    })
       	#else:   	
            #raise Http404 
    #if poll.type == Poll.TYPE_TEXT and not  poll.categories.exists():
    
        
    return render_to_response('ureport/partials/viz/best_visualization.html'
                              , dict_to_render,
                              context_instance=RequestContext(request))

