def bug_msg_builder(bugs):
    bug_concat = []
    if isinstance(bugs, str):
        return bugs
    else:
        for bug_dict in bugs:
            bug_concat.append(bug_dict.summary + " " + bug_dict.weburl)
        return bug_concat


def bugs_count(bugs_messages_to_send):
    if not type(bugs_messages_to_send) == str:
        return len(bugs_messages_to_send)
    else:
        return 0


def amt_string(num_of_bugs):
    if num_of_bugs == 1:
        return ' is '
    else:
        return ' are '
