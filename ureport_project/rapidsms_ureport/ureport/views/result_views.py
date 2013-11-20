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
from ureport.utils import retrieve_poll
from ureport.views.utils.tags import _get_tags, _get_responses
from django.http import HttpResponse, Http404



def view_result(request,group_name,poll_id):
	
    module = False
    response=Response.objects.filter(pk=poll_id)
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
        
        #'response':response,
        'poll': poll,
        'polls': [poll],
        'unlabeled': True,
        'module': module,
        'rate': int(rate),
        }
    
   # if poll.type == Poll.TYPE_TEXT and not  poll.categories.exists():
    dict_to_render.update({'tagged': True,
                               'tags': _get_tags(polls),
                   'responses': _get_responses(poll),
                    'poll_id': poll.pk,
                    })
	
    return render_to_response('ureport/poll_results.html'
                              , dict_to_render,
                              context_instance=RequestContext(request))
	
	
	
	
        


    
