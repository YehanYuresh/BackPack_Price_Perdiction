from flask import Flask, render_template, request
import pickle, os
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    price = 0
    if request.method == 'POST':
        brand = request.form['brand']
        material = request.form['material']
        Sizesmall = request.form.getlist('small')
        Sizemedium = request.form.getlist('medium')
        Sizelarge = request.form.getlist('large')
        Sizeunknown = request.form.getlist('unknown')
        compartments = request.form['compartments']
        laptopCompartment = request.form.getlist('laptopCompartment')
        waterproof = request.form.getlist('waterproof')
        style = request.form['style']
        color = request.form['color']
        weightCapacity = request.form['weightCapacity']

        send_list = []
        brand_list = ['Adidas', 'Jansport', 'Nike', 'Puma', 'Under Armour', 'Other']
        material_list = ['Canvas', 'Leather', 'Nylon', 'Polyester', 'Other']
        style_list = ['Backpack', 'Messenger', 'Tote', 'Unknown']
        color_list = ['Black', 'Blue', 'Grey', 'Green', 'Pink', 'Red', 'Unknown']

        def addtoList(list, value):
            for i in list:
                if value == i:
                    list.append(1)
                else:
                    list.append(0)

        send_list.append(int(compartments)if compartments else 0)
        send_list.append(int(laptopCompartment[0]) if laptopCompartment else 0)
        send_list.append(int(waterproof[0]) if waterproof else 0)
        send_list.append(int(weightCapacity)if weightCapacity else 0)

        for i in brand_list:
            if brand == i:
                send_list.append(1)
            else:
                send_list.append(0)

        for m in material_list:
            if material == m:
                send_list.append(1)
            else:
                send_list.append(0)

        send_list.append(int(Sizelarge[0]) if Sizelarge else 0)
        send_list.append(int(Sizemedium[0]) if Sizemedium else 0)
        send_list.append(int(Sizemedium[0]) if Sizemedium else 0)
        send_list.append(int(Sizesmall[0]) if Sizesmall else 0)
        send_list.append(int(Sizeunknown[0]) if Sizeunknown else 0)

        for s in style_list:
            if style == s:
                send_list.append(1)
            else:
                send_list.append(0)

        for c in color_list:
            if color == c:
                send_list.append(1)
            else:
                send_list.append(0)

        print(send_list)

        filename = 'model/gradient_boosting_model.pkl'
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                model = pickle.load(file)

            # Create a DataFrame for a new sample
            new_data_df = pd.DataFrame([send_list])

            # Make a prediction
            predicted_price = model.predict(new_data_df)
            price = predicted_price[0]

    return render_template('index.html', price=price)

if __name__ == '__main__':
    app.run(debug=True)