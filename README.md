# QuantLib

* The scope of this project is to use QuantLib for calculation of option prices


    https://www.quantlib.org/

## Docker

* docker_local_deploy.bat is used to:
  * create the image
  * push the image into docker hub
  * to run the container

## Option Pricing Request Example

```
  {
    "calculation_date": "2023-04-22",
    "maturity_date": "2024-04-22",
    "spot_price": 127.62,
    "strike_price": 130.0,
    "volatility": 0.20,
    "dividend_rate": 0.0163,
    "risk_free_rate": 0.001,
    "option_type": "call",
    "exercise_type": "european"
  }
