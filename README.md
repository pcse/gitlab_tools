# GitLab Tools

### Christopher Newport University
### Department of Physics, Computer Science and Engineering
____

To help manage project and exam distribution using Git in our CS courses, we developed several Python scripts to assist in setting up student accounts, course groups, manage member permissions, and submit code.

For an overview, see our CCSC:Eastern 2019 paper [here](https://sites.google.com/site/ccsceastern/).

These convenience scripts are Python 3 wrappers to an existing [Python gitlab interface](https://python-gitlab.readthedocs.io/en/stable/)
to the GitLab Community Edition version 12.0.3 (API v4) that works by sending and receiving HTTP/S messages.

These tools have been tested with Ubuntu 16.04, Python 3.5.2,
python-gitlab 1.6.0, and GitLab 12.0.3 (API v4), but we anticipate
that they will work on most platforms with Python 3.x.

See https://python-gitlab.readthedocs.io/en/stable/install.html for information about installing the Python Gitlab interface.

To use our scripts, just clone this repo to your computer and invoke the scripts from their `gitlab_tools` folder, or add the folder to the Python path.

# Account Setup

The `gitlab_account_setup.py` script, located in the `gitlab_tools` folder, is used to set up a course given a text file of student emails.
The script requires admin permission on the GitLab server instance, and uses a GitLab API access token in lieu of a password.  
See https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html for additional information on creating such a token.

The script requires a `master_student_group` name,
and a personal `group_suffix` that is appended to the student usernames to identify their personal group for a particular course.
For example we might use `cpsc250-students-f19` as the `master_student_group`, and `cpsc250-f19` as the `group_suffix`.

Optionally, an instructor user name can be specified (if different from the admin user running the script),
as well as an expiration date to remove instructors from individual student groups.

The script first checks to see if the `master_student_group` exists, and creates it as necessary.
Next, the script parses a list of student email addresses given in a text file with one student per line.
We base the user names off of the student email address, which is formatted as
`first.last.yy@cnu.edu` at our school.  If the student user does not exist on our GitLab server, an account with username and default password `first.last.yy` is created for them.
Next, an individual group of the form `first.last.yy`-`group_suffix` is created if it does not exist,
and the instructor is added as a reporter.
The group is configured to be `private`,
so that only the individual student and instructor have access to projects in the group.

Usage:
```
python gitlab_account_setup.py <token> <csv_input> <master_student_group> (--personal_group_suffix <personal_group_suffix>) (--expire <expiration date>) (--gitlab_url <url>) (--instructor <instructor username>) (--delete_admin True)
```

The user running this script **MUST** be an admin of the Gitlab instance.
This script creates Gitlab accounts for students without accounts, adds all students to the `master_student_group`, and creates a personal group for each student with a *properly* formatted group name.
* `token` is the user access token (in lieu of password)
* `input` is the input file containing student email.
  * The script parses the email and uses everything before the `@` for user name
  * For CNU, we use `first.last.yy@cnu.edu` on each line,
  *  thus `first.last.yy` will be the assigned gitlab user name and initial password
* `master_student_group` is the group where the instructor posts git repositories for each project or exam.
* `personal_group_suffix` is the phrase appended to each student's user name to define a personal group (not created if empty).
* `expiration date` - expiration date for reporters (student's in master_student_group, and instructor in student personal groups)
* `url` - optional url for the gitlab server
  * defaults to CNU's internal gitlab server address
* `instructor` Instructor's gitlab username if the admin user is different from the instructor (default: unset)
* `delete_admin` set to True to remove the admin ID used to run this script from student personal groups; otherwise instructor and admin are members of created groups (default: False)

For CNU, the input CSV file should have lines that are formatted as:
```
captain.chris.18@cnu.edu
random.student.19@cnu.edu
...
```

For example if I want to set up Gitlab accounts for a class taught by `Dr. Code` with information (from above example) in `CPSC250_9AM.csv` with master student group `cpsc250-students-code-f19` (group with instructor name) and suffix `cspc250-f19`, I would run
```
python gitlab_account_setup.py <token> CPSC250_9AM.csv cpsc250-students-code-f19 --personal_group_suffix cpsc250-f19 --expire 2019-12-31 --instructor doctor.code --delete_admin True
```


It would first create the `cpsc250-students-code-f19` with Dr. Code (gitlab ID doctor.code) as the owner if it did not previously exist.

If Chris Captain did not have a gitlab account, it would then make one with username `captain.chris.18`;
each new account's initial password is set to the owner's user name (`first.last.yy`).
Then it would add him as a reporter to `cpsc250-students-code-f19` and it would create `captain.chris.18-cpsc250-f19` and add him as owner to the account, and add Dr. Code as a reporter.

You can comment a student out of the roster by placing a '#' as the first character in their line in the CSV file.

Note, when the script creates the group, the Admin running the script is owner by default and then demoted to reporter; use `delete_admin` option to remove as user after the creation.

# sample_project and webcat-submitter.py

The `sample_project` contains a simple refresher Hello World project that we give to students as they are first learning our work flow.  For our course, this project would be its own repository posted to the `master_student_group` created for each course.  All of our projects and exams are distributed this way.

These projects are private, and individually forked to each students personal group for the course.  The projects must remain with `private` visibility; we consider it an honor code violation for students to make these projects `public` or `internal`.

Our projects and exams follow this typical layout:
```txt
project_root/
  |-- README.md
  |
  |-- .gitignore
  |
  |-- .gitlab-ci.yml
  |-- webcat-submitter.py
  |-- webcat-submitter-1.0.4.jar
  |
  |-- src/   (files that students create or modify for submission)
  |-- tests/ (test files distributed to students)
  |-- exam/  (optional folder containing exam identifiers)
  |-- data/  (optional data files used by programs)
  |-- docs/  (optional folder for additional documenation)
  |-- given/ (optional any files provided to students)
  |-- img/   (optional folder for images used in README and docs)
```

Our `sample_project` also includes a `webcat` folder that demonstrates how we set code up on WebCAT to
make use of multiple tests files and custom exam problems for a single submission site.

The students push their code to their personal fork, the unit tests are automatically run according to the `.gitlab-ci.yml` file, and results are reported as part of GitLab's Continuous Integration (CI) system.

We make use of the [WebCat](https://web-cat.org/) system for automatic grading based on unit tests.

The `webcat-submitter.py` script is run by the CI system as specified in the `.gitlab-ci.yml` file.  The `webcat-submitter` script packages the relevant folders and submits to the WebCAT server using
the standard [webcat-submitter-1.0.4.jar](https://github.com/web-cat/electronic-submitter) file.
This occurs every single commit, so we allow students to submit as many times as they like, but still encourage them to debug using their local IDE software.

As part of the initial course setup, the student creates a pair of `WCUSER` and `WCPASS` environment variables in the student's personal group via the GitLab web interface;
these environment variables store the student's Web-CAT user name and password respectively.  Once configured, the system works automatically unless the password is changed during the semester; students can easily update the environment variables.

The submitter script uploads the student code found in a list of folders specified in the `.gitlab-ci.yml` file.
Typically we upload the `src/` and possibly an `exam/` folder; the `given/` and final `test/` code is common on the WebCAT server.  The `exam/` folder is used to identify specific versions of an exam that may be distributed to students, and can be used to specify specific tests for WebCAT to load.


# Other Miscellaneous Scripts

Additional scripts are located in the `gitlab_tools` folder.

## gitlab_remove_from_groups.py

This script removes the specified user from any groups whose name ends with the specified suffix if they are a member.
This is useful for removing instructors from student personal groups after the semester is over (normally set expriration date).
Usage:
`./gitlab_remove_from_groups.py <token> --instructor <instructor> --suffice <group suffix> (--gitlab_url <server url>)`
E.g. To remove instructor doctor.code from all groups ending with the suffix `cpsc250-s18` run
`./gitlab_remove_from_groups.py notmytoken --instructor doctor.code --suffix cpsc250-s18`
If `instructor` option is left out, then the admin running script (by token) is removed.

## gitlab_list_groups_by_visibility.py, gitlab_list_groups_by_visibility.py, gitlab_set_group_visibility.py

These scripts generate text files that list groups or projects by visibility level.  They are useful for checking that group/projects are as expected.  The files can be used as input into the `gitlab_set_group_visibility` script.

## gitlab_check_group_membership.py, gitlab_remove_from_groups_list.py

These scripts can be used to get a list of all groups where a specified user is a member, and return those groups as a text file, which can be used as input to the `gitlab_remove_from_groups_list` script.


## gitlab_create_project.py

The `gitlab_create_project` script is used to create a named project under a specified group.
This is useful for defining empty projects following a given naming convention.
While it is typically easier to create single projects via the GitLab web interface,
this script enables future developments such as automated deployment of projects.


## gitlab_check_class_access.py

We use the same workflow for in-class exams that we do for projects and labs,
and therefore give students access to their GitLab account and
prior work during the exam.  The `gitlab_check_class_access` script is used to verify that
no unauthorized persons have been given permission to view contents of
another student's GitLab group or individual project repo.

## gitlab_add_student_pairs.py

For code review, or pair programming assignments, students must be given access to their partner's *project* repository.  Note: Their personal group remains private, but we can allow partners on a project-by-project basis.
The script `gitlab_add_student_pairs.py` takes a pairing of email addresses in csv form, and adds the associated partner to a specified project in their respective groups with `Reporter` access by default.  The script also allows for an optional expiration date when the partner is removed from access.

This script is useful for code review exercises where students comment directly in the GitLab web interface.
This makes the review conform to professional practices, and allows direct feedback to all.

For pair programming, the second person needs ``Developer`` access to the partner's single project.
We generally have pairs share a single repo and follow
a `Pull-Edit-Commit-Push-Switch` workflow to avoid merge issues.
