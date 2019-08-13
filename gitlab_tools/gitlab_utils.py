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
A slightly better documented wrapper around the current python wrapper for the Gitlab API.
Variables that start with 'gl' are associated with the python-gitlab module, all others are not.
Author: Matt McCarthy
"""
from contextlib import contextmanager

import gitlab
import sys

class GitlabLoginException(Exception):
    def __init__(self, value):
        self.value = value
        print("Exception: "+value)

    def __str__(self):
        return repr(self.value)

    def __repr__(self):
        return str(self)


# Authenticate a user on a Gitlab instance
@contextmanager
def gl_auth(gitlab_url, token, admin=False):
    """
    Authenticates and opens a Gitlab instance
    :param gitlab_url: The URL of a Gitlab server
    :param token: Your Private Access Token
    :param admin: True if you want to use your admin privileges. False otherwise.
    :return: An authenticated Gitlab instance if no exception thrown.
    """
    # Create a login instance
    print("Create Gitlab instance to {} ... ".format(gitlab_url))
    sys.stdout.flush()
    gl = gitlab.Gitlab(gitlab_url, token.strip(),api_version='4')

    # Authenticate
    print("Attempt to authenticate ... " )
    sys.stdout.flush()
    try:
        gl.auth()
    except Exception as ex:
        print("Failed to authenticate with token "+token)
        sys.stdout.flush()
        raise GitlabLoginException('Token invalid')

    print("  authenticated!")
    sys.stdout.flush()
    if gl_instance_logged_in(gl):
        if admin:
            if gl_instance_admin(gl):
                yield gl
            else:
                print("Failed to log in with token "+token+" because user does not have admin privileges")
                sys.stdout.flush()
                raise GitlabLoginException('User not an admin')
        else:
            yield gl
    else:
        print("Failed to log in with token "+token)
        sys.stdout.flush()
        raise GitlabLoginException('Token invalid')


def gl_instance_logged_in(gl):
    """
    Checks if a Gitlab instance is logged in.
    :param gl: A Gitlab object
    :return: True if logged in, False otherwise
    """
    return hasattr(gl, 'user')


def gl_instance_admin(gl):
    """
    Checks if the Gitlab instance exposes admin privileges.
    :param gl: A Gitlab object.
    :return: True if admin, False otherwise.
    """
    return gl.user.is_admin


def gl_get_all_users(gl):
    """
    Gets a list of all users on this Gitlab instance.
    :param gl: A Gitlab object that is logged on (check gl_instance_logged_in first).
    :return: A list of all users on this Gitlab server.
    """
    return gl.users.list(all=True)  # Using all=True is bad, but I'm not familiar enough with python to know better.


def gl_get_all_owned_projects(gl):
    """
    Gets a list of all projects that you have access to.
    :param gl: A Gitlab object that is logged on (check gl_instance_logged_in first).
    :return: A list of all projects that you have access to.
    """
    return gl.users.get(gl.user.id).projects.list(all=True)
    # Using all=True is bad, but I'm not familiar enough with python to know better.


def gl_get_group_by_name(gl, group_name):
    """
    Searches this Gitlab instance for a group with a given name.
    :param gl: A Gitlab object that is logged on (check gl_instance_logged_in first).
    :param group_name: The group name to find.
    :return: The group that has the given name.
    """
    return gl.groups.get(group_name)


def gl_find_user_by_email(gl, email, gl_user_list=None):
    """
    Searches a list of users for one with a given email.
    :param gl: A Gitlab object that is logged on (check gl_instance_logged_in first). Must have admin rights!!!
    :param email: The email address to search for.
    :param gl_user_list: The list of Gitlab users to search through. If not specified, gets a list of ALL users.
    :return: A gitlab.User object that has the given email.
    """
    if not gl_instance_admin(gl):
        raise GitlabLoginException('User not an admin')
    if gl_user_list is None:
        gl_user_list = gl_get_all_users(gl)
    for gl_user in gl_user_list:
        if gl_user.email == email:
            return gl_user
    return None


def gl_find_project_in_list(project_name, gl_project_list):
    """
    Finds a project with a given name in a list of gitlab.Project objects.
    :param project_name: The project name to find.
    :param gl_project_list: The list of Project objects to search.
    :return: A handle to the first Project with the desired name.
    """
    for gl_project in gl_project_list:
        if gl_project.name == project_name.strip():
            return gl_project
    return None


def gl_create_group(gl, group_name, visibility='private'):
    """
    Creates a group on a GitLab instance with a desired visibility. May throw an exception (e.g. if it already exists).
    :param gl: GitLab instance
    :param group_name: Name of the group you wise to
    :param visibility: The visibility of the group, valid options are 'private', 'internal', and 'public'. Default: 'private'
    :return: A handle to the newly create group
    """
    return gl.groups.create({'name': group_name, 'path': group_name, 'visibility': visibility})


def gl_create_project(gl, project_name, gl_group=None):
    """
    Creates a project on a GitLab instance. May throw an exception (e.g. if it already exists in the given namespace).
    :param gl: GitLab instance
    :param project_name: The name of the project to make
    :param gl_group: The group to create it in (if not set or set to None, makes the project in the user's namespace)
    :return: A handle to the newly create project
    """
    return gl.projects.create(
        {'name': project_name} if gl_group is None
        else {'name': project_name, 'namespace_id': gl_group.id}
    )


def gl_create_user(gl, email, password, username, last_name, first_name):
    """
    Creates a user on a GitLab instance. May throw an exception (e.g. if it already exists).
    :param gl: GitLab instance
    :param email: The user's email address
    :param password: The user's default password
    :param username: The user's username
    :param last_name: The user's last name
    :param first_name: The user's first name
    :return: A handle to the newly created user
    """
    return gl.users.create({
                        'email': email,
                        'password': password,
                        'username': username,
                        'name': first_name + ' ' + last_name
                    })


def gl_add_user_group_project(gl_project_group, gl_user, gl_access_level):
    """
    Adds a Gitlab user to a Gitlab project or group at the given access level
    :param gl_project_group: A Project or Group object
    :param gl_user: A User instance
    :param gl_access_level: A gitlab.Access_Level. Can be gitlab.GUEST_ACCESS, gitlab.REPORTER_ACCESS,
                gitlab.DEVELOPER_ACCESS, gitlab.MASTER_ACCESS, or gitlab.OWNER_ACCESS (group only).
    :return: A handle to the member instance. Use this to adjust properties of the member.
    """
    return gl_project_group.members.create({
        'user_id': gl_user.id,
        'access_level': gl_access_level

    })

def gl_set_visibility(gl_project_group, gl_visibility_level):
    """
    Sets the visibility for a Gitlab project or group
    :param gl_project_group: A Project or Group object
    :param visibility ('public','internal','private')
    """
    gl_project_group.visibility = gl_visibility_level
    gl_project_group.save()

def gl_get_group_membership(gl, user_id):
    """
    Get a list of all groups where user_id is a member
    :param gl: GitLab instance
    :param user_id: user id (not username!) this field is (gitlab User object).id
    """
    groups=[]
    for gl_gp in gl.groups.list(as_list=False):
        for gl_mem in gl_gp.members.list(as_list=False):
            if gl_mem.id == user_id:
                groups.append(gl_gp)
                break # No need to check additional members
    return groups
