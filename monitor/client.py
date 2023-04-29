import sqlite3
import json
import time
import math
from rich.live import Live
from rich.table import Table

SWID_MAP = {
     1: 'sri',
     2: 'utah',
     3: 'ucsb',
     4: 'ucla'
}

HOST_MAP = {
     '192.0.0.2': 'h1',
     '192.3.0.2': 'h2',
     '192.1.0.2': 'h3',
     '192.2.0.2': 'h4'
}

# create db
conn = sqlite3.connect('monitor.db')
cursor = conn.cursor()

def generate_table() -> Table:
    """Make a new table."""
    table = Table()
    table.add_column("ID")
    table.add_column("[red]End2End")
    table.add_column("[magenta]switch_path")
    table.add_column("[violet]init_size")
    table.add_column("[cyan]avg_size")
    table.add_column("[green]latency")
    table.add_column("[pink3]Jitter")
    table.add_column("[navy_blue]bandwidth")
    table.add_column("[purple4]throughput")

    cursor.execute('select * from ping_data')
    values = cursor.fetchall()

    latency_list = [row[4] - row[3] for row in values]
    latency_mean = sum(latency_list) / len(latency_list) if len(latency_list) != 0 else 0

    min = max(0, len(values) - 50)
    for row in range(min, len(values)):
        id = values[row][0]
        # end to end
        summary = values[row][1]
        summary = summary.split(' -> ')
        summary = ' -> '.join(HOST_MAP[node] for node in summary)
        # switch message extract
        switches = json.loads(values[row][2])
        start_time = values[row][3]
        end_time = values[row][4]
        init_size = values[row][5]

        switch_path = ' -> '.join([SWID_MAP[switch['name']] for switch in switches])
        # switch_time = ' -> '.join([str(switch['time']) for switch in switches if switch.get('time')])
        switch_size = [switch['size'] for switch in switches]
        avg_psize = sum(switch_size) / len(switch_size) if len(switch_size) != 0 else 0
        
        Latency = end_time - start_time # s
        Jitter = math.sqrt((Latency - latency_mean) ** 2) #stability
        Bandwidth = avg_psize / Latency * 8 if Latency != 0 else 0 #bps
        Throughput = avg_psize / Latency if Latency != 0 else 0 #bytes/s

        init_size_txt = str(init_size) + "/bytes"
        avg_psize_txt = str(int(avg_psize)) + "/bytes"
        Latency_txt = str('%.2f' % (Latency * 1000)) + "(ms)"
        Jitter_txt = str('%.2f' % (Jitter * 1000)) + "(ms)"
        Bandwidth_txt = str('%.3f' % (Bandwidth/1000)) + "/kbps"
        Throughput_txt = str('%.2f' % Throughput) + "(bytes/s)"
        # summary
        table.add_row(str(id),
                      '[red]'+ summary, 
                      '[magenta]'+ switch_path,
                      '[violet]' + init_size_txt,
                      '[cyan]'+ avg_psize_txt,
                      '[green]'+ Latency_txt,
                      '[orange3]' + Jitter_txt,
                      '[navy_blue]'+ Bandwidth_txt,
                      '[purple4]'+ Throughput_txt)
    
    return table


with Live(generate_table(), refresh_per_second=4) as live:
    for _ in range(40):
        time.sleep(0.5)
        live.update(generate_table())