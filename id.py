def showinfo(message):
    chat_id = message.chat.id
    reply = message.reply_to_message
    from_user = message.from_user
    if reply is not None:
        from_user = reply.from_user
        if reply.forward_from is not None:
            from_user = reply.forward_from
    from_id = from_user.id
    from_first = from_user.first_name
    from_last = from_user.last_name
    from_username = from_user.username
    from_name = from_first
    if from_last is not None:
        from_name += " " + from_last
    msg = "Info for this user:\n"
    msg += "Name:%s\n" % from_name
    msg += "ID:`%d`\n" % from_id
    msg += "Username: @%s" % from_username
    return msg
