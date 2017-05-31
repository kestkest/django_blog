def notification_processor(request):
    if not request.user.is_anonymous():
        unread_notifications = request.user.notifications.filter(is_read=False)
        notifications = request.user.notifications.all()[:10]
        short_note_list = notifications[:10]
        count = unread_notifications.count()
        return {
            'notifications': notifications,
            'count': count,
            'short': short_note_list,
            'n': notifications[0]
        }
    else:
        return {
            'notifications': None,
            'count': None
        }
