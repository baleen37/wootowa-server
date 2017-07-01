from flask import Flask
import sys
print('web/app')


from wootowa.web.views import register_bp

app = Flask(__name__)
app.config.from_object('wootowa.glb.config.Config')

register_bp(app)
