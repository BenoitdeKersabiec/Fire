## :computer: Fire calculator

This repository contains a Fire calculator, to simulate an investing strategy.

---

## :file_folder: Project layout

```text
.
├── main.py                                     # The simulation script
├── requirements.txt
├── .gitignore
└── README.md

```

---

## :wrench: How to run the code

1. Install `requirements.txt` in your `Python` environment with `pip install -r requirements.txt`.
2. Run the command `python -m main` to run a simulation. 

To change the default parameters, you can specify them using `python -m similarity with start_date=<DATE> end_date=<DATE>`. When not specified, the default parameters are: `python -m similarity with start_date="01/01/2025" end_date="01/01/2100"`

Optional arguments you can add after `with`:

- `mode=<MODE>` Mode is either `simulate` or `eval`. 

   - `simulate` will run a simulation with the specified parameters
   - `eval` will run multiple simulation to simulate all the possible retirement dates, and evaluate the first retirement wage for a given retirement date
- `start_date=<DATE>` The first investment date. Default is `"01/01/2025"`.
- `end_date=<DATE>` The last investment date (i.e. your death). Default is `"01/01/2100"`.
- `monthly_investment=<VALUE>` The starting monthly investment amount. Default is `500`.
- `investment_annual_growth_rate=<VALUE>` The annual growth rate of your monthly investment. Default is `0.1` (i.e. 10%).
- `annual_return=<VALUE>` The annual return rate of your investments. Default is `0.08` (i.e. 8%).
- `retirement_date=<DATE>` The retirement date on which your monthly investments stop and you start to live from your investments' returns. Default is `"01/01/2045"`.
- `retirement_percentage=<VALUE>` The percentage of your networth you live on during your retirement. Default is `0.04` (i.e. 4%).
- `save_resutls_to_csv=<BOOL>` Boolean specifying if you want to save the computed data to a CSV. Default is `True`. The output filename is `output.csv`
---

## :man: Author
- [Benoit Sioc'han de Kersabiec](https://github.com/BenoitdeKersabiec)

