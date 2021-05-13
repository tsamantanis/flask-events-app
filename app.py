from app import app
from flask import render_template

@app.errorhandler(404)
def show_404(error):
    """Display a 404 error page"""
    return render_template('error_page.html', message = "This page has melted in the sun", button = "Back to Home"), 404

if __name__ == "__main__":
    app.run(debug=True)
