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
Lists all groups in a given Gitlab server by permission, and
writes to 3 files: public_groups.txt, internal_groups.txt, private_groups.txt

"""
import argparse

from gitlab_utils import gl_auth

parser = argparse.ArgumentParser()

parser.add_argument('--gitlab_url', default='https://gitlab.pcs.cnu.edu', help='The url for the Gitlab server.')
parser.add_argument('token', help='Your private access token from Gitlab')

args = parser.parse_args()

url = args.gitlab_url
token = args.token
private=[]
internal=[]
public=[]

print("Access gitlab ...")
with gl_auth(url, token, admin=True) as gl:

    print(" Get all groups ... ")
    gp_list= gl.groups.list(as_list=False)

    cnt = 0
    for gl_gp in gp_list:
        if gl_gp.visibility=='internal':
            internal.append(gl_gp.full_path)
        if gl_gp.visibility=='private':
            private.append(gl_gp.full_path)
        if gl_gp.visibility=='public':
            public.append(gl_gp.full_path)

        cnt +=1

    print("Total groups=",cnt)
    print("     public  =",len(public))
    print("     internal=",len(internal))
    print("     private =",len(private))

    total = len(public) + len(private) + len(internal)

    if cnt != total:
        print("Totals not equal! {} vs. {} ",total,cnt)
        raise Exception(" Invalid processing !")

    print(" Write files ...")
    with open('private_groups.txt',"wt") as fout:
        fout.write('\n'.join(private))
    with open('internal_groups.txt',"wt") as fout:
        fout.write('\n'.join(internal))
    with open('public_groups.txt',"wt") as fout:
        fout.write('\n'.join(public))
    print("Done!")
