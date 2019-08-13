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
Writes a file containing list of all groups that user_name (or admin) is a member of
Usage:
./gitlab_check_group_membership.py (token) <--user_name user_name> <--gitlab_url address_of_server>
Without specifying the user name, the script checks membership of the administrator running the scripts

"""
import argparse

from gitlab_utils import gl_auth, gl_get_group_membership

parser = argparse.ArgumentParser()

parser.add_argument('token', help='Your private access token from Gitlab')
parser.add_argument('--user_name', default='', help='The Gitlab username of the instructor')
parser.add_argument('--gitlab_url', default='https://gitlab.pcs.cnu.edu', help='The url for the Gitlab server.')

args = parser.parse_args()

url = args.gitlab_url
token = args.token
user = None

with gl_auth(url, token, admin=True) as gl:
    if args.user_name == '':
        user = gl.users.get(gl.user.id)
    else:
        users = gl.users.list(search=args.user_name)
        if len(users) != 1:
            print("users: ",users)
            raise Exception("Invalid user name (%s)!"%(args.user_name)))
        user=users[0] #

    print(" Get list of all groups that ",user.username," belongs to ...")

    groups = gl_get_group_membership(gl, user.id)

    print(" Write files ...")
    with open('group_membership_'+user.username+'.txt',"wt") as fout:
        fout.write('\n'.join([gp.full_path for gp in groups]))
