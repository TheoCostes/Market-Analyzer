# Market-Analyzer

Market Analyzer is a web application that screen the crypto market quotes and return a report of advice for the managament of an active portfolio.
It is built with Python, and uses the Streamlit framework for the frontend.

## Features

- Trend analyzer (TA): a module that screen the market and return the Top N crypto assets in a good trend.
- Portfolio analyzer : a module that take the analyze of the TA and the portfolio state, and return the adjustment of the portfolio to do.
- Dashboard: Under development => I will add some performance visualization + a market analysis.

## Roadmap to follow

- connect to api to get historical data from diferent market ==> DONE
- create a pipeline to transform the data and create features
- create a pipeline to train a model for the TA
- create a pipeline to train a model for the PA
- Deploy the model on a server
- create a dashboard to visualize the performance of your portfolio
- create a dashboard to rank assets by performance
- create a dashboard to visualize the performance of the TA


## Installation

1. Clone the repository:
```bash
git clone https://github.com/TheoCostes/Market-Analyzer.git
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

After running the application, navigate to the provided local URL in your web browser. Register or log in to access the dashboard.  

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
