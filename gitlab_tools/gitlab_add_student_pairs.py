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

from gitlab_utils import gl_auth
import gitlab_utils

import argparse
import gitlab
import sys
import datetime
import csv

class Student:
    def __init__(self, email_line):
        student_info = email_line.split('@')
        self.email_line = email_line.strip()
        student_name = student_info[0].split('.')
        self.username = student_info[0].strip()
        self.first_name = student_name[0].strip()
        self.last_name = student_name[1].strip()
        self.year      = student_name[2].strip()

    def get_email(self):
        return self.email_line

    def get_last_name(self):
        return self.last_name

    def get_first_name(self):
        return self.first_name

    def get_input(self):
        return self.email_line

    def mk_gl_username(self):
        return self.username

    def __str__(self):
        return '{}, {} ({}): {}'.format(self.last_name, self.first_name, self.year, self.email_line)

    def __repr__(self):
        return self.__str__()


today = datetime.datetime.now()
delta = datetime.timedelta(7) # 1 week in future
expire = today+delta

parser = argparse.ArgumentParser()

parser.add_argument('token', help='Your private access token from Gitlab')
parser.add_argument('email_input',   help='A text file with 2 columns of CNU email (project owner, review partner)')
parser.add_argument('group_suffix',  help='Group suffix of owner')
parser.add_argument('project_name',  help='The project to add reviewer to')
parser.add_argument('--expire', default=expire.isoformat()[:10],
                    help='The date that you want to be removed from all of these groups. Format: yyyy-mm-dd.  Default 5 months from today.')
parser.add_argument('--gitlab_url', default='https://gitlab.pcs.cnu.edu', help='The url for the Gitlab server.')

args = parser.parse_args()
group_suffix = "-"+args.group_suffix # assumes user_name-suffix format
project_name = args.project_name
expire_date = args.expire

print("  expiration date:"+expire_date )

print( "Args:"+str(args))

# Authenticate
try:
  with gl_auth(args.gitlab_url, args.token, admin=True) as gl:
    admin_id = gl.user.id
    admin_name = gl.users.get(gl.user.id).username
    print(" admin name: "+admin_name)


    # If we found or made the student group
    if True:
        # Get the instructor's account
        current_user = gl.user
        # Construct list of students
        student_list = []
        with open(args.email_input,'rt') as csv_in:
            main_reader = csv.reader(csv_in,delimiter='\t')
            print( "got main reader ...")
            for row in main_reader:
                if not row[0].startswith('#') and len(row)==2:
                    student_list.append((Student(row[0]), Student(row[1])))
                else:
                    print(" Ignoring "+row)

    if (len(student_list) > 0):
        # Get a list of all users from GL instance. SLOW.
        # There does exist a better way to do this though.
        print(" Retrieve master list from Gitlab ... (slow ...)")
        all_user_list = list(gl.users.list(as_list=False))
        print("all users:"+str(len(all_user_list)))
        #for gl_user in all_user_list:
        #    print("  user "+gl_user.username+"  email("+gl_user.email+")")

        # Find existing users
        # Add existing users to student group and create their personal group
        gl_instructor = None
        gl_existing_users = {}
        bad_account = []
        bad_group = []
        bad_add = []

        print("Begin processing student pairs ...")
        for students in student_list:
          for student in students:
            for gl_user in all_user_list:
                if gl_user.email == student.get_email():
                    print(" found existing user "+gl_user.email)
                    gl_existing_users[student.get_email()] = gl_user
                    break

            if student.get_email() not in gl_existing_users.keys():
                print("Unknown student "+student.get_email())
                bad_account.append(student.get_email())
                print("  existing keys: "+str(gl_existing_users.keys()))
                print("all users:"+str(len(all_user_list)))
                for gl_user in all_user_list:
                    print("  user "+gl_user.username+"  email("+gl_user.email+")"+ str(gl_user.email == student.get_email())+" "+student.get_email())
                print("----------------------")
                sys.stdout.flush()
                sys.exit(-1)

        student = None
        # Set up accounts
        for students in student_list:
            owner = students[0]
            reviewer = students[1]

            gl_owner = None
            gl_reviewer = None
            try:
                gl_owner = gl_existing_users[owner.get_email()]
                gl_reviewer = gl_existing_users[reviewer.get_email()]
            except Exception as ex:
                print("Could not get GitLab reference for owner or reviewer")
                print(ex)

            if (gl_owner is None or gl_reviewer is None):
                print(" Invalid pairing "+str(students))
            else:
                try:
                    print(" Trying to find project for {} ...".format(owner.mk_gl_username()))
                    gl_target_group = gl.groups.get(owner.mk_gl_username()+group_suffix)
                    if gl_target_group is None:
                        sys.exit('Group {} not found'.format(group_name))
                    owner_projects = gl_target_group.projects.list(all=True)

                    #print("Get the project object ...")
                    project = gitlab_utils.gl_find_project_in_list(project_name, owner_projects)
                    gl_project = gl.projects.get(project.id)
                    print("  Got the "+project_name+" project for "+owner.mk_gl_username())

                    try:
                        print(" Adding "+reviewer.mk_gl_username()+" to project ...")
                        member = gitlab_utils.gl_add_user_group_project(gl_project, gl_reviewer, gitlab.REPORTER_ACCESS)
                        member.expires_at = expire_date
                        member.save()

                    except Exception as ex:
                        print('Could not add {} to {} project '.format(reviewer.mk_gl_username(), owner.mk_gl_username()))
                        print("   "+str(ex))
                        bad_add.append((owner.mk_gl_username(), reviewer.mk_gl_username()))

                except Exception as ex2:
                        print('Could not find {} project {}'.format(owner.mk_gl_username(), project_name))
                        print("   "+str(ex2))
                        print("--------------------")
                        print(str(gl_owner))
                        print("--------------------")
                        bad_add.append((owner.mk_gl_username(), reviewer.mk_gl_username()))


        # Print the cases where there is an account creation error
        print("Finished processing students ... ")
        if len(bad_account) > 0:
            print('Missing Accounts:')
            for student in bad_account:
                print(student)
        # Print the cases where we could not add the student to the group
        if len(bad_add) > 0:
            print('Could not add:')
            for student in bad_add:
                print(student)
        # Print the cases where there is an account creation error
        if len(bad_group) > 0:
            print('Missing Groups:')
            for student in bad_group:
                print(student)
        print("done!")

    else:
        print('I couldn\'t find any students to process  ' + student_group_name)
        sys.exit(1)
except Exception as ex:
    print(ex)
