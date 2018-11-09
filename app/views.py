from app import app


@app.route('/custom_views')
def index():
    return 'hello cust'

