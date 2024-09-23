from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用於 session 管理

@app.route('/', methods=['GET', 'POST'])
def index():
    # 初始化遊戲範圍和答案
    if 'answer' not in session:
        session['answer'] = 50  # 這裡假設答案是50，實際可以隨機生成
        session['min'] = 1
        session['max'] = 100

    if request.method == 'POST':
        guess = int(request.form['guess'])
        if guess < session['answer']:
            session['min'] = max(session['min'], guess)
            message = f"太小了！範圍：{session['min']} 到 {session['max']}"
        elif guess > session['answer']:
            session['max'] = min(session['max'], guess)
            message = f"太大了！範圍：{session['min']} 到 {session['max']}"
        else:
            message = "恭喜你猜對了！"

        return render_template('index.html', message=message)

    return render_template('index.html')

@app.route('/reset')
def reset():
    session.pop('answer', None)
    session.pop('min', None)
    session.pop('max', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)