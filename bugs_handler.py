def bug_msg_builder(bugs):
    bug_concat = []
    if isinstance(bugs, str):
        return bugs
    else:
        for bug_dict in bugs:
            bug_concat.append(bug_dict.summary + " " + bug_dict.weburl)
        return bug_concat
