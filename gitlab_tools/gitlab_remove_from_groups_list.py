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
Removes the logged in user from any groups he/she is a member of whose name end with a given suffix.
This is useful for removing yourself or another instructor from student personal groups after the semester is over.
Usage:
./gitlab_remove_from_groups.py (token) (suffix) <--member (id)> <--gitlab_url address_of_server>
E.g. To remove yourself from all groups ending with the suffix 'cs1' run
./gitlab_remove_from_groups.py notmytoken cs1
"""
import argparse
import sys

from gitlab_utils import gl_auth

parser = argparse.ArgumentParser()

parser.add_argument('token', help='Your private access token from Gitlab')
parser.add_argument('group_list', help='Text file containing list of groups to remove user from')
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
            users = gl.users.get(search=args.user_name)
            gl_ins = users[0]
        except Exception as e:
            print("Failed to find specified user :",args.user_name)
            sys.exit(-1)

    print(" Removing ",gl_ins.username," from groups ...")
    with open(args.group_list,"rt") as fin:
        groups = [name.strip() for name in fin.readlines()]
        for ndx, gp_name in enumerate(groups):
            try:
                gl_gp = gl.groups.get(gp_name)
                for gl_mem in gl_gp.members.list(as_list=False):
                    if gl_mem.id == gl_ins.id:
                        try:
                            gl_mem.delete()
                            print("Removed ",gl_ins.username," from ",gl_gp.name,"  ",ndx+1," of ",len(groups))
                        except Exception as e:
                            print("Failed to remove ",gl_ins.username," from ",gl_gp.name,"  ",ndx+1," of ",len(groups))
            except Exception as e:
                    print("Could not find group ",gp_name,"  ",ndx+1," of ",len(groups))
    print("Done!")
