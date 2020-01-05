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

# Author: David Conner, based on work by Matthew McCarthy
"""
Removes the logged in user from a list of projects that he/she is a member of .
This is useful for removing yourself or another instructor from student personal groups after the semester is over.
Usage:
./gitlab_remove_from_projects_list.py (token) (project_list) <--user_name (id)> <--gitlab_url address_of_server>
E.g. To remove yourself from all projects listed in file project_membership.txt run
./gitlab_remove_from_groups_list.py notmytoken project_membership.txt

The project_membership.txt file has structure of tab delimited csv file with:
project_id  project_url
on each line.  (Only the project_id is used by this script.)

"""
import argparse
import sys
import csv
from gitlab_utils import gl_auth

parser = argparse.ArgumentParser()

parser.add_argument('token', help='Your private access token from Gitlab')
parser.add_argument('project_list', help='Text file containing list of groups to remove user from')
parser.add_argument('--user_name', default='', help='The Gitlab username')
parser.add_argument('--gitlab_url', default='https://gitlab.pcs.cnu.edu', help='The url for the Gitlab server.')

args = parser.parse_args()

url = args.gitlab_url
token = args.token
gl_ins = None
with gl_auth(url, token, admin=True) as gl:
    if args.user_name == '':
        gl_ins = gl.users.get(gl.user.id)
    else:
        try:
            users = gl.users.list(search=args.user_name)
            if len(users) != 1:
                print("users: ",users)
                raise Exception("Invalid user name (%s)!"%(args.user_name))
            gl_ins = users[0]
        except Exception as e:
            print("Failed to find specified user :",args.user_name)
            sys.exit(-1)

    print(" Removing ",gl_ins.username," from projects ...")
    with open(args.project_list,"rt") as fin:
        csv_reader = csv.reader(fin, delimiter="\t")
        for data in csv_reader:
            project_id = int(data[0])
            project_url = data[1]

            try:
                gl_project = gl.projects.get(project_id)
                try:
                    gl_project.members.delete(gl_ins.id)
                    print("Removed ",gl_ins.username," from ",gl_project.name)
                except Exception as e:
                    print("Failed to remove ",gl_ins.username," from ",gl_project.name, " ", project_id)
            except Exception as e:
                    print("Could not find project ", project_id, " ", gl_project.name )
    print("Done!")
