from flask import Flask, render_template, request

app = Flask(__name__)

def code():
    return request.args.get('code')

def get_code(data):
    file_name = raw_input('Enter file name')
    with open("C:/" + file_name + '.txt', 'a') as text_file:
        text_file.write(data + '\n')

def run():
    data = code()
    get_code(data)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/authgood')
def exchange():
    run()
    return render_template('token_exchange.html')

if __name__ == '__main__':
    app.run()

