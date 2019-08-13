#!/usr/bin/python3
# Copyright (c) 2019
# Physics, Computer Science and Engineering (PCSE)
# Christopher Newport University
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   1. Redistributions of source code must retain the above copyright notice,
#      this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#   3. Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
#      THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#      "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#      LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#      FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#      COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#      INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#      BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#      LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#      CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#      LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
#      WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#      POSSIBILITY OF SUCH DAMAGE.

# Author: Matthew McCarthy

from gitlab_utils import gl_auth, gl_create_project, gl_get_all_owned_projects, gl_find_project_in_list

import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument('--gitlab_url', default='https://gitlab.pcs.cnu.edu', help='The url for the Gitlab server.')
parser.add_argument('token', help='Your private access token from Gitlab')
parser.add_argument('--group', default='', help='The group to create the project in')
parser.add_argument('project_name', help='The name of the project to create')

args = parser.parse_args()

# Authenticate
with gl_auth(args.gitlab_url, args.token) as gl:
    project_name = args.project_name
    group_name = args.group

    gl_target_group = None
    project_list = None
    if group_name != '':
        gl_target_group = gl.groups.get(group_name)
        if gl_target_group is None:
            sys.exit('Group {} not found'.format(group_name))
        project_list = gl_target_group.projects.list(all=True)
    else:
        project_list = gl_get_all_owned_projects(gl)

    if gl_find_project_in_list(project_name, project_list) is None:
        gl_create_project(gl, project_name, gl_target_group)
    else:
        sys.exit(
            'Project {} exists in namespace {}'.format(project_name,
                                                       group_name if group_name != '' else gl.user.username)
        )
