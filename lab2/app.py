from flask import Flask, render_template, request, redirect, url_for
from data_access.repositories import SqlAlchemyRepository
from business.services import ListingService

app = Flask(__name__)

# Initialize your layers
conn_str = "mssql+pyodbc://@DESKTOP-33IR0JT/rental_service?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
repo = SqlAlchemyRepository(db_url=conn_str)
listing_service = ListingService(repo)

@app.route('/')
def index():
    listings = listing_service.get_all_listings()
    return render_template('index.html', listings=listings)

@app.route('/delete/<id>')
def delete(id):
    listing_service.delete_listing(id)
    return redirect(url_for('index')) 

@app.route('/add', methods=['GET', 'POST'])
def add_listing_view():
    if request.method == 'POST':
        listing_service.create_listing(request.form)
        return redirect(url_for('index'))
    return render_template('listing_form.html', listing=None)

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_listing_view(id):
    listing = listing_service.get_listing_by_id(id)
    if request.method == 'POST':
        listing_service.update_listing(id, request.form)
        return redirect(url_for('index'))
    return render_template('listing_form.html', listing=listing)

if __name__ == '__main__':
    app.run(debug=True)    