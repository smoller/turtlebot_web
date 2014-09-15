from flask import Flask, render_template

@app.route('/')
def index():
    render_template('index.html')
