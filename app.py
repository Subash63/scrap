from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape_product():
    product_id = request.form['product_id']

    url=f'https://www.moparpartsgiant.com/parts/mopar-belt-serpentine~{product_id}.html'
    
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        product = soup.find('table',class_="pn-spec-list")
        product_data=[]
        for rows in product:
            cells= rows.find_all('td')
            rows_data=[cells.text.strip() for cells in cells]
            product_data.append(rows_data)


        vehicle = soup.find('table',class_="fit-vehicle-list-table")
        Vehicle_data=[]
        for rows2 in vehicle:
            cell_data=rows2.find_all('td')
            rows_data1=[cell_data.text.strip() for cell_data in cell_data]
            Vehicle_data.append(rows_data1)

        product_details = {
            'name': soup.find('h1', {'class': 'pn-detail-h1'}).text.strip(),
            'price': soup.find('span', {'class': 'price-section-price'}).text.strip(),
            'ModelandPartNumber':soup.find('p',class_="pn-detail-sub-desc").text.strip(),
            'MRPprice': soup.find('span', class_="price-section-retail").text.strip(),
            'Partdescription':soup.find('li',class_="pn-detail-description").div.text.strip(),

            'Productdescrition': product_data,

            'VehicleFit': Vehicle_data
        }
        

        with open(f'{product_id}_details.json', 'w') as json_file:
            json.dump(product_details, json_file, indent=2)

        return jsonify(product_details)
    else:
        return jsonify({'error': 'Failed to fetch product details'}), 500
    




if __name__ == '__main__':
    app.run(debug=True)
