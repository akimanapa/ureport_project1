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




def view_scout_result(request,poll):
    responses = Response.objects.filter(contact_groups_name='SCOUT', pk=poll)
    return render_to_response('polls/scout_result.html', {'responses': responses,})
    
def view_guide_result(request,poll):
    responses = Response.objects.filter(contact_groups_name='GUIDE', pk=poll)
    return render_to_response('polls/scout_result.html', {'responses': responses,}) 
    
def view_redcross_result(request,poll):
    responses = Response.objects.filter(contact_groups_name='redcross', pk=poll)
    return render_to_response('polls/scout_result.html', {'responses': responses,})       
    
