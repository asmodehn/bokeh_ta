import functools

from bokeh.models import BooleanFilter, CDSView, ColumnDataSource, Legend
from bokeh.plotting import Figure, figure

def ohlc(source):

    onesource = source

    def render(**figure_kwargs):

        figure = Figure(**figure_kwargs)

        figure.segment(source=onesource, legend_label="OHLC H/L",
                       x0='datetime', x1='datetime',
                       y0='low', y1='high',
                       line_width=1, color='black')

        updown = [o < c for o, c in zip(onesource.data['open'], onesource.data['close'])]

        figure.vbar(legend_label="OHLC Up",
                    source=onesource,
                    view=CDSView(source=onesource, filters=[BooleanFilter(updown)]),
                    width=(onesource.data['datetime'][1] - onesource.data['datetime'][0]) / 2,
                    x='datetime',
                    bottom='open', top='close',
                    fill_color="#D5E1DD", line_color="black",
                    )

        figure.vbar(legend_label="OHLC Down",
                    source=onesource,
                    view=CDSView(source=onesource, filters=[BooleanFilter([not b for b in updown])]),
                    width=(onesource.data['datetime'][1] - onesource.data['datetime'][0]) / 2,
                    x='datetime',
                    top='open', bottom='close',
                    fill_color="#F2583E", line_color="black",
                    )

        # point of calling super.__call__() ?? Legend ??
        figure.legend.location = "top_left"
        figure.legend.click_policy = "hide"

        return figure

    return render


if __name__ == '__main__':
    # A simple demo of outputting a figure to html file
    import pandas
    dataframe = pandas.DataFrame.from_records(
        # TODO : sample data from csv / cassettes ?
        [[1581024000, "8885.6", "8885.6", "8870.0", "8870.1", "8882.6", "3.40642649", 23],
                      [1581024060, "8870.1", "8871.3", "8863.5", "8870.3", "8869.1", "1.51573747", 21],
                      [1581024120, "8871.3", "8872.8", "8867.8", "8869.9", "8871.5", "2.55702814", 16],
                      [1581024180, "8869.9", "8880.1", "8869.9", "8880.1", "8876.9", "5.59530296", 21],
                      [1581024240, "8877.9", "8880.5", "8877.9", "8880.1", "8880.2", "0.58048481", 11],
                      [1581024300, "8880.1", "8880.1", "8878.8", "8879.3", "8879.1", "0.10505158", 4],
                      [1581024360, "8879.3", "8880.0", "8879.0", "8879.0", "8879.0", "0.12800715", 3],
                      [1581024420, "8879.4", "8883.2", "8879.4", "8882.9", "8881.8", "0.21217143", 8],
                      [1581024480, "8883.1", "8883.1", "8879.5", "8882.5", "8882.2", "1.06838783", 31],
                      [1581024540, "8881.1", "8882.5", "8879.3", "8882.4", "8881.3", "0.12026107", 10],
                      [1581024600, "8882.4", "8882.4", "8875.3", "8875.3", "8881.5", "1.89192643", 17],
                      [1581024660, "8875.2", "8875.2", "8869.0", "8873.2", "8869.9", "2.68435432", 18],
                      [1581024720, "8873.2", "8874.0", "8871.7", "8872.8", "8872.8", "0.27668860", 13],
         ],
        columns=["timestamp", "open", "high", "low", "close", "vwap", "volume", "count"],
    )
    # minimum processing to be compatible with OHLCFigure
    dataframe['datetime'] = pandas.to_datetime(dataframe.timestamp, unit="s")

    cds = ColumnDataSource(dataframe, name="OHLC")

    ohlcp = ohlc(source=cds)

    from bokeh.io import output_file
    from bokeh.plotting import save

    output_file(f"ohlc_sample.html", mode='inline')
    save(ohlcp(plot_height=320, tools='pan, wheel_zoom', toolbar_location="left",
                   x_axis_type="datetime", y_axis_location="right",
                   sizing_mode="scale_width"))
