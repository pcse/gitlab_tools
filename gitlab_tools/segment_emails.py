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

import re
import sys

def segment_emails(fin, fout):
    """
    Given emails formated as either:
     1) email@address , or
     2) Name < email@address >
    Output file as email@address only
    """
    lines=[]
    with open(fin,"rt") as file:
      lines = file.readlines()
      print(" Read ",len(lines),"  lines from file ...")
      for item, line in enumerate(lines):
        line = line.strip()
        segments = re.split("<|>",line)
        if len(segments)== 3:
            lines[item] = segments[1].strip()
        elif len(segments) == 1:
            lines[item] = segments[0].strip()
        else:
            print("    Error: at line ",item," ",line)

    with open(fout,"wt") as file:
        file.writelines([line+"\n" for line in lines])

if __name__ == "__main__":
    fin = "roster.txt"
    fout = "roster.txt"
    if len(sys.argv) > 1:
        fin = sys.argv[1]
        fout = sys.argv[1] # Assume same name if only 1 arg

    if len(sys.argv) > 2:
        fout = sys.argv[2]

    print("Segment emails in ",fin," to ",fout)
    segment_emails(fin, fout)
