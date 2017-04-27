from app import app


# HEALTH-CHECK

@app.route('/health-check')
def health_check():
	return 'It lives!!!'