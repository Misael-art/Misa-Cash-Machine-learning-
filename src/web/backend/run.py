from web.backend.app import create_app, db
from web.backend.app.models import Transaction

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Configura o contexto do shell com objetos úteis."""
    return {'db': db, 'Transaction': Transaction}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 