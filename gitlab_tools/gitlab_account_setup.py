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
        return '{}, {} ({}): {}'.format(self.last_name, self.first_name, self.year, self.email)

    def __repr__(self):
        return self.__str__()


today = datetime.datetime.now()
delta = datetime.timedelta(5*365/12) # 5 months in future
expire = today+delta

parser = argparse.ArgumentParser()

parser.add_argument('token', help='Your private access token from Gitlab')
parser.add_argument('email_input',   help='A text file with 1 column of email address')
parser.add_argument('master_student_group', help='The student group on Gitlab to add all students to')
parser.add_argument('--personal_group_suffix', default='', help='The suffix to append to all student personal groups (default: no personal group)')
parser.add_argument('--expire', default=expire.isoformat()[:10],
                    help='The date that you want to be removed from all of these groups. Format: yyyy-mm-dd.  Default 5 months from today.')
parser.add_argument('--instructor', default='', help='The Gitlab username of the instructor')
parser.add_argument('--delete_admin', default=False, help='Remove the admin from created groups (default:False)')
parser.add_argument('--gitlab_url', default='https://gitlab.pcs.cnu.edu', help='The url for the Gitlab server.')

args = parser.parse_args()

user_is_instructor = (args.instructor == '')
delete_admin = False
student_group_name = args.master_student_group
personal_group_suffix = args.personal_group_suffix
expire_date = args.expire

print("  expiration date:"+expire_date )

print( "Args:"+str(args))

# Authenticate
try:
  with gl_auth(args.gitlab_url, args.token, admin=True) as gl:
    instructor_name = args.instructor if not user_is_instructor else gl.users.get(gl.user.id).username
    print("instructor name: "+instructor_name)
    admin_id = gl.user.id
    admin_name = gl.users.get(gl.user.id).username
    print(" admin name: "+admin_name)
    if instructor_name == admin_name:
        print(" API user is both admin and instructor ")
        user_is_instructor = True
        delete_admin = False
    else:
        try:
            tmp_del_admin = args.delete_admin
            if type(tmp_del_admin) == str:
                tmp_del_admin = tmp_del_admin.lower() in ["yes","true","t",1]
            elif type(tmp_del_admin) != bool:
                tmp_del_admin = False

            if (tmp_del_admin):
                print("Delete the admin from any created groups")
                delete_admin = True
        except:
            print("Do not delete admin from created groups!")

    # Find master student group (e.g. cpsc150-students-s2018)
    gl_student_group = None
    try:
        gl_student_group = gitlab_utils.gl_get_group_by_name(gl, student_group_name)
        print(" Found existing student group "+student_group_name)
    # If we can't find it, make it.
    except gitlab.exceptions.GitlabHttpError as e:
        print(" Create the new student group "+student_group_name)
        gl_student_group = gitlab_utils.gl_create_group(gl, student_group_name)
    except gitlab.exceptions.GitlabGetError as e:
        print(" Create the new student group "+student_group_name)
        gl_student_group = gitlab_utils.gl_create_group(gl, student_group_name)

    # If we found or made the student group
    if gl_student_group:
        # Get the admin's account
        current_user = gl.user
        # Get list of members of student group (possibly slow, depending on size of group)
        master_group_members = gl_student_group.members.list(as_list=False)
        # Construct list of students
        student_list = []
        with open(args.email_input) as csv_in:
            for line in csv_in:
                if not line.startswith('#'):
                    student_list.append(Student(line))
        # Get a list of all users from GL instance. SLOW.
        # There does exist a better way to do this though, I think.
        print(" Retrieve master list from Gitlab ... (slow ...)")
        all_user_list = gl.users.list(as_list=False)
        # Find existing users
        # Add existing users to student group and create their personal group
        gl_instructor = None
        gl_existing_users = {}
        bad_account = []
        bad_group = []
        bad_add = []
        for gl_user in all_user_list:
            if gl_user.username == instructor_name:
                gl_instructor = gl_user
            for student in student_list:
                if gl_user.email == student.get_email():
                    gl_existing_users[student.get_email()] = gl_user


        if not user_is_instructor:
            # Add instructor as owner
            print("  Adding instructor "+gl_instructor.username+" as owner of student group ...")
            try:
                gl_instructor_member = gitlab_utils.gl_add_user_group_project(gl_student_group,
                                                                              gl_instructor,
                                                                              gitlab.OWNER_ACCESS)
                gl_instructor_member.save()
            except gitlab.exceptions.GitlabCreateError as ex:
                print("  GitlabCreateError: Could not add instructor as owner of student group ... " + str(ex))

            except Exception as ex:
                print("  Exception: Could not add instructor as owner of student group ... " + str(ex))


            if (delete_admin):
                # Remove admin
                print("Removing admin "+admin_name+" from student group ...")
                try:
                    gl_student_group.members.get(admin_id).delete()
                except Exception as ex:
                    print("Could not remove api user as admin from the student group ... "+str(ex))

        # Set up accounts
        for student in student_list:
            gl_user = None
            print(student.get_email())
            # If the user exists, grab its GL handle
            if student.get_email() in gl_existing_users.keys():
                print("     Found existing user "+student.mk_gl_username()+"!")
                gl_user = gl_existing_users[student.get_email()]
            # Otherwise, create missing user
            else:
                gl_user = None
                try:
                    # Use email as email, the prescribed username as password and username
                    print(" Create new user "+student.mk_gl_username()+" to group ...")
                    gl_user = gitlab_utils.gl_create_user(gl, student.get_email(), student.mk_gl_username(),
                                                          student.mk_gl_username(), student.get_last_name(),
                                                          student.get_first_name())
                except Exception as e:
                    print('Could not create account for email {}'.format(student.get_email()))
                    bad_account.append(student.get_email())

            # If we found the user or created the user
            if gl_user is not None:
                # Check if student is in student group
                in_student_group = False
                for group_member in master_group_members:
                    if group_member.id == gl_user.id:
                        print("     user already in student group!")
                        in_student_group = True
                        break

                # Add user to student group, if not already in it
                if not in_student_group:
                    try:
                        print("     Adding "+student.mk_gl_username()+" to group")
                        member = gitlab_utils.gl_add_user_group_project(gl_student_group, gl_user, gitlab.REPORTER_ACCESS)
                        member.expires_at = expire_date
                        member.save()

                    except Exception as ex:
                        print('     Could not add {} to student group'.format(student.get_email())+"   "+str(ex))
                        bad_add.append(student.get_email())

                # Check if the student's personal group exists
                if (len(personal_group_suffix) == 0):
                    pass
                else:
                    personal_group_name = student.mk_gl_username() + '-' + personal_group_suffix
                    personal_group_exists = False
                    gl_personal_group = None
                    try:
                        gl_personal_group = gitlab_utils.gl_get_group_by_name(gl, personal_group_name)
                        personal_group_exists = True
                    except gitlab.exceptions.GitlabHttpError as e:
                        personal_group_exists = False
                    except Exception as ex:
                        print("     Exception searching for "+personal_group_name+"   " + str(ex))
                        personal_group_exists = False

                    # if it does not exist
                    if not personal_group_exists:
                        # Create student personal group
                        print("     Create personal group "+personal_group_name)
                        try:
                            gl_personal_group = gitlab_utils.gl_create_group(gl, personal_group_name)
                            if gl_personal_group is not None:
                                print("           now add student to group ...")
                                gitlab_utils.gl_add_user_group_project(gl_personal_group, gl_user, gitlab.OWNER_ACCESS)
                                print("           set as private access ...")
                                gl_personal_group.visibility = "private"
                                gl_personal_group.save()
                            else:
                                print('           Could not create personal group for email {}'.format(student.get_email()))
                                bad_group.append(student.get_email())

                        except Exception as e:
                            print('      Exception creating personal group for email {}'.format(student.get_email()),"    ", str(e))
                            bad_group.append(student.get_email())

                    # If we successfully created the student's personal group
                    if gl_personal_group is not None:
                        try:
                          if user_is_instructor:
                            # Demote instructor to reporter
                            try:
                                gl_instructor_member = gl_personal_group.members.get(admin_id)
                                if gl_instructor_member is not None:
                                    print("      Demoting admin "+admin_name+" to reporter access ...")
                                    gl_instructor_member.access_level = gitlab.REPORTER_ACCESS
                                    gl_instructor_member.expires_at = expire_date
                                    gl_instructor_member.save()
                            except Exception as ex:
                                print("      group not created by this admin - cannot demote to reporter! "+str(ex))
                                try:
                                    print("      add admin as reporter to existing group")
                                    gl_instructor_member = gitlab_utils.gl_add_user_group_project(gl_personal_group,
                                                                                                  gl_instructor,
                                                                                                  gitlab.REPORTER_ACCESS)
                                    print("      Set the expiration date ...")
                                    gl_instructor_member.expires_at = expire_date
                                    gl_instructor_member.save()
                                except gitlab.exceptions.GitlabCreateError as ex:
                                    print("      GitlabCreateError: Could not add admin as reporter ... "+str(ex))
                                except Exception as ex:
                                    print("      Exception: Could not add admin as reporter ... "+str(ex))
                          else:
                            # Add instructor as reporter
                            print("     Adding instructor "+gl_instructor.username+" as reporter ...")
                            try:
                                gl_instructor_member = gitlab_utils.gl_add_user_group_project(gl_personal_group,
                                                                                              gl_instructor,
                                                                                              gitlab.REPORTER_ACCESS)

                                # Set expiration date
                                print("      Set the expiration date ...")
                                gl_instructor_member.expires_at = expire_date
                                gl_instructor_member.save()
                            except gitlab.exceptions.GitlabCreateError as ex:
                                print("      GitlabCreateError: Could not add instructor as reporter ... "+str(ex))
                            except Exception as ex:
                                print("      Exception: Could not add instructor as reporter ... "+str(ex))

                            if (delete_admin):
                                # Remove admin
                                print("     Removing admin "+admin_name+" from personal group ...")
                                try:
                                    gl_personal_group.members.get(admin_id).delete()
                                except Exception as ex:
                                    print("      Could not remove api user as admin ... "+str(ex))

                        except Exception as ex:
                            print("Failed instructor handling in personal group ... "+str(ex))

                    if gl_personal_group is None:
                        print("     Failed to access the personal group "+personal_group_name)

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
        # Print the cases where there is an group creation error
        if len(bad_group) > 0:
            print('Missing Groups:')
            for student in bad_group:
                print(student)
        print("done!")

    else:
        print('I couldn\'t find nor make the group ' + student_group_name)
        sys.exit(1)
except Exception as ex:
    print(ex)
