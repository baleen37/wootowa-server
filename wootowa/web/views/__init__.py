def register_bp(app):
    """
    blue print 등록
    :param app:
    :return:
    """
    from wootowa.web.views.v1 import user
    app.register_blueprint(user.bp)
