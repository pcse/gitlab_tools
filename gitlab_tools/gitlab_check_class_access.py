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
"""
Determines if any student in a roster shared their Gitlab group (or a specified repository) with another user.
If it detects illegal sharing, this script will print '(sharer) gave (sharee) access to (url): (time detected)'.
This script also takes a list of user names that are allowed to have access to all repositories/groups for the class.
I require admin privileges on the Gitlab instance here (for safety), but if the instructor has access to everything,
it should (probably maybe) work.
Usage:
./gitlab_check_class_access.py (token) (csv roster) (list of ignored users) (repo) [--interval time b/t checks, default 60]

E.g. If I wanted to check the cpsc150-mt1 repo for all groups in my roster.txt file while ignoring users in ignore.txt.
./gitlab_check_class_access.py thisisnotmytoken roster.txt ignore.txt cpsc150-mt1
This will check all groups listed in the roster.txt file and the cpsc150-mt1 repository in each of those groups.
Since instructors should have access to their student's work, the instructor user name (and maybe lab TA user name)
would be in the ignore.txt.

Roster format:
user1,group1
user2,group2

Ignore list format:
user1
user2
"""
import time

from gitlab_utils import gl_auth

import argparse
import datetime


def check_members(gl_thing, ignore_these, owner_name):
    for gl_member in gl_thing.members.list(all=True):
        if gl_member.username != owner_name and gl_member.username not in ignore_these:
            print("{} gave {} access to {}: {}".format(owner_name, gl_member.username, gl_thing.web_url,
                                                                    datetime.datetime.now()))


parser = argparse.ArgumentParser()

parser.add_argument('--gitlab_url', default='https://gitlab.pcs.cnu.edu', help='The url for the Gitlab server.')
parser.add_argument('token', help='Your private access token from Gitlab')
parser.add_argument('csv_roster',
                    help='A csv file whose 1st column is username, ' +
                         'and 2nd column is group name')
parser.add_argument('ignore_list', help='A list of users who are allowed access to student groups/projects')
parser.add_argument('repo_name', help='The repo to check.')
parser.add_argument('--interval', type=int, default=60, help='The time to wait between checks.')

args = parser.parse_args()

with gl_auth(args.gitlab_url, args.token, admin=True) as gl:
    # Get the ignored usernames
    ignore_us = []
    with open(args.ignore_list) as ignore_list_f:
        for line in ignore_list_f:
            ignore_us.append(line.strip())
    # Go through the roster
    user_names = []
    group_names = {}
    gl_gp_ids = {}
    gl_repo_ids = {}
    with open(args.csv_roster) as roster_f:
        for line in roster_f:
            # Line formatted "username,groupname"
            split_line = line.strip().split(',')
            username = split_line[0]
            group_name = split_line[1]
            # Check if the group is currently shared
            gl_group = gl.groups.get(group_name)
            check_members(gl_group, ignore_us, username)
            # Get the repo
            gl_repo = None
            for gl_gp_repo in gl_group.projects.list(all=True):
                if gl_gp_repo.name == args.repo_name:
                    gl_repo = gl.projects.get(gl_gp_repo.id)
                    break
            # If the repo exists, check if it is shared.
            if gl_repo is not None:
                check_members(gl_repo, ignore_us, username)

            # fill out list of users and dictionaries so we don't have to find them later
            user_names.append(username)
            group_names[username] = group_name
            gl_gp_ids[username] = gl_group.id
            gl_repo_ids[username] = gl_repo.id if gl_repo is not None else -1

    # Check the repos and groups until the user kills the program
    check_interval = args.interval
    while True:
        start_time = time.time()
        for username in user_names:
            # Get the group and get the project if it exists
            gl_group = gl.groups.get(gl_gp_ids[username])
            gl_repo = gl.projects.get(gl_repo_ids[username]) if gl_repo_ids[username] != -1 else None
            # If we haven't seen the project yet, check if it exists
            if gl_repo is None:
                for gl_gp_repo in gl_group.projects.list(all=True):
                    if gl_gp_repo.name == args.repo_name:
                        gl_repo = gl.projects.get(gl_gp_repo.id)
                        break
                if gl_repo is not None:
                    gl_repo_ids[username] = gl_repo.id
            # Check the members of group and repo
            check_members(gl_group, ignore_us, username)
            if gl_repo is not None:
                check_members(gl_repo, ignore_us, username)
        # Wait a little bit
        finish_time = time.time()
        if finish_time - start_time < check_interval:
            time.sleep(check_interval - (finish_time - start_time))
