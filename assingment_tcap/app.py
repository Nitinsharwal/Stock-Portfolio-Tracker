from flask import Flask, render_template, send_file
import pandas as pd

app = Flask(__name__)

results_file = "backtest_results.csv"
trades_df = pd.read_csv(results_file)


@app.route("/")
def index():
    return render_template("index.html", trades=trades_df.to_dict(orient="records"))


@app.route("/download")
def download():
    return send_file(results_file, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
