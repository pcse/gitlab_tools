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

# Author: David Conner

"""
Lists all groups in a given Gitlab server by permission, and
writes to 3 files: public_groups.txt, internal_groups.txt, private_groups.txt

"""
import argparse

import gitlab_utils
import gitlab

visibility=['private','internal','public']
visibility_levels={visibility[0]:0,visibility[1]:1, visibility[2]:2  }

def lower_visibility_level(gl, gl_group, target_visibility):
    """ Lower group visibility level.
    Requires all member projects to have lower visibility as well
    """

    projects = gl_group.projects.list()
    target_level = visibility_levels[target_visibility]
    print("Set group visibility for ",gl_group.name," from ", gl_group.visibility, " to ",target_visibility)
    for project in projects:
        #print("Project:\n",project)
        try:
            manageable_project = gl.projects.get(project.id, lazy=True)
            #print("Project:\n",manageable_project)
            current_level = visibility_levels[project.visibility]
            if current_level > target_level:
                print("   Lowering project visibility for ",project.name," from ",project.visibility, " to ",target_visibility)
                manageable_project.visibility = target_visibility
                manageable_project.save()
        except Exception as e:
            print("   Failed to lower project visibility for ",project.name," from ",project.visibility, " to ",target_visibility)
            print(e)

    gitlab_utils.gl_set_visibility(gl_group, target_visibility)
    print("------")


parser = argparse.ArgumentParser()

parser.add_argument('token', help='Your private access token from Gitlab')
parser.add_argument('group_list_file', help='File listing group names')
parser.add_argument('target_visibility', default='private', help="Target visibility ('public','internal','private')")
parser.add_argument('--gitlab_url', default='https://gitlab.pcs.cnu.edu', help='The url for the Gitlab server.')

args = parser.parse_args()

url = args.gitlab_url
token = args.token
group_list = args.group_list_file
target_visibility = args.target_visibility
target_level = visibility_levels[target_visibility]

private=[]
internal=[]
public=[]

print("Access gitlab ...")
with gitlab_utils.gl_auth(url, token, admin=True) as gl:

    with open(group_list,'rt') as fin:
        groups = fin.readlines()

        for group_name in groups:
            group_name = group_name.strip()
            try:
                gl_group = gitlab_utils.gl_get_group_by_name(gl, group_name)
                print(" Found group ", group_name)

                current_visibility = gl_group.visibility
                if current_visibility != target_visibility:
                    current_level = visibility_levels[current_visibility]
                    if current_level < target_level:
                        # Just set the visibility level of group and level projects alone
                        gitlab_utils.gl_set_visibility(gl_group, target_visibility)
                    else:
                        lower_visibility_level(gl, gl_group, target_visibility)

            # If we can't find it, make it.
            except gitlab.exceptions.GitlabHttpError as e:
                print("Failed to access gitlab to get group ", group_name)
                raise e
            except gitlab.exceptions.GitlabGetError as e:
                print("Failed to find group ",group_name)

print("Done!")
