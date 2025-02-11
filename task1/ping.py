import pandas as pd
from pythonping import ping


result_path = "ping_results.csv"


addresses = ["google.com",
             "tetr.io",
             "github.com",
             "en.wikipedia.com",
             "nsu.ru",
             "fresh.nsuts.ru",
             "orel-region.ru",
             "president.gov.by",
             "vk.com",
             "mail.google.com"]


def save_to_csv(host, min_ms, avg_ms, max_ms):
    df = pd.DataFrame([[host, min_ms, avg_ms, max_ms]])
    df.to_csv(result_path, mode='a', index=False, header=False)

    print(f"Saved to {result_path}: {min_ms}, {avg_ms}, {max_ms} ms")


def get_rtt(addresses_arr):
    for address in addresses_arr:
        response = ping(address)
        save_to_csv(address, response.rtt_min_ms, response.rtt_avg_ms,
                    response.rtt_max_ms)


get_rtt(addresses)
