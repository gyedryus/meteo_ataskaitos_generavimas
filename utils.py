import pandas as pd
import matplotlib.pyplot as plt
import os
import matplotlib.dates as mdates


def interpolate_values(
        data: pd.Series,
        interval: str = "5min",
        method: str = "cubic"
) -> pd.Series:
    """
    Interpoliuoja vienmačius laiko eilučių duomenis, sukuriant tarpines reikšmes
    nurodytu laiko intervalu ir pasirenkamu interpoliacijos metodu.

    :param data: Duomenų seka su DatetimeIndex.
    :param interval: Laiko intervalas tarp tarpinių reikšmių.
            Galimi pavyzdžiai: '1min', '5min', '15min', '1H', '1D'. (numatyta: '5min')
    :param method: Interpoliacijos metodas. Galimos reikšmės:
            ['linear', 'time', 'index', 'nearest', 'zero',
             'slinear', 'quadratic', 'cubic', 'pchip', 'akima', 'polynomial'].
            (numatyta: 'cubic')

    :return: Interpoliuota duomenų seka su nauju laiko intervalu.

    Raises:
        ValueError: Jei indeksas nėra DatetimeIndex arba nurodytas netinkamas metodas.
    """

    if not isinstance(data.index, pd.DatetimeIndex):
        raise ValueError("Duomenų sekos indeksas turi būti DatetimeIndex tipo.")

    valid_methods = [
        "linear", "time", "index", "nearest", "zero",
        "slinear", "quadratic", "cubic", "pchip",
        "akima", "polynomial"
    ]

    if method not in valid_methods:
        raise ValueError(
            f"Netinkamas metodas '{method}'. Pasirinkite vieną iš: {valid_methods}"
        )

    data = pd.to_numeric(data, errors="coerce")

    interpolated = data.resample(interval).interpolate(method=method)

    return interpolated


def plot_series(
        data_1: pd.Series,
        data_2: pd.Series = None,
        label_1: str = None,
        label_2: str = None
) -> None:
    """
    Funkcija atvaizduoja vieną arba dvi vienmačių laiko eilučių (pd.Series)
    sekas linijine diagrama.

    Jei nurodoma tik viena serija, nubraižomas vienas grafikas.
    Jei pateikiamos dvi serijos, jos pavaizduojamos skirtingomis spalvomis tame pačiame grafike.

    :param data_1: Duomenų seka su DatetimeIndex.
    :param data_2: Duomenų seka su DatetimeIndex.
    :param label_1: Kreivės pavadinimas pirmai duomenų sekai.
    :param label_2: Kreivės pavadinimas antrai duomenų sekai.
    :return: None.
    """

    if not isinstance(data_1.index, pd.DatetimeIndex):
        raise ValueError("Duomenų sekos Nr.1 indeksas turi būti DatetimeIndex tipo.")
    if data_2 is not None and not isinstance(data_2.index, pd.DatetimeIndex):
        raise ValueError("Duomenų sekos Nr.2 indeksas turi būti DatetimeIndex tipo.")

    data_1 = data_1.sort_index()
    if data_2 is not None:
        data_2 = data_2.sort_index()

    first_timestamp = data_1.index[0].strftime('%Y-%m-%d')
    if data_2 is not None:
        last_timestamp = data_2.index[-1].strftime('%Y-%m-%d')
    else:
        last_timestamp = data_1.index[-1].strftime('%Y-%m-%d')

    plt.figure(figsize=(12, 6))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    plt.plot(data_1.index, data_1.values, label=label_1, color="blue")

    if data_2 is not None:
        plt.plot(data_2.index, data_2.values, label=label_2, color="red")

    plt.xticks(rotation=45)
    plt.title(f"Oro temperatūra laikotarpyje nuo {first_timestamp} iki {last_timestamp}")
    plt.xlabel("Data")
    plt.ylabel("Temperatūra, °C")
    plt.legend()
    plt.grid(True, color='lightgrey', linewidth=0.5)
    plt.tight_layout()
    
    file_path = "temp_plot_output.png"
    
    plt.savefig(file_path)
    
    full_path = os.path.join(os.getcwd(), file_path)
    
    try:
        plt.savefig(full_path)
        print(f"Grafikas išsaugotas: {file_path}")
    except Exception as e:
        print(f"Klaida išsaugant grafiką faile {full_path}: {e}")

    plt.show()
    
    plt.close() 
